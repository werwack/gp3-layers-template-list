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
UI for the snapshots - in the snaptshots list component
"""

import bpy
from bpy.types import UIList
from . import config_icons

#############
# LayerTreeItem
#############


class WKSL_UL_LayerTreeItem_Items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        drawLayerTreeItem(context, layout, data, item, icon, active_data, active_propname, index)


def drawLayerTreeItem(context, layout, data, item, icon, active_data, active_propname, index):
    # layout.label("my layer item")

    # if self.gpIsStoryboardFrame:
    # editedGpencil = props.getSelectedShotStoryboardFrame()
    editedGpencil = context.active_object
    layerOrGp = item.getGpLayerOrGpFromPt(editedGpencil)
    isLayer = item.type == "GreasePencilLayer"

    def _drawHierarchyIcons(layout):
        row = layout.row(align=True)

        for i in range(1, item.depth):
            subRow = row.row(align=True)
            subRow.ui_units_x = 0.7
            # subRow.label(text="  |")
            # subRow.label(icon="THREE_DOTS")
            iconExplorer = config_icons.icons_col["layer_vertical_line_32"]
            subRow.label(icon_value=iconExplorer.icon_id)

        if isLayer:
            subRow = row.row(align=True)
            subRow.ui_units_x = 0.74
            subRow.label(icon="BLANK1")

        else:
            subRow = row.row(align=True)
            if 0 == item.numChildren:
                subRow.ui_units_x = 0.74
                subRow.label(icon="BLANK1")
            else:
                # if layerOrGp.isExpanded:
                if True:
                    subRow.ui_units_x = 0.74
                    subRow.label(text="", icon="DOWNARROW_HLT")
                else:
                    subRow.label(icon="RIGHTARROW")
            layout.separator(factor=0.8)

    # layout.label(text=item.name)
    # layer = item["layerOrGroup"]

    row = layout.row(align=True)

    _drawHierarchyIcons(row)

    typeRow = row.row(align=True)
    typeRow.ui_units_x = 1
    if isLayer:
        typeRow.label(text="", icon="OUTLINER_DATA_GP_LAYER")

    else:
        typeRow.label(text="", icon="GREASEPENCIL_LAYER_GROUP")

    row.separator(factor=0.4)
    # use a prop and not a label to makeit editable by double-click
    row.prop(layerOrGp, "name", text="", emboss=False)
    # row.label(text=layerOrGp.name)

    ########################
    # add your custom code here (for instance)
    if bpy.context.window_manager.Wk_GP_LayerTreeUseCustomProps:
        subRow = row.row(align=False)
        subRow.alignment = "RIGHT"
        subRow.label(text="My Prop")
        subRow.separator(factor=1.0)

    ########################

    subRow = row.row(align=True)
    if isLayer:
        # NOTE: if a specific icon has to be provided, note that use_masks automatically takes the icon BEFORE the one provided when True
        # subRow.prop(layerOrGp, "use_masks", text="", icon="CLIPUV_HLT" if layerOrGp.use_masks else "CLIPUV_HLT", emboss=False)
        subRow.prop(layerOrGp, "use_masks", text="", emboss=False)
    else:
        # mask icons are not provided by default for groups
        # CLIPUV_HLT CLIPUV_DEHLT
        subRow.prop(layerOrGp, "use_masks", text="", icon="CLIPUV_DEHLT" if layerOrGp.use_masks else "CLIPUV_HLT", emboss=False)
    subRow.prop(layerOrGp, "use_onion_skinning", text="", emboss=False)
    subRow.prop(layerOrGp, "hide", text="", emboss=False)
    subRow.prop(layerOrGp, "lock", text="", emboss=False)


classes = (WKSL_UL_LayerTreeItem_Items,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
