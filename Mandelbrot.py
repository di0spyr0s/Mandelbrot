'''
Renders mandelbrot visualization to image using PIL.
'''

import PIL.Image
from multiprocessing import Pool

ITERATIONS = 600


def escape_value(((x,y), C)):
    '''
    Tests whether complex number 'C' is in the set. 
    Returns grid coordinates and number of iterations before escape. If C is in set,
    returns grid coordinates and global variable ITERATIONS.
    '''
    Z = 0
    num_iterations = 0
    while num_iterations < ITERATIONS:
        if abs(Z) > 2:
            break
        Z = Z ** 2 + C
        num_iterations += 1
    return (x, y), num_iterations

def pixel_coordinate_to_complex(x, y, width, height, top_left = (-2, 1), complex_width = 3.0, complex_height = 2.0):
        '''
        Translates graph coordinates (x,y) in image size (width, height)
        to complex number. Returns complex number.
        '''
        return complex(top_left[0] + complex_width/width * x, top_left[1] - complex_height/height * y)   

def get_color(num_iterations):
    '''
    takes number of iterations before escape and returns an HSV color. 
    if number is greater than 600, returns black
    '''
    if num_iterations < 600:
        # Cycle through hue wheel multiple times to create narrower bands of color
        hsv = num_iterations  % (360 / 6)
        return (int(hsv * 6), 360, 360)
    else:
        return (0, 0, 0)

def render(width, height, top_left = (-2, 1), complex_width = 3.0, complex_height = 2.0):
    '''
    given width and height of image, returns an image of mandelbrot set.
    '''
    mandel = PIL.Image.new('HSV', (width, height))
    # For each grid coordinate create tuple in form ((x,y), C)
    # and append to list 'l' for input into pool.map()
    coord_complex_pairs = [] 
    for y in range(height):
        for x in range(width):
            C = pixel_coordinate_to_complex(x, y, width, height, top_left, complex_width, complex_height)
            coord_complex_pairs.append(((x,y), C))
    pool = Pool()
    # Create dictionary in form (x,y): number of iterations before escape
    results = dict(pool.map(escape_value, coord_complex_pairs))     
    for x,y in results:
        color = get_color(results[x,y])
        mandel.putpixel((x, y), color)
    mandel.show()
    
render(960, 640, (-0.8, 0.5), 0.25, 0.11)
