import bpy


##########################################
# function called when context.active_object changed:
def active_object_changed_callback():
    txt = ""
    ob = bpy.context.active_object
    if ob and ob.type == "GREASEPENCIL":
        txt = f": {ob.name}"
        bpy.context.window_manager.Wk_GPSceneLayerTree.refreshlayerTree(ob)
    print("Active object changed" + txt)


# https://blenderartists.org/t/subscribe-to-active-objects-active-material-index/1465192/2
def subscribe_to_active_object():
    # subscribe_to = (bpy.types.Context, "active_object")
    # # subscribe_to = bpy.context.path_resolve("active_object", False)
    # bpy.msgbus.subscribe_rna(
    #     key=subscribe_to,
    #     owner=bpy.context,
    #     # Args passed to callback function (tuple)
    #     args=(bpy.context,),
    #     # Callback function for property update
    #     notify=active_object_changed_callback,
    #     options={"PERSISTENT"},
    # )
    active_object_owner = 123

    # Subscribe to active object changes.
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.LayerObjects, "active"),
        owner=active_object_owner,
        args=(),
        notify=active_object_changed_callback,
    )


##########################################


def register():
    # Subscribe for register
    bpy.app.timers.register(subscribe_to_active_object, first_interval=1)


def unregister():
    pass
    if bpy.app.timers.is_registered(subscribe_to_active_object):
        bpy.app.timers.unregister(subscribe_to_active_object)
