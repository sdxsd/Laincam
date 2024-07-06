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

from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageChops
from PIL import Image
import argparse as ap
import math

NOISE_DATA = "PICT1629.tif"

def apply_noise(noise, base):
    result = ImageChops.overlay(base, noise)
    return (result)

def resize(noise, base):
    bwidth, bheight = base.size
    nwidth, nheight = noise.size
    true_nwidth = int(nwidth * (1 / math.sqrt(2)))
    true_nheight = int(nheight * (1 / math.sqrt(2)))
    if (bwidth > true_nwidth):
        new_bheight = int(bheight * (true_nwidth / bwidth))
        resized = base.resize((true_nwidth, new_bheight), Image.Resampling.BICUBIC)
        new_bheight = int(new_bheight * (nwidth / true_nwidth))
        resized = base.resize((nwidth, new_bheight), Image.Resampling.BICUBIC)
        return (resized)
    return (base)

def enhance_image(base):
    base = base.filter(ImageFilter.SHARPEN)
    contrast = ImageEnhance.Contrast(base)
    color = ImageEnhance.Color(base)
    base = contrast.enhance(1.05)
    base = color.enhance(0.90)
    return (base)

def main():
    parser = ap.ArgumentParser(prog="Laincam", description="Kyocera look emulator", epilog="Laincam")
    parser.add_argument("input_img")
    parser.add_argument("ofile")
    args = parser.parse_args()
    base = Image.open(args.input_img)
    noise = Image.open(NOISE_DATA)
    base = resize(noise, base)
    base = enhance_image(base)
    base = apply_noise(noise, base)
    base.save(args.ofile)


main()
