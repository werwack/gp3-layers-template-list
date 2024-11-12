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
Layer Tree functions
"""


def getLayerTree(gpencil, verbose=True):
    class LayerTreeItem:
        def __init__(self):
            # can be a layer or a group
            self.layerOrGroup = None

            self.parent = None
            # list of LayerTreeItem
            self.children = list()

        def getChildIndex(self, layerOrGrp):
            """Return the index of a LayerTreeItem in the current LayerTreeItem, -1 if not found"""
            for i, it in enumerate(self.children):
                if layerOrGrp == it.layerOrGroup:
                    return i
            return -1

        def getChildRec(self, layerOrGrp):
            def _getChildRec(item, layerOrGrp):
                """Return a LayerTreeItem, None if not found"""
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
            """Return a LayerTreeItem, None if not found"""
            childInd = self.getChildIndex(layerOrGrp)
            if -1 != childInd:
                return self.children[childInd]
            return None

        def printLayerTree(self):
            pointersList = list()

            def _printLayerTreeRec(layerTree, spacer):
                if layerTree.layerOrGroup is None:
                    if verbose:
                        print(f"\n{spacer}- Root")
                else:
                    if verbose:
                        print(f"{spacer}- {layerTree.layerOrGroup.name}")
                    # pointer / layer type / depth / num children
                    pointersList.append(
                        (
                            layerTree.layerOrGroup.as_pointer(),
                            type(layerTree.layerOrGroup).__name__,
                            int(len(spacer) / 2),
                            len(layerTree.children),
                        )
                    )
                # for it in reversed(layerTree.children):
                for it in reversed(layerTree.children):
                    spacerChild = spacer + "  "
                    _printLayerTreeRec(it, spacerChild)

            _printLayerTreeRec(self, "")
            return pointersList

    gpLayerTreeRoot = LayerTreeItem()

    def _addLayersOrGrpsTotree(doLayers=True):
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

            subTreeItem = gpLayerTreeRoot
            # we start from the root parent group
            for parentGrp in reversed(parentGrps):
                child = subTreeItem.getChildRec(parentGrp)
                if child is None:
                    gpLayerTreeItem = LayerTreeItem()
                    gpLayerTreeItem.layerOrGroup = parentGrp
                    # is its parent in the tree?
                    subTreeItem.children.append(gpLayerTreeItem)
                    subTreeItem = gpLayerTreeItem
                else:
                    subTreeItem = child

            # now add the layer as a leaf
            child = subTreeItem.getChild(layer)
            if child is None:
                gpLayerTreeItem = LayerTreeItem()
                gpLayerTreeItem.layerOrGroup = layer
                subTreeItem.children.append(gpLayerTreeItem)
                # subTreeItem = gpLayerTreeItem     # not necessary
            else:
                subTreeItem = child  # not necessary
                pass

    # collect layers
    _addLayersOrGrpsTotree(doLayers=True)

    # now collect empty groups
    _addLayersOrGrpsTotree(doLayers=False)

    print("\nLayers:")
    for layer in gpencil.data.layers:
        print(layer.name)

    print("\nLayer Groups:")
    for layerGp in gpencil.data.layer_groups:
        print(layerGp.name)

    pointersList = gpLayerTreeRoot.printLayerTree()

    # return gpLayerTreeRoot
    return pointersList


def getActiveLayerOrGp(gp):
    if gp.data.layers.active is not None:
        return gp.data.layers.active
    if gp.data.layer_groups.active is not None:
        return gp.data.layer_groups.active
    return None
