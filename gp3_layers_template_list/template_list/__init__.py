# GPLv3 License
# Copyright (C) 2024 WerwacK
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.props import BoolProperty

from .config_icons import initGlobalVariables, releaseGlobalVariables
from . import ui_layersGrpsTemplateList
from . import class_LayerTree
from . import ui_layerTreeItemList
from . import layers_callbacks
from . import active_object_callbacks
from . import layerTree_operators
from . import ui_layerTree_right_click_menu
from . import layers_operators


def register():
    initGlobalVariables()

    class_LayerTree.register()
    ui_layerTreeItemList.register()
    ui_layersGrpsTemplateList.register()
    layers_callbacks.register()
    active_object_callbacks.register()
    layerTree_operators.register()
    ui_layerTree_right_click_menu.register()
    layers_operators.register()

    bpy.types.WindowManager.Wk_GP_LayerTreeUseCustomProps = BoolProperty(default=False)


def unregister():
    del bpy.types.WindowManager.Wk_GP_LayerTreeUseCustomProps

    layers_operators.unregister()
    ui_layerTree_right_click_menu.unregister()
    layerTree_operators.unregister()
    active_object_callbacks.unregister()
    ui_layersGrpsTemplateList.unregister()
    layers_callbacks.unregister()
    ui_layerTreeItemList.unregister()
    class_LayerTree.unregister()

    releaseGlobalVariables()


# if __name__ == "__main__":
#     register()
