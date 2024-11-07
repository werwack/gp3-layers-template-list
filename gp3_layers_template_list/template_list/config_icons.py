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

import os
from pathlib import Path
import bpy
import bpy.utils.previews


def initGlobalVariables():
    # icons
    global icons_col

    pcoll = bpy.utils.previews.new()
    # my_icons_dir = os.path.join(os.path.dirname(__file__), "../icons")
    currentDir = os.path.dirname(__file__)
    addon_dir = Path(currentDir).parent
    my_icons_dir = os.path.join(addon_dir, "template_list")
    my_icons_dir = os.path.join(my_icons_dir, "icons")
    for imgFile in Path(my_icons_dir).rglob("*.png"):
        # print(f"str(png): {str(imgFile)}")
        pcoll.load(imgFile.stem, str(imgFile), "IMAGE")

    icons_col = pcoll


def releaseGlobalVariables():
    global icons_col

    bpy.utils.previews.remove(icons_col)
    icons_col = None
