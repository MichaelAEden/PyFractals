import os
import math

from fractal import FractalMandel
from fractal import FractalJulia
import renderanimation

import numpy as np

FRAMES_FILE_NAME = "anim/frames/frame_"
VIDEO_FILE_NAME = "anim/videos/video"


def run():
    init()

    # fractal = FractalMandel(800, 800, 50, -1.3, 1.3, -1.3, 1.3)
    fractal = FractalMandel(800, 800, 50, -2.0, 0.5, -1.25, 1.25)

    # renderanimation.animate_fractal_values(fractal, FRAMES_FILE_NAME,
    #                                        lambda x: dict(c=complex(real=0.14 * (math.log(x + 0.001) + 3),
    #                                                                 imag=0.2 * math.pow(x, 2.0))))
    # renderanimation.animate_fractal_values(fractal, FRAMES_FILE_NAME,
    #                                        lambda x: dict(p=-3 * math.pow(x - 1, 2) + 2),
    #                                        step=0.05)
    renderanimation.animate_fractal_values(fractal, FRAMES_FILE_NAME,
                                           lambda x: dict(p=-3.6 * math.pow(x - 1, 2) + 2 if x > 0.25 else 4 * x - 1),
                                           step=0.01)

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
