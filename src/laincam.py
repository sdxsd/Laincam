#!/usr/bin/env python3

# Laincam IS LICENSED UNDER THE GNU GPLv3
# Copyright (C) 2024 Will Maguire

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# The definition of Free Software is as follows:
# 	- The freedom to run the program, for any purpose.
# 	- The freedom to study how the program works, and adapt it to your needs.
# 	- The freedom to redistribute copies so you can help your neighbor.
# 	- The freedom to improve the program, and release your improvements
#   - to the public, so that the whole community benefits.

# A program is free software if users have all of these freedoms.

import argparse as ap
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageChops
import math

def load_image(image_name):
    img = Image.open(image_name)
    return (img)

def load_noise_overlay(noise_img_path):
    noise = Image.open(noise_img_path)
    return (noise)

def prep_img(noise, base):
    res = noise.size
    x = res[0] * (1 / math.sqrt(2))
    y = res[1] * (1 / math.sqrt(2))
    base = base.resize((int(x), int(y)), Image.Resampling.BILINEAR)
    base = base.filter(ImageFilter.SHARPEN)
    enh = ImageEnhance.Contrast(base)
    base = enh.enhance(1.25)
    result = ImageChops.overlay(base, noise)
    result.save("bloop.jpg")
    return (base)


def main():
    parser = ap.ArgumentParser(prog="Laincam", description="Kyocera look emulator", epilog="Laincam")
    parser.add_argument("input_img")
    args = parser.parse_args()
    img = load_image(args.input_img)
    noise = load_noise_overlay("PICT1629.tif")
    prep_img(noise, img)


main()
