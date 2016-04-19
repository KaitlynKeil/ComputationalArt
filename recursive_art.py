""" Computational Art Reworked: Mini Project 5
    Kaitlyn Keil
    Software Design Spring 2016 """

import random
from PIL import Image
from math import *
import numpy as np


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a lambda function
                 possible functions:
                    prod(a,b) = ab
                    avg(a,b) = 0.5 * (a + b)
                    circle(a,b) = sqrt(a^2 + b^2)/sqrt(2)
                    hyperbola(a,b) = (a^2 + b^2)/sqrt(2)
                    cos_pi(a) = cos(pi*a)
                    sin_pi(a) = sin(pi*a)
                    sqrt_abs(a) = sqrt(abs(a))
                    power(a) = a^(randomPower)
                    to_the(a) = randomBase^a
    """
    x = lambda x,y,t: x
    y = lambda x,y,t: y
    t = lambda x,y,t: t
    product = lambda f1,f2: f1*f2
    average = lambda f1,f2: (f1+f2)/2
    circle = lambda f1,f2: np.sqrt(f1**2 + f2**2)/sqrt(2)
    hyperbola = lambda f1,f2: (f1**2 - f2**2)/ sqrt(2)
    get_sign = lambda f1,f2: abs(f1)*np.sign(f2)
    to_the_power = lambda f1,f2: abs(f1)**abs(f2)
    cosine = lambda f1: np.cos(pi * f1)
    sine = lambda f1: np.sin(pi * f1)
    sqrt_abs = lambda f1: np.sqrt(abs(f1))
    power = lambda f1: f1**7
    to_the = lambda f1: 0.5**abs(f1)
    function_list = [x, y, t, product, average, circle, hyperbola, get_sign, to_the_power,
                    cosine, sine, sqrt_abs, power, to_the]

    n = len(function_list) # Get the length of the list of possible functions
    
    if max_depth == 0: # stops the function if it has hit the maximum depth
        i = random.randint(0,2)
    elif min_depth <= 0:
        i = random.randint(0, n-1)
    else: # ignore the last three options if minimum depth hasn't reached 0.
        i = random.randint(3, n-1)

    if i == 0:
        return lambda x,y,t: x # makes sure the function ends on x, y, or t
    elif i == 1:
        return lambda x,y,t: y 
    elif i == 2:
        return lambda x,y,t: t

    # Generate the function. If needed, generate a second function
    new_function1 = build_random_function(min_depth-1, max_depth-1)

    if i in range(3,9):
        new_function2 = build_random_function(min_depth-1, max_depth-1)
        return lambda x,y,t: function_list[i](new_function1(x,y,t), new_function2(x,y,t))
    else:
        return lambda x,y,t: function_list[i](new_function1(x,y,t))

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_interval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        Had to alter these to account for NumPy, no longer includes float()

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1
        >>> remap_interval(5, 4, 6, 1.0, 2.0) #not fond of this integer value here, but it's what makes NumPy work
        1.5
    """
    range_old = input_interval_end - input_interval_start
    range_new = output_interval_end - output_interval_start
    step_multiplier = range_new / range_old
    from_start_old = val - input_interval_start
    from_start_new = from_start_old * step_multiplier
    new_val = output_interval_start + from_start_new
    return new_val 

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: value in the interval [0,255]

        >>> color_map(-1.0)
        0.0
        >>> color_map(1.0)
        254.0
        >>> color_map(0.0)
        127.0
        >>> color_map(0.5)
        190.5
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return color_code

def generate_art(filename, x_size, y_size, timespan):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    print 'Red Done'
    green_function = build_random_function(7,9)
    print 'Green Done'
    blue_function = build_random_function(7,9)
    print 'Blue Done'

    x = np.tile(np.linspace(-1,1, x_size),(y_size,1))   # lines things up nicely
    y = np.tile(np.linspace(-1,1, y_size),(x_size,1)).T

    for t_index in range(timespan):
        t = remap_interval(float(t_index),0.0, float(timespan-1),-1.0,1.0)
        red = color_map(red_function(x,y,t))
        green = color_map(green_function(x,y,t))
        blue = color_map(blue_function(x,y,t))

        pixels = np.vstack(([red.T],[green.T],[blue.T])).T #lines everything up

        im = Image.fromarray(pixels.astype(np.uint8))
        im.save(filename%t_index)

if __name__ == '__main__':
    import doctest
    #doctest.testmod()
    # Create some computational art!
    generate_art("frame%03d.png",500,500,100)
