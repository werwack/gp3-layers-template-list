# GP3 Layers Template List

A template list to mimic the layers and layer groups of a Grease Pencil V3 object in Blender 4.3+

In Blender 4.3, many features of the Grease Pencil objects, as well as their internal structure, have considerably changed compared
to the previous versions. The implementaiton is now based on what is called Grease Pencil V3.

Many cool new features have then been introduced, including the ability to have layer groups and a color associated to those layers and groups.

As an add-on developer, you may want to have the layers list displayed in a custom panel, and may want to modify some behaviors. Currently
this is not an easy task since there is no template list provided by default in the Python API of Blender 4.3 allowing that.

**This add-on is then an attempt to simply re-creates the list of the layers and layer groups of a Grease Pencil object in a custom panel.**


![GP_Layers And Groups Screen](images/GP_LayersAndGroupsScreen.jpg)


## Disclamer

This is an experimental add-on. I cannot be held responsible for any misuse of the product or loss of data.

The implementation and approach I used do not pretend to be perfect, and there is probably a smarter way to get to the same result. Nevertheless this
one works and provides the expected interactions and UI feedback a user may have in order to use only this template list when integrated into your own add-on.

Feel free to send me any issue you may face, as well as suggestions to improve this implementation.


## Download and Installation

Get the add-on package from the [Release page](https://github.com/werwack/gp3-layers-template-list/releases/).

Then open Blender 4.3, go to the Preference panel, Add-Ons section, then install the package thanks to the *Install From Disk...* 
dropdown component, at the top right side of the window.


## Use

Once installed, the add-on panel appears in the N-tabs of the viewport under the name "Layers List".

Click on it, and select a Grease Pencil object in the scene. The layers are then displayed in the add-on panel.

Layers and layer groups can be selected to set the active item, and they properties (mask, layer skin, visibility, lock) can be changed
from the panel.

Whenever the structure of the layers hierarchy is modified, when a layer or layer group is added, removed or moved for example, the layers
tree in the template list receives some notifications and is rebuilt to match the layers list displayed in the Properties panel.


## Current limitations

At the moment this implementation is facing the following limitations. They are rather minor and do not prevent the template list
to work very efficiently:

* **Layer and Layer Group colors are not supported**
  This will be the case on Blender 4.4.

* **Drag and drop of layers and layer groups is not supported.**
  This behavior is currently not supported by the template list component
  of the Python API.

  Since this has an impact in the manipulations of the layer tree (when a layer has to be placed into a group for example),
  the Move Up and Move Down buttons in the template list will have to be modified a bit (coming soon):

    - when clicking on them, the active element is moved at the same level in the hierarchy (as in the Properties panel)
    - when Shift + clicking on them, the active element is moved into - or out of - the element place above or below it.

* **Empty layer groups may have a wrong position in the tree.** This has no impact on the grease pencil object display though because
  they are empty.

* **Collapsing or expanding a layer group is not yet implemented.**
  Note that the expanded state of the layer groups will not match the one of the Properties panel. This is because this state is not
  a property of the layer group but a property of the UI. It allows for example 2 Properties panels to be opened at the same time in
  the interface of Blender, each one with a different expanded state.

**Bugs:**

* When calling Undo, the custom layers list is not refreshed

