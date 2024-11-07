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
Layer Tree class
"""

import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, IntProperty, CollectionProperty

from .class_LayerTreeItem import WkLayerTreeItem
from .layerTree_functions import getLayerTree, getActiveLayerOrGp


class WkLayerTree(PropertyGroup):

    layerTreeItems: CollectionProperty(name="Layer Tree Items", type=WkLayerTreeItem)

    def getItemFromPt(self, layerOrGpPt):
        for item in self.layerTreeItems:
            if str(layerOrGpPt) == item.layerOrGroupPt:
                return item
        return None

    def getItemIndexFromPt(self, layerOrGpPt):
        for i, item in enumerate(self.layerTreeItems):
            if str(layerOrGpPt) == item.layerOrGroupPt:
                return i
        return -1

    # the default value defined here is used instead of the default set in the property
    def _get_selected_layerTreeItem_index(self):
        val = self.get("selected_layerTreeItem_index", -1)

        # if self.selected_layerTreeItem_index < len(self.layerTreeItems):
        if True:
            # wkip to change
            gp = bpy.context.object

            activeLayerOrGp = getActiveLayerOrGp(gp)
            if activeLayerOrGp is not None:
                # print(f"  Active layer or gp in scene is: {activeLayerOrGp.name}")
                activeItemInd = self.getItemIndexFromPt(activeLayerOrGp.as_pointer())
                # print(f"  Active activeItemInd: {activeItemInd}")
                val = activeItemInd
        return val

    def _set_selected_layerTreeItem_index(self, value):
        # wkip to change
        gp = bpy.context.object

        # activeLayerOrGp = getActiveLayerOrGp(gp)
        # activeItemInd = self.getItemIndexFromPt(activeLayerOrGp.as_pointer())
        layerOrGpItem = self.layerTreeItems[value]
        layerOrGp = layerOrGpItem.getGpLayerOrGpFromPt(gp)
        if layerOrGpItem.isLayer():
            gp.data.layers.active = layerOrGp
        else:
            gp.data.layer_groups.active = layerOrGp
        self["selected_layerTreeItem_index"] = value

    def _update_selected_layerTreeItem_index(self, context):
        print("layerOrGp sel ind: ", self.selected_layerTreeItem_index)

        if self.selected_layerTreeItem_index < len(self.layerTreeItems):
            # wkip to change
            gp = context.object
            selItem = self.layerTreeItems[self.selected_layerTreeItem_index]
            layerOrGp = selItem.getGpLayerOrGpFromPt(gp)
            if "GreasePencilLayer" == selItem.type:
                gp.data.layers.active = layerOrGp
            else:
                gp.data.layer_groups.active = layerOrGp

    selected_layerTreeItem_index: IntProperty(
        name="Selected layerTreeItem",
        get=_get_selected_layerTreeItem_index,
        set=_set_selected_layerTreeItem_index,
        # update=_update_selected_layerTreeItem_index,
        default=-1,
    )

    def getLayerTreeSelectedItem(self):
        if -1 != self.selected_layerTreeItem_index:
            return self.layerTreeItems[self.selected_layerTreeItem_index]
        return None

    def addlayerTreeItem(self, name, type, layerOrGrp, gpobj):
        """Args:
        type: "GreasePencilLayer" or "GreasePencilLayerGroup"
        """
        # type(gplayers[0]).__name__

        # item is added at the end of the list
        layerTreeItem = self.layerTreeItems.add()
        layerTreeItem.initialize()
        layerTreeItem.name = name
        print(f"myVar: {layerTreeItem.myVar}")
        layerTreeItem.type = type

        print("list of layer pointers:")
        for layer in gpobj.data.layers:
            print(f"layer {layer.name} pointer: {layer.as_pointer()}")

        layerTreeItem.layerOrGroupPt = str(layerOrGrp.as_pointer())

        if "GreasePencilLayer" == type:
            pass
        else:
            pass

    def refreshlayerTree(self, gpobj):
        pass
        self.layerTreeItems.clear()
        pointersList = getLayerTree(gpobj)

        for pt in pointersList:
            layerTreeItem = self.layerTreeItems.add()
            layerTreeItem.initialize()
            # layerTreeItem.name
            layerTreeItem.layerOrGroupPt = str(pt[0])
            layerTreeItem.type = pt[1]
            layerTreeItem.depth = pt[2]
            layerTreeItem.numChildren = pt[3]


_classes = (
    WkLayerTreeItem,
    WkLayerTree,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.Wk_GPSceneLayerTree = PointerProperty(type=WkLayerTree)


def unregister():
    del bpy.types.WindowManager.Wk_GPSceneLayerTree

    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
