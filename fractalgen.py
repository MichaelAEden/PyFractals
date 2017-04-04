from fractal import FractalMandel, FractalJulia, FractalNewton
import numpy as np

def f_sine(x):
    """Seed function of which this will be approximating the root"""
    return np.sin(x)

def dx_sine(x):
    """Derivative of the seed function"""
    return np.cos(x)

def f_cosine(x):
    """Seed function of which this will be approximating the root"""
    return np.cos(np.sin(x)) - np.pi

def dx_cosine(x):
    """Derivative of the seed function"""
    return -1 * np.cos(x) * np.sin(np.sin(x))

def f_polynomial(x):
    """Seed function of which this will be approximating the root"""
    return np.power(x, 3) + 1

def dx_polynomial(x):
    """Derivative of the seed function"""
    return 3 * np.power(x, 2)

if __name__=='__main__':
    np.set_printoptions(threshold=np.nan)

    julia_seed = complex(0, 0.6)
    mandel_seeds = None
    newton_seeds = dict(f=f_cosine, dx=dx_cosine, a=1)

    fractal = FractalNewton()
    fractal.generate_fractal(1000, 1000, -10, 10, -10, 10, 100, newton_seeds)
    fractal.display()

