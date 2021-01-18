#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Freelancer.com project
Gimp script
- Scale the image to 1080 width (keep the proportions)
- Change canvas size to 1920 width (keep the proportions)
- Apply a background to the full image
- Apply the colour #113366 to the whole background
"""

from gimpfu import *

def rescale_image(image, rescale_width):
    """Rescales image to 1080 keeping aspect ratio

    :Args:
     - image (IMAGE): The image 
     - rescale_width (int): New width of the image
    """

    # image size
    image_height = pdb.gimp_image_height(image)
    image_width = pdb.gimp_image_width(image)

    # new image height
    rescale_height = round(image_height * (rescale_width * 1.0 / image_width))

    pdb.gimp_image_scale(image, rescale_width, rescale_height)
    gimp.message('Rescaled image')


def resize_canvas(image, resize_width):
    """Resizes canvas and keeps image in center

    :Args:
     - image (IMAGE): The image 
     - resize_width(int): New width of the canvas
    """

    # image size
    image_height = pdb.gimp_image_height(image)
    image_width = pdb.gimp_image_width(image)

    # new canvas size
    resize_height = round(image_height * (resize_width * 1.0 / image_width))

    marginY = resize_height - image_height
    marginX = resize_width - image_width
    pdb.gimp_image_resize(image, resize_width, resize_height, marginX / 2,
                          marginY / 2)
    gimp.message('Resized canvas')


def apply_background(image, background_width):
    """Apply a background to the full image

    :Args:
     - image (IMAGE): The image 
     - background_width (int): Width of the background layer
    """

    # image size
    image_height = pdb.gimp_image_height(image)
    image_width = pdb.gimp_image_width(image)

    # background height
    background_height = round(image_height * (background_width * 1.0 / image_width))

    # convert to rgba
    if pdb.gimp_image_base_type(image):
        pdb.gimp_image_convert_rgb(image)

    # Apply the colour #113366 to the background
    pdb.gimp_context_set_background('#113366')
    gimp.message('Apply colour to the background')

    # create new layer
    bg_layer = pdb.gimp_layer_new(
        image,
        background_width,
        background_height,
        RGBA_IMAGE,
        'background',
        100,
        LAYER_MODE_NORMAL,
        )

    # fill layer with the colour
    pdb.gimp_drawable_fill(bg_layer, FILL_BACKGROUND)
    
    # Apply a background to the full image
    pdb.gimp_image_add_layer(image, bg_layer, 1)
    gimp.message('Apply a background to the full image')

def prepareGraphic(image, drawable):
    rescale_image(image, 1080)
    resize_canvas(image, 1920)
    apply_background(image, 1920)

register(
    'prepare-image',
    'Prepare image',
    'Prepares an image for editing',
    'xNetcat',
    'xNetcat',
    '2021',
    '<Image>/Custom/Prepare image',
    '*',
    [],
    [],
    prepareGraphic,
    )

main()