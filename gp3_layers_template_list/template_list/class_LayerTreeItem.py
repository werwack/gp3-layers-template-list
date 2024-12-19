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
WkLayerTreeItem class
"""


import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty


class WkLayerTreeItem(PropertyGroup):
    def initialize(self):
        self.layerOrGroup = None

    # the default value defined here is used instead of the default set in the property
    def _get_name(self):
        val = self.get("name", "-")
        # wkip to change
        gp = bpy.context.object
        layerOrGp = self.getGpLayerOrGpFromPt(gp)
        if layerOrGp is not None:
            val = layerOrGp.name
        return val

    def _set_name(self, value):
        # wkip to change
        gp = bpy.context.object
        layerOrGp = self.getGpLayerOrGpFromPt(gp)
        if layerOrGp is not None:
            layerOrGp.name = value
            self["name"] = layerOrGp.name
        else:
            self["name"] = "error"

    name: StringProperty(
        name="Name",
        get=_get_name,
        set=_set_name,
        default="",
    )

    # https://docs.blender.org/api/4.3/bpy.types.GreasePencilLayer.html#bpy.types.GreasePencilLayer

    layerOrGroupPt: StringProperty(name="layerOrGroupPt", default="-")

    # "GreasePencilLayer" or "GreasePencilLayerGroup"
    type: StringProperty(name="type", default="-")

    def isLayer(self):
        return "GreasePencilLayer" == self.type

    depth: IntProperty(name="type", description="Depht of the item in the tree hierarchy (0: at root level)", default=0)
    numChildren: IntProperty(name="Num Children", default=0)

    # custom properties
    flag: StringProperty(name="Flag", default="")
    expanded: BoolProperty(name="Expanded", default=True)
    # colorTag: StringProperty(name="Color", default="")
    # see https://projects.blender.org/blender/blender/pulls/129378/files
    colorTag: EnumProperty(
        name="Color Tag",
        description="",
        # items=(
        #     ("LAYERGROUP_COLOR_NONE", "NONE", "ICON_X", "Set Default icon", ""),
        #     ("LAYERGROUP_COLOR_01", "COLOR1", "ICON_LAYERGROUP_COLOR_01", "Color tag 1", ""),
        #     ("LAYERGROUP_COLOR_02", "COLOR2", "ICON_LAYERGROUP_COLOR_02", "Color tag 2", ""),
        #     ("LAYERGROUP_COLOR_03", "COLOR3", "ICON_LAYERGROUP_COLOR_03", "Color tag 3", ""),
        #     ("LAYERGROUP_COLOR_04", "COLOR4", "ICON_LAYERGROUP_COLOR_04", "Color tag 4", ""),
        #     ("LAYERGROUP_COLOR_05", "COLOR5", "ICON_LAYERGROUP_COLOR_05", "Color tag 5", ""),
        #     ("LAYERGROUP_COLOR_06", "COLOR6", "ICON_LAYERGROUP_COLOR_06", "Color tag 6", ""),
        #     ("LAYERGROUP_COLOR_07", "COLOR7", "ICON_LAYERGROUP_COLOR_07", "Color tag 7", ""),
        #     ("LAYERGROUP_COLOR_08", "COLOR8", "ICON_LAYERGROUP_COLOR_08", "Color tag 8", ""),
        # ),
        items=(
            ("LAYERGROUP_COLOR_NONE", "NONE", "Set Default icon"),
            ("LAYERGROUP_COLOR_01", "COLOR1", "Color tag 1"),
            ("LAYERGROUP_COLOR_02", "COLOR2", "Color tag 2"),
            ("LAYERGROUP_COLOR_03", "COLOR3", "Color tag 3"),
            ("LAYERGROUP_COLOR_04", "COLOR4", "Color tag 4"),
            ("LAYERGROUP_COLOR_05", "COLOR5", "Color tag 5"),
            ("LAYERGROUP_COLOR_06", "COLOR6", "Color tag 6"),
            ("LAYERGROUP_COLOR_07", "COLOR7", "Color tag 7"),
            ("LAYERGROUP_COLOR_08", "COLOR8", "Color tag 8"),
        ),
        default="LAYERGROUP_COLOR_NONE",
        options=set(),
    )

    def getParentLayerTree(self):
        return bpy.context.window_manager.Wk_GPSceneLayerTree

    def getGpLayerOrGpFromPt(self, editedGpencil):
        if "GreasePencilLayer" == self.type:
            for layer in editedGpencil.data.layers:
                if str(layer.as_pointer()) == self.layerOrGroupPt:
                    return layer
        else:
            for layer in editedGpencil.data.layer_groups:
                if str(layer.as_pointer()) == self.layerOrGroupPt:
                    return layer
        return None

    def getLayerFromPt(self, editedGpencil):
        for layer in editedGpencil.data.layers:
            if str(layer.as_pointer()) == self.layerOrGroupPt:
                return layer
        return None

    def getGpLayerFromPt(self, editedGpencil):
        for layerGp in editedGpencil.data.layer_groups:
            if str(layerGp.as_pointer()) == self.layerOrGroupPt:
                return layerGp
        return None

    def getParentGroupItem(self, withIndexDict=False):
        """Return the layer group item of this item, or None if the parent is the root or not found"""
        itemInfoDict = dict()

        layerTree = self.getParentLayerTree()
        parentsList = list()
        parentItem = None
        # parentsList.append(None)

        # def _getParentGroupItemRec(layerOrGpItem):
        #     for item in layerOrGpItem.layerTreeItems:
        #         if item == self:
        #             return parentItem
        #         if not item.isLayer():
        #             return _getParentGroupItemRec()

        # _getParentGroupItemRec(layerTree)
        # return layerTree

        # layers at root have a depht of 1
        previousDepth = 1
        for item in layerTree.layerTreeItems:
            if item.depth < previousDepth:
                del parentsList[(item.depth - 1) :]
            if item == self:
                if len(parentsList):
                    parentItem = parentsList[-1]
                    break
                    # return parentsList[-1]
                else:
                    return None
            if not item.isLayer():
                parentsList.append(item)
            previousDepth = item.depth

        if withIndexDict:
            itemInfoDict["parentItem"] = parentItem

            return itemInfoDict

        return parentItem

    def getContainedItems(self):
        containedItems = list()
        layerTree = self.getParentLayerTree()

        itemIndex = 0
        # item = layerTree.layerTreeItems[0]
        while layerTree.layerTreeItems[itemIndex] != self and itemIndex < len(layerTree.layerTreeItems):
            itemIndex += 1

        # we skip the current item
        itemIndex += 1

        if itemIndex < len(layerTree.layerTreeItems):
            while itemIndex < len(layerTree.layerTreeItems) and self.depth < int(layerTree.layerTreeItems[itemIndex].depth):
                containedItems.append(layerTree.layerTreeItems[itemIndex])
                itemIndex += 1

        return containedItems


## registering is done in layerTree
