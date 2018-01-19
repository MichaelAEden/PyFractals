from fractal import Fractal
from julia import Julia
from mandelbrot import Mandelbrot
from newton import Newton
from pheonix import Pheonix

# Static constant fractal instances.
MANDELBROT = Mandelbrot("Mandelbrot Set")
NEWTON =     Newton("Newton Fractal")
JULIA =      Julia("Julia Set")
PHEONIX =    Pheonix("Pheonix Fractal")


def getFractal(fractal_id):
    return Fractal.FRACTALS[fractal_id]


def getFractals():
    return Fractal.FRACTALS