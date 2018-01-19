import numpy as np


def adjustRange(a, vmin=0, vmax=255):
    """
    Return array with values compressed into given range.

    :type a: np.ndarray
    :param vmin: Minimum value
    :param vmax: Maximum value
    :return: Array with values ranging from vmin to vmax.
    :rtype: np.ndarray
    """
    new_a = (
        (
            # Represent array as floats ranging between 0 and 1.
            a.astype(dtype=float) / np.nanmax(a)

            # Fill given range.
            * (vmax - vmin) + vmin
        )
        # Convert back to regular array.
        .astype(dtype=np.uint8)
    )

    return new_a
