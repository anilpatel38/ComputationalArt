"""Header"""

import random
from PIL import Image

# Lists of functions to grab from
listall = ["prod", "avg", "cos_pi", "sin_pi", "choose_x", "choose_y", "two_x",
           "sqrd"]
list1arg = ["cos_pi", "sin_pi", "sqrt", "sqrd"]


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

    >>> build_random_function(3, 4)
    1
    """
    function = []
    if min_depth <= 1:
        return random.choice("xy")

    else:
        index = random.randint(0, len(listall)-1)
        this_func = listall[index]
        function.append(this_func)
        if this_func in list1arg:
            function.append(build_random_function(min_depth - 1,
                                                  max_depth - 1))
        else:
            function.append(build_random_function(min_depth - 1,
                                                  max_depth - 1))
            function.append(build_random_function(min_depth - 1,
                                                  max_depth - 1))
        return function


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["sin_pi", "x"], 2, 5)
        True
    """
    import math
    if f == "x":
        return x
    if f == "y":
        return y

    if f[0] == "avg":
        arg1 = evaluate_random_function(f[1], x, y)
        arg2 = evaluate_random_function(f[2], x, y)
        res = 0.5*(arg1 + arg2)
        return res

    if f[0] == "prod":
        arg1 = evaluate_random_function(f[1], x, y)
        arg2 = evaluate_random_function(f[2], x, y)
        res = arg1*arg2
        return res

    if f[0] == "cos_pi":
        arg1 = evaluate_random_function(f[1], x, y)
        res = math.cos(arg1 * math.pi)
        return res

    if f[0] == "sin_pi":
        arg1 = evaluate_random_function(f[1], x, y)
        res = math.sin(arg1 * math.pi)
        return res

    if f[0] == "choose_x":
        arg1 = evaluate_random_function(f[1], x, y)
        return arg1

    if f[0] == "choose_y":
        arg2 = evaluate_random_function(f[2], x, y)
        return arg2

    if f[0] == "two_x":
        arg1 = evaluate_random_function(f[1], x, y)
        res = 2*arg1
        return res

    if f[0] == "sqrd":
        arg1 = evaluate_random_function(f[1], x, y)
        res = arg1*arg1
        return res
    else:
        print(f[0])


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
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    interval1 = input_interval_end - input_interval_start
    temp = val - input_interval_start
    fraction = temp / interval1
    interval2 = output_interval_end - output_interval_start
    new_val = fraction*interval2 + output_interval_start
    return new_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
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


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


"""
if __name__ == "__main__":
    import doctest
    doctest.run_docstring_examples(evaluate_random_function, globals(),
                                   verbose=True)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
"""

# Create some computational art!
# TODO: Un-comment the generate_art function call after you
#       implement remap_interval and evaluate_random_function
generate_art("myart2.png")

# Test that PIL is installed correctly
# TODO: Comment or remove this function call after testing PIL install
