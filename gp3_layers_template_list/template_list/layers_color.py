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


def getColorIcon(colorTag):
    icon = colorTag
    if "LAYERGROUP_COLOR_NONE" == colorTag:
        icon = "GREASEPENCIL_LAYER_GROUP"
    return icon
    # LAYERGROUP_COLOR_08


def getColorTag(colorTag):
    match colorTag:
        case "LAYERGROUP_COLOR_NONE":
            return "NONE"
        case "LAYERGROUP_COLOR_01":
            return "COLOR1"
        case "LAYERGROUP_COLOR_02":
            return "COLOR2"
        case "LAYERGROUP_COLOR_03":
            return "COLOR3"
        case "LAYERGROUP_COLOR_04":
            return "COLOR4"
        case "LAYERGROUP_COLOR_05":
            return "COLOR5"
        case "LAYERGROUP_COLOR_06":
            return "COLOR6"
        case "LAYERGROUP_COLOR_07":
            return "COLOR7"
        case "LAYERGROUP_COLOR_08":
            return "COLOR8"
    return "NONE"


def drawColorsRow(layout):
    pass
    row = layout.row(align=True)
    # row.separator(factor=3.5)
    row.label(text="")
    row.operator("wk.setlayerorgpcolortag", icon="PANEL_CLOSE", text="").colorTag = "LAYERGROUP_COLOR_NONE"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_01", text="").colorTag = "LAYERGROUP_COLOR_01"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_02", text="").colorTag = "LAYERGROUP_COLOR_02"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_03", text="").colorTag = "LAYERGROUP_COLOR_03"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_04", text="").colorTag = "LAYERGROUP_COLOR_04"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_05", text="").colorTag = "LAYERGROUP_COLOR_05"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_06", text="").colorTag = "LAYERGROUP_COLOR_06"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_07", text="").colorTag = "LAYERGROUP_COLOR_07"
    row.operator("wk.setlayerorgpcolortag", icon="LAYERGROUP_COLOR_08", text="").colorTag = "LAYERGROUP_COLOR_08"
