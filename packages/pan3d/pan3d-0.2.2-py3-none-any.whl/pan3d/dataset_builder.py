import json
import os
import pandas
import pyvista
import typing
import xarray
from pathlib import Path
from pvxarray.vtk_source import PyVistaXarraySource
from pyvista.trame.ui import plotter_ui

from trame.decorators import TrameApp, change
from trame.app import get_server
from trame.widgets import html, client
from trame.widgets import vuetify3 as vuetify
import trame_server
import trame_vuetify

from pan3d.ui import AxisDrawer, MainDrawer, Toolbar, RenderOptions
from pan3d.utils import (
    initial_state,
    has_gpu_rendering,
    run_singleton_task,
    coordinate_auto_selection,
)

BASE_DIR = Path(__file__).parent
CSS_FILE = BASE_DIR / "ui" / "custom.css"


@TrameApp()
class DatasetBuilder:
    """Manage data slicing, mesh creation, and rendering for a target N-D dataset."""

    def __init__(
        self,
        server: typing.Union[trame_server.core.Server, str] = None,
        dataset_path: str = None,
        state: dict = None,
        pangeo: bool = False,
    ) -> None:
        """Create an instance of the DatasetBuilder class.

        Parameters:
            server: Trame server instance.
            dataset_path: A path or URL referencing a dataset readable by xarray.open_dataset()
            state:  A dictionary of initial state values.
            pangeo: If true, use a list of example datasets from Pangeo Forge (examples/pangeo_catalog.json).
        """

        server = get_server(server, client_type="vue3")
        self.server = server
        self._layout = None
        self._force_local_rendering = not has_gpu_rendering()

        self.state.update(initial_state)
        self.algorithm = PyVistaXarraySource()
        self.plotter = pyvista.Plotter(off_screen=True, notebook=False)
        self.plotter.set_background("lightgrey")
        self.dataset = None
        self.da = None
        self._mesh = None
        self.actor = None

        self.ctrl.get_plotter = lambda: self.plotter
        self.ctrl.reset = self.reset

        if pangeo:
            with open(Path(BASE_DIR, "../examples/pangeo_catalog.json")) as f:
                self.state.available_datasets += json.load(f)

        if dataset_path:
            self.state.dataset_path = dataset_path
            self.set_dataset_path(dataset_path=dataset_path)
        if state:
            self.state.update(state)

        if self._force_local_rendering:
            pyvista.global_theme.trame.default_mode = "client"

    # -----------------------------------------------------
    # Properties
    # -----------------------------------------------------

    @property
    def state(self) -> trame_server.state.State:
        """Returns the current State of the Trame server."""
        return self.server.state

    @property
    def ctrl(self) -> trame_server.controller.Controller:
        """Returns the Controller for the Trame server."""
        return self.server.controller

    @property
    def data_array(self) -> xarray.core.dataarray.DataArray:
        """Returns the current Xarray data array with current slicing applied."""
        return self.algorithm.sliced_data_array

    @property
    def mesh(
        self,
    ) -> typing.Union[pyvista.core.grid.RectilinearGrid, pyvista.StructuredGrid]:
        """Returns the PyVista Mesh derived from the current data array."""
        if self._mesh is None:
            self._mesh = self.algorithm.mesh
        return self._mesh

    @property
    def viewer(self) -> trame_vuetify.ui.vuetify3.VAppLayout:
        """Constructs and returns a Trame UI for managing and viewing the current data."""
        if self._layout is None:
            # Build UI
            self._layout = trame_vuetify.ui.vuetify3.VAppLayout(self.server)
            with self._layout:
                client.Style(CSS_FILE.read_text())
                Toolbar(
                    self.ctrl.reset,
                    self.import_config,
                    self.export_config,
                )
                MainDrawer()
                AxisDrawer(
                    coordinate_select_axis_function=self._coordinate_select_axis,
                    coordinate_change_slice_function=self._coordinate_change_slice,
                    coordinate_toggle_expansion_function=self._coordinate_toggle_expansion,
                )
                with vuetify.VMain(v_show=("da_active",)):
                    vuetify.VBanner(
                        "{{ ui_error_message }}",
                        v_show=("ui_error_message",),
                    )
                    with html.Div(style="height: 100%; position: relative"):
                        RenderOptions()
                        with plotter_ui(
                            self.ctrl.get_plotter(),
                            interactive_ratio=1,
                            collapse_menu=True,
                        ) as plot_view:
                            self.ctrl.view_update = plot_view.update
                            self.ctrl.reset_camera = plot_view.reset_camera
                            self.ctrl.push_camera = plot_view.push_camera
        return self._layout

    # -----------------------------------------------------
    # UI bound methods
    # -----------------------------------------------------

    def _coordinate_select_axis(
        self, coordinate_name, current_axis, new_axis, **kwargs
    ):
        if self.state[current_axis]:
            self.state[current_axis] = None
        if new_axis and new_axis != "undefined":
            self.state[new_axis] = coordinate_name

    def _coordinate_change_slice(self, coordinate_name, slice_attribute_name, value):
        if value.isnumeric():
            coordinate_matches = [
                (index, coordinate)
                for index, coordinate in enumerate(self.state.da_coordinates)
                if coordinate["name"] == coordinate_name
            ]
            if len(coordinate_matches) > 0:
                coord_i, coordinate = coordinate_matches[0]
                value = float(value)
                if slice_attribute_name == "step":
                    if value > 0 and value < coordinate["size"]:
                        coordinate[slice_attribute_name] = value
                else:
                    if (
                        value >= coordinate["range"][0]
                        and value <= coordinate["range"][1]
                    ):
                        coordinate[slice_attribute_name] = value

                self.state.da_coordinates[coord_i] = coordinate
                self.state.dirty("da_coordinates")

    def _coordinate_toggle_expansion(self, coordinate_name):
        if coordinate_name in self.state.ui_expanded_coordinates:
            self.state.ui_expanded_coordinates.remove(coordinate_name)
        else:
            self.state.ui_expanded_coordinates.append(coordinate_name)
        self.state.dirty("ui_expanded_coordinates")

    # -----------------------------------------------------
    # User-accessible state change functions
    # -----------------------------------------------------

    def set_dataset_path(self, dataset_path: str) -> None:
        """Set the path to the current target dataset.

        Parameters:
            dataset_path: A local path or remote URL referencing a dataset readable by xarray.open_dataset()
        """
        if dataset_path != self.state.dataset_path:
            self.state.dataset_path = dataset_path

        self.dataset = None
        if dataset_path is None:
            return

        self.state.ui_loading = True
        for available_dataset in self.state.available_datasets:
            if (
                available_dataset["url"] == dataset_path
                and "more_info" in available_dataset
            ):
                self.state.ui_more_info_link = available_dataset["more_info"]
        if "https://" in dataset_path or os.path.exists(dataset_path):
            engine = None
            if ".zarr" in dataset_path:
                engine = "zarr"
            if ".nc" in dataset_path:
                engine = "netcdf4"
            try:
                self.dataset = xarray.open_dataset(
                    dataset_path, engine=engine, chunks={}
                )
            except Exception as e:
                self.state.ui_error_message = str(e)
                return
        else:
            # Assume it is a named tutorial dataset
            self.dataset = xarray.tutorial.load_dataset(dataset_path)
        # reset algorithm
        self.algorithm = PyVistaXarraySource()

        self.state.da_attrs = [
            {"key": k, "value": v} for k, v in self.dataset.attrs.items()
        ]
        self.state.da_attrs.insert(
            0,
            {
                "key": "dimensions",
                "value": str(dict(self.dataset.dims)),
            },
        )

        self.state.da_vars = [
            {"name": k, "id": i} for i, k in enumerate(self.dataset.data_vars.keys())
        ]
        self.state.da_vars_attrs = {
            var["name"]: [
                {"key": str(k), "value": str(v)}
                for k, v in self.dataset.data_vars[var["name"]].attrs.items()
            ]
            for var in self.state.da_vars
        }

        self.state.dataset_ready = True
        if len(self.state.da_vars) > 0:
            self.set_data_array_active_name(self.state.da_vars[0]["name"])
        else:
            self.state.no_da_vars = True
            self.set_data_array_active_name(None)
        self.state.ui_loading = False

    def set_data_array_active_name(self, da_active: str) -> None:
        """Set the name of the current data array within the current dataset.

        Parameters:
            da_active: The name of a data array that exists in the current dataset.
        """
        if da_active == self.da:
            return

        self.da = da_active
        if da_active != self.state.da_active:
            self.state.da_active = da_active

        self.state.update(
            dict(
                da_x=None,
                da_y=None,
                da_z=None,
                da_t=None,
                da_t_index=0,
                da_coordinates=[],
                ui_expanded_coordinates=[],
                ui_error_message=None,
                ui_axis_drawer=False,
                ui_current_time_string="",
            )
        )
        if self.dataset is None or da_active is None:
            return

        da = self.dataset[da_active]
        for key in da.dims:
            current_coord = da.coords[key]
            d = current_coord.dtype
            array_min = current_coord.values.min()
            array_max = current_coord.values.max()

            # make content serializable by its type
            if d.kind in ["m", "M", "O"]:  # is timedelta or datetime
                if not hasattr(array_min, "strftime"):
                    array_min = pandas.to_datetime(array_min)
                if not hasattr(array_max, "strftime"):
                    array_max = pandas.to_datetime(array_max)
                array_min = array_min.strftime("%b %d %Y %H:%M")
                array_max = array_max.strftime("%b %d %Y %H:%M")
            elif d.kind in ["i", "u"]:
                array_min = int(array_min)
                array_max = int(array_max)
            elif d.kind in ["f", "c"]:
                array_min = round(float(array_min), 2)
                array_max = round(float(array_max), 2)

            coord_attrs = [
                {"key": str(k), "value": str(v)}
                for k, v in da.coords[key].attrs.items()
            ]
            coord_attrs.append({"key": "dtype", "value": str(da.coords[key].dtype)})
            coord_attrs.append({"key": "length", "value": int(da.coords[key].size)})
            coord_attrs.append(
                {
                    "key": "range",
                    "value": [array_min, array_max],
                }
            )
            if key not in [c["name"] for c in self.state.da_coordinates]:
                self.state.da_coordinates.append(
                    {
                        "name": key,
                        "attrs": coord_attrs,
                        "size": da.coords[key].size,
                        "range": [array_min, array_max],
                        "start": array_min,
                        "stop": array_max,
                        "step": 1,
                    }
                )
            if key not in self.state.ui_expanded_coordinates:
                self.state.ui_expanded_coordinates.append(key),
        self.state.dirty("da_coordinates", "ui_expanded_coordinates")
        self.auto_select_coordinates()
        if len(self.state.da_coordinates) > 0:
            self.state.ui_axis_drawer = True

        self.plotter.clear()
        self.plotter.view_isometric()

    def set_data_array_axis_names(self, **kwargs: dict) -> None:
        """Assign any number of coordinates in the current data array to axes x, y, z, and/or t.

        Parameters:
            kwargs: A dictionary mapping of axis names to coordinate names.\n
                Keys must be 'x' | 'y' | 'z' | 't'.\n
                Values must be coordinate names that exist in the current data array.\n
                Example: {'x': 'longitude', 'y': 'latitude', 'z': 'depth', 't': 'hour'}
        """
        if "x" in kwargs and kwargs["x"] != self.state.da_x:
            self.state.da_x = kwargs["x"]
        if "y" in kwargs and kwargs["y"] != self.state.da_y:
            self.state.da_y = kwargs["y"]
        if "z" in kwargs and kwargs["z"] != self.state.da_z:
            self.state.da_z = kwargs["z"]
        if "t" in kwargs and kwargs["t"] != self.state.da_t:
            self.state.da_t = kwargs["t"]

    def set_data_array_time_index(self, index: int) -> None:
        """Set the index of the current time slice.

        Parameters:
            index: Must be an integer >= 0 and < the length of the current time coordinate.
        """
        if int(index) != self.state.da_t_index:
            self.state.da_t_index = int(index)
        if self.dataset and self.state.da_active and self.state.da_t:
            time_steps = self.dataset[self.state.da_active][self.state.da_t]
            current_time = time_steps.values[self.state.da_t_index]
            if not hasattr(current_time, "strftime"):
                current_time = pandas.to_datetime(current_time)
            self.state.ui_current_time_string = current_time.strftime("%b %d %Y %H:%M")

    def set_data_array_coordinates(self, da_coordinates: list[dict]):
        """Set the info for coordinates in the current data array, including slicing.

        Parameters:
            da_coordinates: A list of dictionaries, where each dictionary contains the following mapping:\n
                name: the name of a coordinate that exists in the current data array\n
                start: the coordinate value at which the sliced data should start (inclusive)\n
                stop: the coordinate value at which the sliced data should stop (exclusive)\n
                step: an integer > 0 which represents the number of items to skip when slicing the data (e.g. step=2 represents 0.5 resolution)
        """
        if self.state.da_coordinates != da_coordinates:
            self.state.da_coordinates = da_coordinates
        slicing = {}
        for coord in da_coordinates:
            if coord["name"] != self.state.da_t:
                slicing[coord["name"]] = [
                    coord["start"],
                    coord["stop"],
                    coord["step"],
                ]
        self.state.slicing = slicing

    def set_render_scales(self, **kwargs) -> None:
        """Set the scales at which each axis (x, y, and/or z) should be rendered.

        Parameters:
            kwargs: A dictionary mapping of axis names to integer scales.\n
                Keys must be 'x' | 'y' | 'z'.\n
                Values must be integers > 0.
        """
        if "x" in kwargs and kwargs["x"] != self.state.render_x_scale:
            self.state.render_x_scale = int(kwargs["x"])
        if "y" in kwargs and kwargs["y"] != self.state.render_y_scale:
            self.state.render_y_scale = int(kwargs["y"])
        if "z" in kwargs and kwargs["z"] != self.state.render_z_scale:
            self.state.render_z_scale = int(kwargs["z"])
        self.plotter.set_scale(
            xscale=self.state.render_x_scale or 1,
            yscale=self.state.render_y_scale or 1,
            zscale=self.state.render_z_scale or 1,
        )

    def set_render_options(
        self,
        colormap: str = "viridis",
        transparency: bool = False,
        transparency_function: str = None,
        scalar_warp: bool = False,
    ) -> None:
        """Set available options for rendering data.

        Parameters:
            colormap: A colormap name from Matplotlib (https://matplotlib.org/stable/users/explain/colors/colormaps.html)
            transparency: If true, enable transparency and use transparency_function.
            transparency_function: One of PyVista's opacity transfer functions (https://docs.pyvista.org/version/stable/examples/02-plot/opacity.html#transfer-functions)
            scalar_warp: If true, warp the mesh proportional to its scalars.
        """
        if self.state.render_colormap != colormap:
            self.state.render_colormap = colormap
        if self.state.render_transparency != transparency:
            self.state.render_transparency = transparency
        if self.state.render_transparency_function != transparency_function:
            self.state.render_transparency_function = transparency_function
        if self.state.render_scalar_warp != scalar_warp:
            self.state.render_scalar_warp = scalar_warp

        if self._mesh is not None and self.data_array is not None:
            self.plot_mesh()

    # -----------------------------------------------------
    # State change callbacks
    # -----------------------------------------------------

    @change("dataset_path")
    def _on_change_dataset_path(self, dataset_path, **kwargs):
        self.set_dataset_path(dataset_path)

    @change("da_active")
    def _on_change_da_active(self, da_active, **kwargs):
        self.set_data_array_active_name(da_active)

    @change("da_active", "da_x", "da_y", "da_z", "da_t", "da_t_index", "da_coordinates")
    def _on_change_da_inputs(
        self, da_active, da_x, da_y, da_z, da_t, da_t_index, da_coordinates, **kwargs
    ):
        self.set_data_array_axis_names(x=da_x, y=da_y, z=da_z, t=da_t)
        self.set_data_array_time_index(da_t_index)
        self.set_data_array_coordinates(da_coordinates)
        self.mesh_changed()

    @change("ui_action_name")
    def _on_change_action_name(self, ui_action_name, **kwargs):
        self.state.ui_action_message = None
        if ui_action_name == "Export":
            self.state.state_export = self.export_config(None)

    @change("render_x_scale", "render_y_scale", "render_z_scale")
    def _on_change_render_scales(
        self, render_x_scale, render_y_scale, render_z_scale, **kwargs
    ):
        self.set_render_scales(
            x=int(render_x_scale), y=int(render_y_scale), z=int(render_z_scale)
        )

    @change(
        "render_colormap",
        "render_transparency",
        "render_transparency_function",
        "render_scalar_warp",
    )
    def _on_change_render_options(
        self,
        render_colormap,
        render_transparency,
        render_transparency_function,
        render_scalar_warp,
        **kwargs,
    ):
        self.set_render_options(
            colormap=render_colormap,
            transparency=render_transparency,
            transparency_function=render_transparency_function,
            scalar_warp=render_scalar_warp,
        )

    # -----------------------------------------------------
    # Render Logic
    # -----------------------------------------------------

    def auto_select_coordinates(self) -> None:
        """Automatically assign available coordinates to available axes.
        Automatic assignment is done according to the following expected coordinate names:\n
        X: "x" | "i" | "lon" | "len"\n
        Y: "y" | "j" | "lat" | "width"\n
        Z: "z" | "k" | "depth" | "height"\n
        T: "t" | "time"
        """
        if self.state.da_x or self.state.da_y or self.state.da_z or self.state.da_t:
            # Some coordinates already assigned, don't auto-assign
            return
        state_update = {}
        for coordinate in self.state.da_coordinates:
            name = coordinate["name"].lower()
            for axis, accepted_names in coordinate_auto_selection.items():
                # don't overwrite if already assigned
                if not self.state[axis]:
                    # If accepted name is longer than one letter, look for contains match
                    name_match = [
                        coordinate["name"]
                        for accepted in accepted_names
                        if (len(accepted) == 1 and accepted == name)
                        or (len(accepted) > 1 and accepted in name)
                    ]
                    if len(name_match) > 0:
                        state_update[axis] = name_match[0]
        if len(state_update) > 0:
            self.state.update(state_update)

    def mesh_changed(self) -> None:
        """Reset and update cached mesh according to current state."""
        if self.dataset is None:
            return
        self._mesh = None

        # Update algorithm all at once
        self.algorithm.data_array = self.dataset[self.state.da_active]
        self.algorithm.slicing = self.state.slicing
        self.algorithm.x = self.state.da_x
        self.algorithm.y = self.state.da_y
        self.algorithm.z = self.state.da_z
        self.algorithm.time = self.state.da_t
        self.algorithm.time_index = self.state.da_t_index

        da = self.data_array
        if self.state.da_active and da is not None:
            total_bytes = da.size * da.dtype.itemsize
        else:
            total_bytes = 0
        exponents_map = {0: "bytes", 1: "KB", 2: "MB", 3: "GB"}
        for exponent in sorted(exponents_map.keys(), reverse=True):
            divisor = 1024**exponent
            suffix = exponents_map[exponent]
            if total_bytes > divisor:
                self.state.da_size = f"{round(total_bytes / divisor)} {suffix}"
                break

        self.state.ui_unapplied_changes = True
        self.state.ui_loading = False

    def plot_mesh(self) -> None:
        """Render current cached mesh in viewer's plotter."""
        self.plotter.clear()
        args = dict(
            cmap=self.state.render_colormap,
            clim=self.algorithm.data_range,
            scalar_bar_args=dict(interactive=True),
        )
        if self.state.render_transparency:
            args["opacity"] = self.state.render_transparency_function

        mesh = self._mesh
        if self.state.render_scalar_warp:
            mesh = mesh.warp_by_scalar()
        self.actor = self.plotter.add_mesh(
            mesh,
            **args,
        )
        self.plotter.view_isometric()
        self.ctrl.push_camera()
        self.ctrl.view_update()

    def reset(self, **kwargs) -> None:
        """Asynchronously reset and update cached mesh and render to viewer's plotter."""
        if not self.state.da_active:
            return
        if self.data_array is None:
            self.mesh_changed()
        self.state.ui_error_message = None
        self.state.ui_loading = True
        self.state.ui_unapplied_changes = False

        async def update_mesh():
            self._mesh = self.algorithm.mesh
            self.plot_mesh()

        def mesh_updated(exception=None):
            with self.state:
                self.state.ui_error_message = (
                    str(exception) if exception is not None else None
                )
                self.state.ui_loading = False

        run_singleton_task(
            update_mesh,
            mesh_updated,
            timeout=self.state.mesh_timeout,
            timeout_message=f"Failed to create mesh in under {self.state.mesh_timeout} seconds. Try reducing data size by slicing.",
        )

    # -----------------------------------------------------
    # Config logic
    # -----------------------------------------------------

    def import_config(self, config_file: typing.Union[str, Path, None]) -> None:
        """Import state from a JSON configuration file.

        Parameters:
            config_file: Can be a dictionary containing state information,
                or a string or Path referring to a JSON file which contains state information.
                For details, see Configuration Files documentation.
        """
        if isinstance(config_file, dict):
            config = config_file
        elif isinstance(config_file, str):
            path = Path(config_file)
            if path.exists():
                config = json.loads(path.read_text())
            else:
                config = json.loads(config_file)
        origin_config = config.get("data_origin")
        array_config = config.get("data_array")
        slices_config = config.get("data_slices")
        ui_config = config.get("ui")

        if not origin_config or not array_config:
            self.state.ui_action_message = "Invalid format of import file."
            return

        self.set_dataset_path(dataset_path=origin_config)
        if "active" in array_config:
            self.set_data_array_active_name(array_config["active"])
        self.set_data_array_axis_names(**array_config)
        if "da_t_index" in array_config:
            self.set_t_index(array_config["t_index"])

        if slices_config:
            new_coordinates = []
            for coordinate in self.state.da_coordinates:
                new_coordinate = coordinate.copy()
                if new_coordinate["name"] in slices_config:
                    start, stop, step = slices_config[new_coordinate["name"]]
                    new_coordinate["start"] = start
                    new_coordinate["stop"] = stop
                    new_coordinate["step"] = step
                new_coordinates.append(new_coordinate)
            self.set_data_array_coordinates(new_coordinates)

        if ui_config:
            for key, value in ui_config.items():
                self.state[f"ui_{key}"] = value

        self.mesh_changed()
        self.state.update({"ui_action_name": None, "ui_selected_config_file": None})

    def export_config(self, config_file: typing.Union[str, Path, None] = None) -> None:
        """Export the current state to a JSON configuration file.

        Parameters:
            config_file: Can be a string or Path representing the destination of the JSON configuration file.
                If None, a dictionary containing the current configuration will be returned.
                For details, see Configuration Files documentation.
        """
        config = {}
        config["data_origin"] = self.state.dataset_path
        config["data_array"] = {"active": self.state.da_active}

        for axis in ["x", "y", "z", "t"]:
            if self.state[f"da_{axis}"]:
                config["data_array"][axis] = self.state[f"da_{axis}"]
        config["data_array"]["t_index"] = self.state.da_t_index

        da_coordinates = self.state.da_coordinates
        for coordinate in da_coordinates:
            if coordinate.get("name") != self.state.da_t and (
                coordinate.get("start")
                or coordinate.get("stop")
                or coordinate.get("step")
            ):
                if "data_slices" not in config:
                    config["data_slices"] = {}
                coordinate_slice = [
                    coordinate.get("start", 0),
                    coordinate.get("stop", -1),
                    coordinate.get("step", 1),
                ]
                config["data_slices"][coordinate["name"]] = coordinate_slice

        for state_var in ["main_drawer", "axis_drawer", "expanded_coordinates"]:
            if "ui" not in config:
                config["ui"] = {}
            config["ui"][state_var] = self.state[f"ui_{state_var}"]

        if config_file:
            Path(config_file).write_text(json.dumps(config))
        else:
            return config
