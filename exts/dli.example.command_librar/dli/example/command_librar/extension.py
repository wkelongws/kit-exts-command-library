import omni.ext
import omni.ui as ui
import omni.kit.commands # New
import omni.usd # New
from typing import List # New


def get_selection() -> List[str]:
    """Get the list of currently selected prims"""
    return omni.usd.get_context().get_selection().get_selected_prim_paths()

class ScaleIncrement(omni.kit.commands.Command):
    def __init__(self):
        self.stage = omni.usd.get_context().get_stage()

    def set_scale(self, undo: bool=False):
        prim_paths = get_selection()
        for path in prim_paths:
            print(path)
            prim = self.stage.GetPrimAtPath(path)
            old_scale = prim.GetAttribute('xformOp:scale').Get()
            new_scale = tuple(x + 1 for x in old_scale)
            if undo:
                new_scale = tuple(x - 1 for x in old_scale)
            prim.GetAttribute('xformOp:scale').Set(new_scale)

    def do(self):
        self.set_scale()

    def undo(self):
        self.set_scale(True)


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[dli.example.command_librar] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class DliExampleCommand_librarExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[dli.example.command_librar] dli example command_librar startup")

        self._count = 0

        self._window = ui.Window("command window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("")


                def on_click():
                    self._count += 1
                    label.text = f"count: {self._count}"

                def on_reset():
                    self._count = 0
                    label.text = "empty"

                on_reset()

                with ui.HStack():
                    ui.Button("Add", clicked_fn=on_click)
                    ui.Button("Reset", clicked_fn=on_reset)

    def on_shutdown(self):
        print("[dli.example.command_librar] dli example command_librar shutdown")
