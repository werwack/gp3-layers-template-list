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
GP3 useful functions
"""


def isLayer(layerOrGp):
    if "GreasePencilLayer" == type(layerOrGp).__name__:
        return True
    return False


def printLayers(gp):
    for layer in gp.data.layers:
        print(layer.name)


def printLayerGroups(gp):
    for layerGp in gp.data.layer_groups:
        print(layerGp.name)
