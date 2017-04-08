from fractal import FractalMandel
import renderanimation

import numpy as np

FRAMES_FILE_NAME = "anim/frame_"

if __name__=='__main__':
    np.set_printoptions(threshold=np.nan)

    fractal = FractalMandel()

    renderanimation.generate_zoom_images(fractal, FRAMES_FILE_NAME)
    # renderanimation.animate_mandel(fractal, FRAMES_FILE_NAME)
    renderanimation.convert_pngs_to_video(FRAMES_FILE_NAME)
