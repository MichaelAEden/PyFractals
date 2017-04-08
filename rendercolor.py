import numpy as np


def adjust_color(image, color_range):
    """
    Adjusts color of image so the maximum and minimum values in the array match those in the given color range
    :param image: Image array
    :type image: np.ndarray
    :param color_range: Minimum and maximum color range values
    :type color_range: tuple
    :return: Image array adjusted for color
    """
    color_min = color_range[0]
    color_range = color_range[1] - color_min

    max_value = np.nanmax(image)

    color_adjusted_image = (image.astype(dtype=float) / max_value * color_range + color_min).astype(dtype=np.uint8)
    return color_adjusted_image
