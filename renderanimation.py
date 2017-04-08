import math
import subprocess

from PIL import Image


def generate_zoom_images(fractal, filename):
    """
    Generates a series of zoom images for any fractal.
    :param fractal:
    :param filename:
    :return:
    """

    n = 300
    m = 300

    zoom_iters = 30

    start_frame = (-2.0, 0.5, -1.25, 1.25)
    end_frame = (-1.4846, -1.4845, -0.00005, 0.00005)

    zoom_count = 0
    for zoom_count in range(zoom_iters + 1):
        # Calculates the boundaries of the current zoom frame
        current_frame = []
        for i in range(4):
            current_frame.append((start_frame[i] +
                                    (zoom_count / float(zoom_iters) *
                                     (end_frame[i] - start_frame[i]))))

        # print current_frame

        rgb_image = fractal.get_fractal_image(n, m, 100, *current_frame, num_colors=5, p=2)
        saved_image = Image.fromarray(rgb_image, 'RGB')
        saved_image.save(filename + str(zoom_count) + '.png')

def animate_mandel(fractal, filename):
    # To get a smooth animation, we input values of p(x) on the curve p(x) = -e^-x + 2 until within a certain bound of 2
    e = 0.01

    x = 0
    p = 1

    iter_count = 0
    while (2 - p) > e:
        iter_count += 1

        x += 0.1
        p = -math.exp(-x) + 2

        rgb_image = fractal.get_fractal_image(300, 300, -2.0, 0.5, -1.25, 1.25, 100, num_colors=5, p=p)
        saved_image = Image.fromarray(rgb_image, 'RGB')
        saved_image.save(filename + '.png')

        # Safeguard so things do not get out of control
        if iter_count > 100:
            break


def animate_julia(fractal, filename):
    # To get a smooth animation, we input values of p(x) on the curve p(x) = -e^-x + 2 until within a certain bound of 2
    e = 0.01

    x = 0
    p = 1

    iter_count = 0
    while (2 - p) > e:
        iter_count += 1

        x += 0.1
        p = -math.exp(-x) + 2

        rgb_image = fractal.generate_fractal_image(300, 300, -2.0, 0.5, -1.25, 1.25, 100, num_colors=5, p=p)
        saved_image = Image.fromarray(rgb_image, 'RGB')
        saved_image.save(filename + '.png')

        # Safeguard so things do not get out of control
        if iter_count > 100:
            break


def convert_pngs_to_video(FRAMES_FILE_NAME):    # TODO: actually pass in parameter
    """Converts the generated series of images into an animation, outputs as output.mp4"""

    # This is a bad way of doing things.
    # TODO: install ffmpeg in virtualenv
    env = {'PATH': '/Users/michael/.rvm/gems/ruby-2.3.3/bin:/Users/michael/'
                   + '.rvm/gems/ruby-2.3.3@global/bin:/Users/michael/.rvm/rubies'
                   + '/ruby-2.3.3/bin:/bin:/sbin:/usr/bin:/usr/local/sbin:/usr/'
                   + 'local/bin:/usr/local/bin/ngrok:/usr/local/mysql/bin:/Users/michael/.rvm/bin'}
    subprocess.call(["./mandel_anim_script.sh"], env=env)
