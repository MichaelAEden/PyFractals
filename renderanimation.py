import math
import subprocess

from PIL import Image


def animate_fractal_zoom(fractal, filename, start_frame, end_frame, frames):
    """
    Generates a series of zoom images for a fractal.
    :param fractal: Fractal object which will be zoomed into.
    :param filename: Filename which zoom images will be saved under.
    :param start_frame: Tuple containing coordinates of the initial viewpoint.
    :param end_frame: Tuple containing coordinates of the final viewpoint.
    :param frames: Number of frames used in the animation.
    """

    zoom_count = 0
    for zoom_count in range(frames + 1):
        # Calculates the boundaries of the current zoom frame
        current_frame = []
        for i in range(4):
            current_frame.append((start_frame[i] +
                                    (zoom_count / float(frames) *
                                     (end_frame[i] - start_frame[i]))))

        fractal.set_view_frame(*current_frame)
        rgb_image = fractal.get_fractal_image(*current_frame)
        saved_image = Image.fromarray(rgb_image, 'RGB')
        saved_image.save(filename + str(zoom_count) + '.png')


def animate_fractal_values(fractal, filename, seed_generator, start=0, stop=1, step=0.012):
    """
    Generates an animation for a fractal using different seed values.
    :param fractal: Fractal object which will be animated.
    :param filename: Filename which animation images will be saved under.
    :param seed_generator: Function which takes x as input, returns seed values.
    :param start: Starting value of x used in the function to generate seeds.
    :param stop: Max value of x.
    :param step: Value by which x is incremented.
    """
    x = start
    max = stop

    d = step

    iters = 0
    while x < max:
        iters += 1
        x += d

        new_seeds = seed_generator(x)
        fractal.set_seeds(**new_seeds)

        rgb_image = fractal.get_fractal_image()
        saved_image = Image.fromarray(rgb_image, 'RGB')
        saved_image.save(filename + str(iters) + '.png')

        # Safeguard so too many images are not generated if x never exceeds the max
        if iters > 100:
            break


def convert_pngs_to_video(image_filename, video_filename):
    """Converts the generated series of images into an animation, outputs as output.mp4"""

    # TODO: install ffmpeg in virtualenv
    env = {'PATH': '/Users/michael/.rvm/gems/ruby-2.3.3/bin:/Users/michael/'
                   + '.rvm/gems/ruby-2.3.3@global/bin:/Users/michael/.rvm/rubies'
                   + '/ruby-2.3.3/bin:/bin:/sbin:/usr/bin:/usr/local/sbin:/usr/'
                   + 'local/bin:/usr/local/bin/ngrok:/usr/local/mysql/bin:/Users/michael/.rvm/bin'}

    framerate = 20
    pngs_to_video = ("""
        ffmpeg -framerate %s -i %s%%00d.png -crf 18 -c:v
        libx264 -profile:v high -crf 20 -pix_fmt yuv420p %s.mp4"""
        % (str(framerate), image_filename, video_filename)
        ).replace("\n", "")

    subprocess.Popen(pngs_to_video, env=env, shell=True, stdout=subprocess.PIPE).stdout.read()
