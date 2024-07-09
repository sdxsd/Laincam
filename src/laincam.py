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
from pillow_lut import load_cube_file
import argparse as ap
import math
import numpy as np
import cv2

NOISE_DATA = "PICT1629.tif"

def determine_contrast_and_saturation(img_path):
    img = cv2.imread(img_path)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return (img_grey.std(), img_hsv[:,:,1].mean()) # Contrast & Saturation

def apply_noise(noise, base):
    result = ImageChops.overlay(base, noise)
    # result = ImageChops.soft_light(base, noise)
    return (result)

def resize(noise, base):
    bwidth, bheight = base.size
    nwidth, nheight = noise.size
    true_nwidth = int(nwidth * (1 / math.sqrt(2)))
    true_nheight = int(nheight * (1 / math.sqrt(2)))
    if (bwidth > true_nwidth):
        new_bheight = int(bheight * (true_nwidth / bwidth))
        resized = base.resize((true_nwidth, new_bheight), Image.Resampling.NEAREST)
        new_bheight = int(new_bheight * (nwidth / true_nwidth))
        resized = base.resize((nwidth, new_bheight), Image.Resampling.HAMMING)
        return (resized)
    return (base)

def enhance_image(base, contrast, saturation, noise):
    # base = base.filter(ImageFilter.SHARPEN)
    # lut = load_cube_file("./LUT/P1080675_Look.cube")
    lut = load_cube_file("./LUT/kyocerasix.cube")
    base = base.filter(lut)

    base = base.filter(ImageFilter.GaussianBlur(0.5))
    base = apply_noise(noise, base)
    base = base.filter(ImageFilter.UnsharpMask(0.5))

    # enh_sharpness = ImageEnhance.Sharpness(base)
    # result = enh_sharpness.enhance(1.1)
    # return (result)

    # enh_contrast = ImageEnhance.Contrast(base)
    # print("Contrast: {}, Saturation: {}".format(contrast / 100, saturation / 100))
    # enhanced_contrast = enh_contrast.enhance((1.0 + (0.4 - (contrast / 100))))
    # enh_color = ImageEnhance.Color(enhanced_contrast)
    # result = enh_color.enhance(1.0 + (0.6 - (saturation / 100)))
    # return (result)
    return (base)

def main():
    parser = ap.ArgumentParser(prog="Laincam", description="Kyocera look emulator", epilog="Laincam")
    parser.add_argument("input_img")
    args = parser.parse_args()
    base = Image.open(args.input_img)
    noise = Image.open(NOISE_DATA)
    base = resize(noise, base)
    contrast, saturation = determine_contrast_and_saturation(args.input_img)
    base = enhance_image(base, contrast, saturation, noise)
    base.show()
    base.save("digified_" + args.input_img)

main()
