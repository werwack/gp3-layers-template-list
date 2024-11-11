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
__init__
"""

from . import template_list

bl_info = {
    "name": "GP3 Layers Template List",
    "author": "Julien Blervaque (aka Werwack)",
    "description": "Re-create the layers list of a Grease Pencil object in a custom panel",
    "blender": (4, 3, 0),
    "version": (1, 0, 1),
    "location": "View3D > Layers List",
    "doc_url": "https://github.com/werwack/gp3-layers-template-list",
    "tracker_url": "https://github.com/werwack/gp3-layers-template-list/issues",
    "warning": "Beta",
    "category": "3D View",
}


def register():
    print("Registering GP3 Layers Template List...")
    template_list.register()


def unregister():
    pass
    template_list.unregister()
