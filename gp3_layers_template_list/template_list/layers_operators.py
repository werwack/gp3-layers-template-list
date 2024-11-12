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
from .utils_gp3 import isLayer
from .layers_color import getColorTag


class Wk_OT_DisplayCustomProps(Operator):
    bl_idname = "wk.displaycustomprops"
    bl_label = "Display Custom Properties"
    bl_description = "Display sample custom properties in the layer and layer group items"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        bpy.context.window_manager.Wk_GP_LayerTreeUseCustomProps = not bpy.context.window_manager.Wk_GP_LayerTreeUseCustomProps
        return {"FINISHED"}


class Wk_OT_Movelayerorgroup(Operator):
    bl_idname = "wk.movelayerorgrp"
    bl_label = "Reorder Layer"
    bl_description = "Move active element up or down in the layers hierarchy"
    bl_options = {"INTERNAL", "UNDO"}

    direction: StringProperty(name="Move direction", description="Can be UP or DOWN", default="", options={"SKIP_SAVE"})
    action: StringProperty(default="DO_NOTHING", options={"SKIP_SAVE"})

    @classmethod
    def description(self, context, properties):
        descr = "Move active element up or down in the layers hierarchy"
        if "" != properties.direction:
            dirTxt = ""
            if "UP" == properties.direction:
                dirTxt = "above"
            elif "DOWN" == properties.direction:
                dirTxt = "below"
            descr += f"\n+ Shift: If the element right {dirTxt} the active layer is a group, then the layer is moved into it"

        return descr

    @classmethod
    def poll(cls, context):
        return context.object is not None and "GREASEPENCIL" == context.object.type

    def invoke(self, context, event):
        self.action = "SAME_LEVEL"

        if not event.ctrl and not event.shift and not event.alt:
            self.action = "SAME_LEVEL"
        elif not event.ctrl and event.shift and not event.alt:
            self.action = "CHANGE_LEVEL"

        if "DO_NOTHING" == self.action:
            return {"CANCELLED"}
        return self.execute(context)

    def execute(self, context):
        scene = context.scene

        gp = context.object
        # gp = None
        # if "" == self.gpObjName:
        #     gp = context.object
        # else:
        #     if self.gpObjName in scene.objects:
        #         gp = scene.objects[self.gpObjName]

        # layers = bpy.data.objects['MyPencil'].data.layers
        if gp and "GREASEPENCIL" == gp.type:
            layerTree = bpy.context.window_manager.Wk_GPSceneLayerTree

            activeLayerOrGpItem = layerTree.getLayerTreeSelectedItem()

            activeLayerOrGp = getActiveLayerOrGp(gp)

            if activeLayerOrGp is None:
                return {"FINISHED"}

            # layerTree = selItem.getParentLayerTree()
            selItem = layerTree.getLayerTreeSelectedItem()

            if "SAME_LEVEL" == self.action:
                pass

                # # technic 1: with layer tree items
                # # get parent group
                # parentItem = activeLayerOrGpItem.getParentGroupItem()
                # # itemInfoDict = activeLayerOrGpItem.getParentGroupItem(withIndexDict=True)
                # # parentItem = itemInfoDict.parentGpItem

                # if parentItem is None:
                #     parentName = "NONE"
                # else:
                #     parentName = parentItem.name
                # print(f"Parent of {selItem.name} is {parentName}")
                # # get child ind

                ##### ok, working
                # technic 2: with layers directly
                parentGp = activeLayerOrGp.parent_group
                if parentGp is not None:
                    print(f"Parent of {selItem.name} is {parentGp.name}")
                if isLayer(activeLayerOrGp):
                    gp.data.layers.move(activeLayerOrGp, self.direction)
                else:
                    gp.data.layer_groups.move(activeLayerOrGp, self.direction)

            else:
                pass

            bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(gp)

        return {"FINISHED"}


class Wk_OT_RemoveLayerOrGpFromGroup(Operator):
    bl_idname = "wk.removelayerorgpfromgroup"
    bl_label = "Remove From Group..."
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    gpObjName: StringProperty(name="grease Pencil Object Name", default="", options={"SKIP_SAVE"})

    def invoke(self, context, event):
        # NOTE: To do
        # scene = context.scene

        # gp = None
        # if "" == self.gpObjName:
        #     gp = context.object
        # else:
        #     if self.gpObjName in scene.objects:
        #         gp = scene.objects[self.gpObjName]

        # # layers = bpy.data.objects['MyPencil'].data.layers
        # if gp and "GREASEPENCIL" == gp.type:
        #     print(f"Cut layer tree for {self.gpObjName}")
        #     layerTree = bpy.context.window_manager.Wk_GPSceneLayerTree

        #     activeLayerOrGpItem = layerTree.getLayerTreeSelectedItem()
        #     # activeLayerOrGp = getActiveLayerOrGp(gp)
        #     if activeLayerOrGpItem.isLayer():
        #         activeLayerOrGpItem.flag = "CUT"

        return {"FINISHED"}


class Wk_OT_SetLayerOrGpColorTag(Operator):
    bl_idname = "wk.setlayerorgpcolortag"
    bl_label = "Color Tag"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    # name in Blender: layer_group_color_tag

    gpObjName: StringProperty(name="grease Pencil Object Name", default="", options={"SKIP_SAVE"})
    colorTag: StringProperty(name="Color Tag", default="", options={"SKIP_SAVE"})

    def invoke(self, context, event):
        # NOTE: To do
        scene = context.scene

        gp = None
        if "" == self.gpObjName:
            gp = context.object
        else:
            if self.gpObjName in scene.objects:
                gp = scene.objects[self.gpObjName]

        # # layers = bpy.data.objects['MyPencil'].data.layers
        if gp and "GREASEPENCIL" == gp.type:
            print(f"Cut layer tree for {self.gpObjName}")
            layerTree = bpy.context.window_manager.Wk_GPSceneLayerTree

            activeLayerOrGpItem = layerTree.getLayerTreeSelectedItem()
            # activeLayerOrGp = getActiveLayerOrGp(gp)
            if not activeLayerOrGpItem.isLayer():
                activeLayerOrGpItem.colorTag = self.colorTag
                bpy.ops.grease_pencil.layer_group_color_tag(color_tag=getColorTag(self.colorTag))

        return {"FINISHED"}


_classes = (
    Wk_OT_DisplayCustomProps,
    Wk_OT_Movelayerorgroup,
    Wk_OT_RemoveLayerOrGpFromGroup,
    Wk_OT_SetLayerOrGpColorTag,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
