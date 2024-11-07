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
Layer Tree operators
"""


import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from .layerTree_functions import getActiveLayerOrGp


class Wk_OT_LayerTreeAdd(Operator):
    bl_idname = "wk.layertree_add"
    bl_label = "Add New LayerTree..."
    bl_description = "Add a new layertree at current time to the specified shot"
    bl_options = {"REGISTER", "UNDO"}

    gpObjName: StringProperty(name="grease Pencil Object Name", default="", options={"SKIP_SAVE"})

    newLayerName: StringProperty(name="New Layer Name", default="", options={"SKIP_SAVE"})

    def invoke(self, context, event):
        scene = context.scene

        gp = None
        if "" == self.gpObjName:
            gp = context.object
        else:
            if self.gpObjName in scene.objects:
                gp = scene.objects[self.gpObjName]

        # layers = bpy.data.objects['MyPencil'].data.layers
        if gp and "GREASEPENCIL" == gp.type:
            print(f"Adding new layer to object {self.gpObjName}")

            use_keyframe_insert_auto = scene.tool_settings.use_keyframe_insert_auto
            scene.tool_settings.use_keyframe_insert_auto = False
            currentObjectMode = "OBJECT"
            if "OBJECT" != gp.mode:
                # currentObjectMode = utils.getCurrentObjectMode(context)
                currentObjectMode = context.object.mode
                # context.object.mode = "OBJECT"
                bpy.ops.object.mode_set(mode="OBJECT")

            # get active layer index in layers
            activeLayerOrGp = getActiveLayerOrGp(gp)
            isLayer = "GreasePencilLayer" == type(activeLayerOrGp).__name__
            activeLayerInd = 0
            while activeLayerInd < len(gp.data.layers) and gp.data.layers[activeLayerInd] != activeLayerOrGp:
                activeLayerInd += 1

            newLayer = gp.data.layers.new(name="Layer")
            if "" != self.newLayerName:
                newLayer.name = self.newLayerName

            if currentObjectMode != "OBJECT":
                bpy.ops.object.mode_set(mode=currentObjectMode)
            if use_keyframe_insert_auto:
                scene.tool_settings.use_keyframe_insert_auto = use_keyframe_insert_auto

            if isLayer:
                # our layer is at the end of layers, we move it up to the active one

                # numMoves = len(gp.data.layers) - activeLayerInd
                numMoves = activeLayerInd
                for i in range(0, numMoves):
                    gp.data.layers.move(gp.data.layers[len(gp.data.layers) - i - 1], "DOWN")

        # reorder: https://blender.stackexchange.com/questions/261516/changing-grease-pencil-layer-order-in-python

        # "GreasePencilLayer" or "GreasePencilLayerGroup"
        # bpy.context.window_manager.Wk_GPSceneLayerTree.addlayerTreeItem(newLayer.name, "GreasePencilLayer", newLayer, gp)
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(gp)

        return {"FINISHED"}


class Wk_OT_RefreshLayerTree(Operator):
    bl_idname = "wk.refreshlayertree"
    bl_label = "Refresh LayerTree..."
    bl_description = "Refresh a new layertree at current time to the specified shot"
    bl_options = {"REGISTER", "UNDO"}

    gpObjName: StringProperty(name="grease Pencil Object Name", default="", options={"SKIP_SAVE"})

    def invoke(self, context, event):
        scene = context.scene

        gp = None
        if "" == self.gpObjName:
            gp = context.object
        else:
            if self.gpObjName in scene.objects:
                gp = scene.objects[self.gpObjName]

        # layers = bpy.data.objects['MyPencil'].data.layers
        if gp and "GREASEPENCIL" == gp.type:
            print(f"Refreshing layer tree for {self.gpObjName}")

        # reorder: https://blender.stackexchange.com/questions/261516/changing-grease-pencil-layer-order-in-python

        # "GreasePencilLayer" or "GreasePencilLayerGroup"
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(gp)

        return {"FINISHED"}


class Wk_OT_DisplayCustomProps(Operator):
    bl_idname = "wk.displaycustomprops"
    bl_label = "Display Custom Properties"
    bl_description = "Display sample custom properties in the layer and layer group items"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        bpy.context.window_manager.Wk_GP_LayerTreeUseCustomProps = not bpy.context.window_manager.Wk_GP_LayerTreeUseCustomProps
        return {"FINISHED"}


_classes = (Wk_OT_RefreshLayerTree, Wk_OT_LayerTreeAdd, Wk_OT_DisplayCustomProps)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
