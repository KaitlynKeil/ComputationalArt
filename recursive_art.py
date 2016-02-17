""" TODO: Put your header comment here """

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
                    cos_pi(a) = cos(pi*a)
                    sin_pi(a) = sin(pi*a)
                    sqrt_abs(a) = sqrt(abs(a))
                    power(a) = a^(randomPower)
                    circle(a,b) = sqrt(a^2 + b^2)
                    to_the(a) = randomBase^a
    """
    function_list = ["prod", "avg", "cos_pi", "sin_pi", "sqrt_abs", "power", "circle", "to_the"]
    if min_depth <= 0: #random test for how far to go when min is 0 but max isn't
        further = random.randint(0,4)
        if max_depth == 0:
            further += 1 # makes sure it stops when max_depth is 0, has slight tendency towards y
        if further == 1:
            return lambda x,y,t: x # makes sure the function ends on x, y, or z
        elif further == 2:
            return lambda x,y,t: y 
        elif further >= 3:
           return lambda x,y,t: t

    # builds 2 functions to use in the following statements; keeps them from 
    #  regenerating each time.
    new_function1 = build_random_function(min_depth-1, max_depth-1)
    new_function2 = build_random_function(min_depth-1, max_depth-1)
    # Creates a random power/base for the functions that need it
    possible_power = random.randint(1,10)
    possible_base = possible_power/10
    
    function_index = random.randint(0, len(function_list)-1) # chooses a function to use

    if function_index == 0: # product
         return lambda x,y,t: (new_function1(x,y,t) * new_function2(x,y,t))
    elif function_index == 1: # average
        return lambda x,y,t: (new_function1(x,y,t) + new_function2(x,y,t)) / 2
    elif function_index == 2: # cos(pi)
        return lambda x,y,t: np.cos(pi * new_function1(x,y,t))
    elif function_index == 3: # sin(pi)
        return lambda x,y,t: np.sin(pi * new_function1(x,y,t))
    elif function_index == 4: # sqrt_abs
        return lambda x,y,t: np.sqrt(abs(new_function1(x,y,t)))
    elif function_index == 5: # power
        return lambda x,y,t: (new_function1(x,y,t))**possible_power
    elif function_index == 6: # circle
        return lambda x,y,t: np.sqrt((new_function1(x,y,t))**2 + (new_function2(x,y,t))**2) / sqrt(2)
    elif function_index == 7: # to_the
       return lambda x,y,t: possible_base**abs(new_function1(x,y,t))
    #    return lambda x,y: 1/(1 + abs((new_function1)(x,y))) # one over <-functions I didn't like
    #    return lambda x,y: e**((new_function1)(x,y)-1) #e <- another function I didn't like

def evaluate_random_function(f, x, y): #has become obsolete with the introduction of lambda
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == 'prod':
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == 'avg':
        return 0.5 * evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == 'cos_pi':
        return cos(pi * evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi':
        return sin(pi * evaluate_random_function(f[1], x, y))
    elif f[0] == 'sqrt_abs':
        return sqrt(abs(evaluate_random_function(f[1], x, y)))
    elif f[0] == 'power':
        return (evaluate_random_function(f[1], x, y))**random.randint(1,10)
    elif f[0] == 'one_over':
        return 1 / (1.1 + abs(evaluate_random_function(f[1], x, y)))
    elif f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    else:
        return 0


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
    return color_code # took off the int in order to make NumPy work


def test_image(filename, x_size=350, y_size=350): # no longer relevant
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size, y_size, timespan):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(10, 13)

    x = np.tile(np.linspace(-1,1, x_size),(y_size,1))   # lines things up nicely
    y = np.tile(np.linspace(-1,1, y_size),(x_size,1)).T
    # Create image and loop over all pixels <--commented out but
    # still able to revert if I modify everything else back to just x, y
    #im = Image.new("RGB", (x_size, y_size))
    #pixels = im.load()
    #for i in range(x_size):
    #    for j in range(y_size):
            #x = remap_interval(i, 0, x_size, -1, 1)
            #y = remap_interval(j, 0, y_size, -1, 1)
    #        x = np.tile(np.linspace(-1,1, x_size),(y_size,1))
    #        y = np.tile(np.linspace(-1,1, y_size),(x_size,1)).T
            #blue_function(x,y) = ((blue_function(x,y) + 1) + (2-(blue_function(x,y) + 1))/2) - 1
            #pixels[i, j] = (
            #        color_map(red_function(x,y)),
            #        color_map(green_function(x,y)),
            #        color_map(((blue_function(x,y) + 1) + (2-(blue_function(x,y) + 1))/1.3) - 1)
            #        color_map(blue_function(x,y))
            #       )
            #
    #im.save(filename)
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
    #doctest.run_docstring_examples(evaluate_random_function, globals())
    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("frame%03d.png",500,500,200)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
