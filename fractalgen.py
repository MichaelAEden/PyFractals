import os
import math

from fractal import FractalMandel
from fractal import FractalJulia
from fractal import FractalNewton
import renderanimation

import numpy as np

FRAMES_FILE_NAME = "anim/frames/frame_"
VIDEO_FILE_NAME = "anim/videos/video"

# TODO: reduce gif filesize

def run():
    init()

    # fractal = FractalJulia(800, 800, 50, -1.3, 1.3, -1.3, 1.3)
    # fractal = FractalMandel(800, 800, 50, -2.0, 0.5, -1.25, 1.25)
    fractal = FractalNewton(800, 800, 50, -3.0, 3.0, -3.0, 3.0,
                            f=None,
                            dx=None)

    # renderanimation.animate_fractal_values(fractal, FRAMES_FILE_NAME,
    #                                        lambda x: dict(c=complex(real=0.14 * (math.log(x + 0.001) + 3),
    #                                                                 imag=0.2 * math.pow(x, 2.0))))
    # renderanimation.animate_fractal_values(fractal, FRAMES_FILE_NAME,
    #                                        lambda x: dict(p=-3 * math.pow(x - 1, 2) + 2),
    #                                        step=0.05)
    renderanimation.animate_fractal_values(fractal, FRAMES_FILE_NAME,
                                           lambda x: dict(f=(lambda y: np.sin(np.cos(y)) - 7 * x),
                                                          dx=(lambda y: -1 * np.sin(y) * np.cos(np.cos(y)))),
                                           step=1.00)

    renderanimation.convert_pngs_to_video(FRAMES_FILE_NAME, VIDEO_FILE_NAME)

    clean_up()


def init():
    np.set_printoptions(threshold=np.nan)


def clean_up():
    """Deletes pyc files"""

    list_of_pyc = [f for f in os.listdir('.') if '.pyc' in f]
    for pyc_file in list_of_pyc:
        try:
            # Occasionally this fails if the .pyc file was just generated
            os.remove(pyc_file)
        except:
            pass



if __name__=='__main__':
    run()
