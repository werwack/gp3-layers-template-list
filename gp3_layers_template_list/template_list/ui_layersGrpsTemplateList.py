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
Layers and layer groups panel
"""

import bpy
from bpy.types import Panel

from .layerTree_functions import getActiveLayerOrGp


class GpLayersAndGroupsPanel(Panel):
    bl_idname = "WKSL_PT_gplayersandgroupspanel"
    bl_label = "GP Layers and Groups List"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GP Layers List"

    def draw(self, context):
        layout = self.layout

        if context.object is None or "GREASEPENCIL" != context.object.type:
            layout.label(text="Pick a Grease Pencil Object")
            return

        grease_pencil_obj = context.object
        grease_pencil = grease_pencil_obj.data

        activeLayerOrGp = getActiveLayerOrGp(grease_pencil_obj)
        isLayer = "GreasePencilLayer" == type(activeLayerOrGp).__name__

        layout.label(text=f"Grease Pencil Object: {grease_pencil_obj.name}")

        row = layout.row()
        col = row.column()

        layer_rows = 6

        uiListType = "WKSL_UL_LayerTreeItem_Items"
        col.template_list(
            uiListType,
            "",
            bpy.context.window_manager.Wk_GPSceneLayerTree,
            "layerTreeItems",
            bpy.context.window_manager.Wk_GPSceneLayerTree,
            "selected_layerTreeItem_index",
            rows=layer_rows,
            sort_reverse=False,
            sort_lock=True,
        )

        layer = grease_pencil.layers.active
        is_layer_active = layer is not None
        is_group_active = grease_pencil.layer_groups.active is not None

        col = row.column()
        sub = col.column(align=True)
        sub.operator_context = "EXEC_DEFAULT"
        sub.operator("grease_pencil.layer_add", icon="ADD", text="")
        sub.operator("grease_pencil.layer_group_add", icon="NEWFOLDER", text="")
        sub.separator()

        if is_layer_active:
            sub.operator("grease_pencil.layer_remove", icon="REMOVE", text="")
        if is_group_active:
            sub.operator("grease_pencil.layer_group_remove", icon="REMOVE", text="").keep_children = True

        sub.separator()
        sub.menu("GREASE_PENCIL_MT_grease_pencil_add_layer_extra", icon="DOWNARROW_HLT", text="")

        col.separator()
        sub = col.column(align=True)
        sub.operator("grease_pencil.layer_move", icon="TRIA_UP", text="").direction = "UP"
        sub.operator("grease_pencil.layer_move", icon="TRIA_DOWN", text="").direction = "DOWN"

        # experimental
        # col.separator()
        # sub = col.column(align=True)
        # sub.operator_context = "INVOKE_DEFAULT"
        # sub.operator("wk.movelayerorgrp", icon="TRIA_UP", text="").direction = "UP"
        # sub.operator("wk.movelayerorgrp", icon="TRIA_DOWN", text="").direction = "DOWN"

        col.separator()
        sub = col.column(align=True)
        # copy: COPYDOWN
        # cut: PASTEFLIPUP
        # paste: PASTEDOWN
        sub.operator_context = "INVOKE_DEFAULT"
        sub.operator("wk.cutlayersubtree", icon="PASTEFLIPUP", text="")
        sub.operator("wk.pastelayersubtree", icon="PASTEDOWN", text="")

        # for customization ########################
        layout.separator(factor=1.0)
        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("wk.displaycustomprops")

        # for debug only ########################
        # hide this button in your onw implementation
        # display a button that will allow you to manually update the layer tree structure
        layout.separator(factor=1.0)
        row = layout.row(align=True)
        row.label(text="For Debug Only:")
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("wk.refreshlayertree", icon="FILE_REFRESH", text="Refresh Layer Tree").gpObjName = grease_pencil_obj.name


_classes = (GpLayersAndGroupsPanel,)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
