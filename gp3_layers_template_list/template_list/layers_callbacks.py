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


##########################################
# function called when properthe layers from py.types.GreasePencilv3 changes:
def layers_changed_callback():
    txt = ""
    ob = bpy.context.object
    if ob and ob.type == "GREASEPENCIL":
        txt = f": lenght: {len(ob.data.layers)}"
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(ob)
    print("Layers changed" + txt)


def subscribe_layers_content():
    subscribe_to = (bpy.types.GreasePencilv3, "layers")
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=bpy.types.GreasePencilv3,
        # Args passed to callback function (tuple)
        args=(),
        # Callback function for property update
        notify=layers_changed_callback,
        options={"PERSISTENT"},
    )


##########################################
# function called when properthe layer_groups from py.types.GreasePencilv3 changes:
def layer_groups_changed_callback():
    txt = ""
    ob = bpy.context.object
    if ob and ob.type == "GREASEPENCIL":
        txt = f": lenght: {len(ob.data.layer_groups)}"
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(ob)
    print("Layer groups changed" + txt)


def subscribe_layer_groups_content():
    subscribe_to = (bpy.types.GreasePencilv3, "layer_groups")
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=bpy.types.GreasePencilv3,
        # Args passed to callback function (tuple)
        args=(),
        # Callback function for property update
        notify=layer_groups_changed_callback,
        options={"PERSISTENT"},
    )


##########################################
# function called when properthe layers from py.types.GreasePencilv3 changes:
def active_layer_changed_callback():
    txt = ""
    ob = bpy.context.object
    if ob and ob.type == "GREASEPENCIL":
        if ob.data.layers.active is not None:
            txt = f": name: {ob.data.layers.active.name}"
        else:
            txt = ": name: None"
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(ob)
    print("Active layer changed" + txt)


def subscribe_layer_active():
    subscribe_to = (bpy.types.GreasePencilv3Layers, "active")
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=bpy.types.GreasePencilv3,
        # Args passed to callback function (tuple)
        args=(),
        # Callback function for property update
        notify=active_layer_changed_callback,
        options={"PERSISTENT"},
    )


##########################################
# function called when properthe layer_groups from py.types.GreasePencilv3 changes:
def active_layer_group_changed_callback():
    txt = ""
    ob = bpy.context.object
    if ob and ob.type == "GREASEPENCIL":
        if ob.data.layer_groups.active is not None:
            txt = f": name: {ob.data.layer_groups.active.name}"
        else:
            txt = ": name: None"
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(ob)
    print("Active layer group changed" + txt)


def subscribe_layer_group_active():
    subscribe_to = (bpy.types.GreasePencilv3LayerGroup, "active")
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=bpy.types.GreasePencilv3,
        # Args passed to callback function (tuple)
        args=(),
        # Callback function for property update
        notify=active_layer_group_changed_callback,
        options={"PERSISTENT"},
    )


##########################################


def register():
    print("Registering layer subscribtions")
    # Subscribe for register
    bpy.app.timers.register(subscribe_layers_content, first_interval=1)
    bpy.app.timers.register(subscribe_layer_groups_content, first_interval=1)

    bpy.app.timers.register(subscribe_layer_active, first_interval=1)
    bpy.app.timers.register(subscribe_layer_group_active, first_interval=1)


def unregister():
    if bpy.app.timers.is_registered(subscribe_layers_content):
        bpy.app.timers.unregister(subscribe_layers_content)
    if bpy.app.timers.is_registered(subscribe_layer_groups_content):
        bpy.app.timers.unregister(subscribe_layer_groups_content)

    if bpy.app.timers.is_registered(subscribe_layer_active):
        bpy.app.timers.unregister(subscribe_layer_active)
    if bpy.app.timers.is_registered(subscribe_layer_group_active):
        bpy.app.timers.unregister(subscribe_layer_group_active)
