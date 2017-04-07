from fractal import FractalMandel, FractalJulia, FractalNewton, FractalPheonix
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

    julia_seed = dict(num_colors=5, c=complex(0.25, -0.54))
    mandel_seeds = dict(num_colors=5)
    pheonix_seeds = dict(c=complex(0.56, 0), P=-0.5)
    newton_seeds = dict(f=f_polynomial, dx=dx_polynomial, a=1)

    fractal = FractalNewton()
    # fractal.generate_fractal(2000, 2000, -3, 3, -3, 3, 20, newton_seeds) # THIS IS SO COOL
    # fractal.generate_fractal(100, 100, -2.0, 0.5, -1.25, 1.25, 100, julia_seed)  # Classic Mandel
    # fractal.generate_fractal(2000, 2000, -2.0, 2.0, -2.0, 2.0, 50, julia_seed)     # Julia set
    fractal.generate_fractal(500, 500, -2.0, 2.0, -2.0, 2.0, 50, newton_seeds)     # Julia set

    fractal.display()

