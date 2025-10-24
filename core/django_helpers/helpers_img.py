#from tkinter import *
from PIL import Image, ExifTags
#==============================================================================================
def fix_image_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # no EXIF data
        pass
    return img
#==============================================================================================
def crop_image(img,target_width,target_height):

    width, height = img.size
    aspect_ratio = target_width / target_height
    current_ratio = width / height

    if current_ratio > aspect_ratio:
        # Too wide -> crop sides
        new_width = int(height * aspect_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top, bottom = 0, height
    else:
        # Too tall -> crop top/bottom
        new_height = int(width / aspect_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        left, right = 0, width

    img = img.crop((left, top, right, bottom))

    return img
#==============================================================================================