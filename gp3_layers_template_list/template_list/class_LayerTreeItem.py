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
from bpy.types import PropertyGroup
from bpy.props import StringProperty, IntProperty


class WkLayerTreeItem(PropertyGroup):
    def initialize(self):
        self.layerOrGroup = None

    name: StringProperty(name="Name", default="")

    # https://docs.blender.org/api/4.3/bpy.types.GreasePencilLayer.html#bpy.types.GreasePencilLayer

    layerOrGroupPt: StringProperty(name="layerOrGroupPt", default="-")

    # "GreasePencilLayer" or "GreasePencilLayerGroup"
    type: StringProperty(name="type", default="-")

    def isLayer(self):
        return "GreasePencilLayer" == self.type

    depth: IntProperty(name="type", default=0)
    numChildren: IntProperty(name="Num Children", default=0)

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

    def getGpLayerFromPt(self, editedGpencil):
        for layer in editedGpencil.data.layers:
            if str(layer.as_pointer()) == self.layerOrGroupPt:
                return layer
        return None


## registering is done in layerTree
