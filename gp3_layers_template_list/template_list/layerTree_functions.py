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
Layer Tree Pointers list functions
"""


def getLayerTreePointers(gpencil, verbose=True):
    """Return a flat list of tupples made of:
    - a pointer to a layer or layer group
    - the name of the entity type: "GreasePencilLayer" or "GreasePencilLayerGroup"
    - the depth of the entity in the tree hierarchy (0: at root level)
    - the number of children

    Note: the use of instances of the class LayerTreeEntity is purely internal to this file
    """

    class LayerTreeEntity:
        def __init__(self):
            # can be a layer or a group
            self.layerOrGroup = None

            # not used
            # self.parent = None

            # list of LayerTreeEntity
            self.children = list()

        def isLayer(self):
            if self.layerOrGroup is None:
                return None
            return "GreasePencilLayer" == type(self.layerOrGroup).__name__

        def getChildIndex(self, layerOrGrp):
            """Return the index of a LayerTreeEntity in the current LayerTreeEntity, -1 if not found"""
            for i, it in enumerate(self.children):
                if layerOrGrp == it.layerOrGroup:
                    return i
            return -1

        def getChildRec(self, layerOrGrp):
            def _getChildRec(item, layerOrGrp):
                """Return a LayerTreeEntity, None if not found"""
                # parcours des enfants génération par génération, pas en profondeur
                for child in item.children:
                    if child.layerOrGroup == layerOrGrp:
                        return child

                # if not in this generation, query the next gen of each child
                for child in item.children:
                    if len(child.children):
                        subChild = _getChildRec(child, layerOrGrp)
                        if subChild is not None:
                            return subChild

                return None

            # childInd = self.getChildIndex(layerOrGrp)
            # if -1 != childInd:
            #     return self.children[childInd]
            # return None

            return _getChildRec(self, layerOrGrp)
            # if self == layerOrGrp:
            #     return self
            # return None

        def getChild(self, layerOrGrp):
            """Return a LayerTreeEntity, None if not found"""
            childInd = self.getChildIndex(layerOrGrp)
            if -1 != childInd:
                return self.children[childInd]
            return None

        def printLayerTree(self, emptyGroups, tmpLayers):
            pointersList = list()

            def _findInGroupsFromPointer(pt, emptyGrps):
                """return the group, None if not found"""
                for grp in emptyGrps:
                    if str(pt) == str(grp.as_pointer()):
                        return grp
                return None

            # def _findInTmpLayersFromPointer(pt):
            #     """return the group, None if not found"""
            #     for grp in emptyGrps:
            #         if str(pt) == str(grp.as_pointer()):
            #             return grp
            #     return None

            def _printLayerTreeRec(layerTree, spacer):
                if layerTree.layerOrGroup is None:
                    if verbose:
                        print(f"\n{spacer}- Root")
                else:
                    if verbose:
                        print(f"{spacer}- {layerTree.layerOrGroup.name}")

                    # ignore temp layers
                    # if layerTree.parent is not None and _findInGroupsFromPointer(layerTree.parent, emptyGroups) is not None:
                    # if layerTree.parent is not None and layerTree.parent.layerOrGroup in emptyGroups:
                    if layerTree.layerOrGroup in tmpLayers:
                        # layerTree is a temp layer entity in an empty group
                        pass
                    else:
                        numChildren = len(layerTree.children)
                        if layerTree.layerOrGroup in emptyGroups:
                            # layerTree is an empty group entity
                            numChildren = 0

                        # pointer / layer type / depth / num children
                        pointersList.append(
                            (
                                layerTree.layerOrGroup.as_pointer(),
                                type(layerTree.layerOrGroup).__name__,
                                int(len(spacer) / 2),
                                numChildren,
                            )
                        )
                # for it in reversed(layerTree.children):
                for it in reversed(layerTree.children):
                    spacerChild = spacer + "  "
                    _printLayerTreeRec(it, spacerChild)

            _printLayerTreeRec(self, "")
            return pointersList

        def getEmptyGroups_old_tooLong(self):
            """Return a list of all the empty group entities found under that branch level"""

            def _recGetEmptyGroups(entity, empty_groups):
                if 0 == len(entity.children) and entity.isLayer():
                    empty_groups.append(self)
                else:
                    for c in entity.children:
                        _recGetEmptyGroups(c, empty_groups)

            emptyGroups = list()
            _recGetEmptyGroups(self, emptyGroups)
            return emptyGroups

    def _addLayersOrGrpsToTree(treeRoot, doLayers=True):
        layersOrGroups = gpencil.data.layers if doLayers else gpencil.data.layer_groups

        for layer in layersOrGroups:
            # get the groups parent hierarchy
            parentGrps = list()
            parentGrp = layer.parent_group
            while parentGrp is not None:
                parentGrps.append(parentGrp)
                parentGrp = parentGrp.parent_group

            # parentGrpReversed = list()
            # parentGrpReversed = [gp for gp in range(len(parentGrp) - 1, -1, -1)]
            # parentGrp = parentGrpReversed

            subTreeItem = treeRoot
            # we start from the root parent group
            for parentGrp in reversed(parentGrps):
                child = subTreeItem.getChildRec(parentGrp)
                if child is None:
                    gpLayerTreeItem = LayerTreeEntity()
                    gpLayerTreeItem.layerOrGroup = parentGrp
                    # is its parent in the tree?
                    subTreeItem.children.append(gpLayerTreeItem)
                    subTreeItem = gpLayerTreeItem
                else:
                    subTreeItem = child

            # now add the layer as a leaf
            child = subTreeItem.getChild(layer)
            if child is None:
                gpLayerTreeItem = LayerTreeEntity()
                gpLayerTreeItem.layerOrGroup = layer
                subTreeItem.children.append(gpLayerTreeItem)
                # subTreeItem = gpLayerTreeItem     # not necessary
            else:
                subTreeItem = child  # not necessary
                pass

    ############################################################

    useEmptyGrpFix = True
    emptyGroups = list()
    tmpLayers = list()
    ###############
    # fix empty groups order
    if useEmptyGrpFix:
        emptyGroups = getEmptyGroups(gpencil)
        print("\nEmpty groups:")
        if len(emptyGroups):
            for gp in emptyGroups:
                print(f"  {gp.name}")
        else:
            print("  no empty groups")

        # add temp layer in groups
        for grp in emptyGroups:
            newTmpLayer = gpencil.data.layers.new("__wksl_tmpLayer__", set_active=False, layer_group=grp)
            tmpLayers.append(newTmpLayer)

    ###############

    gpLayerTreeRoot = LayerTreeEntity()

    # collect layers
    _addLayersOrGrpsToTree(gpLayerTreeRoot, doLayers=True)

    # now collect empty groups
    _addLayersOrGrpsToTree(gpLayerTreeRoot, doLayers=False)

    pointersList = gpLayerTreeRoot.printLayerTree(emptyGroups, tmpLayers)

    ###############
    # fix empty groups order
    # remove tmp layers
    # wkip we could use pointers instead of layers for tmp layers
    if useEmptyGrpFix:
        for layer in tmpLayers:
            gpencil.data.layers.remove(layer)

    ###############

    print("\nLayers:")
    for layer in gpencil.data.layers:
        print(layer.name)

    print("\nLayer Groups:")
    for layerGp in gpencil.data.layer_groups:
        print(layerGp.name)

    # return gpLayerTreeRoot
    return pointersList


def getEmptyGroups(gpencil):
    """Return a list of all the empty groups"""
    emptyGroups = [gp for gp in gpencil.data.layer_groups]
    for gp in gpencil.data.layer_groups:
        if len(emptyGroups):
            if gp.parent_group in emptyGroups:
                emptyGroups.remove(gp.parent_group)
        else:
            break

    if len(emptyGroups):
        for layer in gpencil.data.layers:
            if len(emptyGroups):
                if layer.parent_group in emptyGroups:
                    emptyGroups.remove(layer.parent_group)
            else:
                break

    return emptyGroups


def getLayerFromPt(gpencil, layerPointer):
    for layer in gpencil.data.layers:
        if str(layer.as_pointer()) == str(layerPointer):
            return layer
    return None


def getActiveLayerOrGp(gp):
    if gp.data.layers.active is not None:
        return gp.data.layers.active
    if gp.data.layer_groups.active is not None:
        return gp.data.layer_groups.active
    return None
