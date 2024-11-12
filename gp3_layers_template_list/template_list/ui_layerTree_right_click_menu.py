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

"""
Items added to the right click menu to extend the functionalities of some operators
"""

import bpy
from .layers_color import drawColorsRow


def draw_wksl_layer_groups_menu_items(self, context):
    prop = getattr(context, "button_prop", None)
    if prop is None:
        print("context.button_prop: None")
    if prop is not None:
        print(f"context.button_prop: {context.button_prop}")
        print(f"button_prop: {prop.__class__.__name__}")
        print(f"button_prop: {prop.name}")
        print(f"button_prop identifier: {prop.identifier}")
    if prop is not None and "selected_layerTreeItem_index" == prop.identifier:
        layout = self.layout

        layerTree = bpy.context.window_manager.Wk_GPSceneLayerTree
        activeLayerOrGpItem = layerTree.getLayerTreeSelectedItem()
        # activeLayerOrGp = getActiveLayerOrGp(gp)
        if not activeLayerOrGpItem.isLayer():
            layout.separator()
            layout.operator("grease_pencil.layer_group_remove", text="Delete Group").keep_children = False
            layout.operator("grease_pencil.layer_group_remove", text="Ungroup").keep_children = True
            layout.operator("grease_pencil.layer_merge", text="Merge Group").mode = "GROUP"

            # layout.separator()
            # row = layout.row(align=True)
            # row.operator_enum("grease_pencil.layer_group_color_tag", "color_tag", icon_only=True)

            # from Blender
            # layout.separator()
            # row = layout.row(align=True)
            # row.operator_enum("grease_pencil.layer_group_color_tag", "color_tag", icon_only=True)

            # custom
            layout.separator()
            drawColorsRow(layout)


def register():
    bpy.types.UI_MT_button_context_menu.append(draw_wksl_layer_groups_menu_items)


def unregister():
    bpy.types.UI_MT_button_context_menu.remove(draw_wksl_layer_groups_menu_items)
