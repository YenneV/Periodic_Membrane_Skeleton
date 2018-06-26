#Monte Carlo Type Simulation for multiple structureless spectrin particles in a 2D Cartesian space

import numpy as np
import random
random.seed(10)


# Create some parameters that I can specify
spectrins = list(range(5)) # Number of particles I'd like - This gives the numbers 0 to 4, 5 numbers in total
xcoords = list(range(10)) #Length 10
ycoords = list(range(10)) #Length 10

# Data structures that I will be applying my functions to
occupation_status = np.zeros([len(xcoords),len(ycoords)], dtype=int)
coordinates = np.zeros([len(spectrins),2], dtype = int)

# Setting some initial values - will think of a better way of doing this later on
coordinates[0,:] = [1,1]
coordinates[1,:] = [1,2]
coordinates[2,:] = [1,3]
coordinates[3,:] = [2,1]
coordinates[4,:] = [2,2]

# I also need to initialise my occupation grid...


# Function occupation_check takes a set of xy coordinates and a grid of occupation status
# and returns true if space is free and false if not
def occupation_check(new_coords,occupation_grid):
    x = new_coords[0]
    y = new_coords[1]

    if occupation_grid[x,y] == 0:
        return True #Indicates space is free
    else:
        return False #Indicates space is occupied

# Next I need a function that just updates the occupation grid once I've approved a move
def occupation_update(old_coords,new_coords,occupation_grid):
    old_x = old_coords[0]
    old_y = old_coords[1]
    new_x = new_coords[0]
    new_y = new_coords[1]

    occupation_grid[old_x,old_y] = 0
    occupation_grid[new_x,new_y] = 1
    return occupation_grid

# Function for generating a trial move and testing if it's ok based on range, occupation status
# and initial coordinates
def multistep(initial, xrange, yrange, occupation_grid):
    x = initial[0]
    print('x is initially')
    print(x)
    y = initial[1]
    print('y is initially')
    print(y)

    step = random.randint(0,3)
    if step == 0:
        x += 1
    elif step == 1:
        x -= 1
    elif step == 2:
        y += 1
    elif step == 3:
        y -= 1
    else: #Not really necessary but just to make sure rand is drawn in range
        print('Step error - out of range')

    if x not in xrange or y not in yrange:
        x = initial[0]
        y = initial[1]
        print('step rejected - out of range')
        final = [x,y]
        return final
    elif occupation_grid[x,y] == 1:
        x = initial[0]
        y = initial[1]
        print('position already occupied')
        final = [x,y]
        return final
    else:
        final = [x,y]
        return final