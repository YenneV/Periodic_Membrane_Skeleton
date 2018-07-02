#Monte Carlo Type Simulation for multiple structureless spectrin particles in a 2D Cartesian space

import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(10)

# Creating Class for Particles
class Particle:
    def __init__(self, position):
        self.initialposition = position
        self.position = position
    def position(self, newcoords):
        self.position = newcoords

# Initialising a few objects of the class, Particles
spectrin1 = Particle([50,50])
spectrin2 = Particle([20,30])
spectrin3 = Particle([10,10])

# Putting all particles in a list
spectrins = [spectrin1, spectrin2, spectrin3]

# Setting up some parameters for the simulation cell and the number of steps 
xcoords = list(range(100)) #Length 100
ycoords = list(range(100)) #Length 100
steps = list(range(1000)) #1000 Steps

# Function takes a set of x and y values, and an initial position, and takes a step
# in one of 4 randomly chosen directions.
def step(initial, xrange, yrange):
    x = initial[0]
    y = initial[1]

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
    else:
        final = [x,y]
        return final

# Random Walk - particle chosen at random, coordinates read in, 'step' function called
# to take a random step, and coordinates updated for the chosen particle
for i in steps:
    print(i)
    mover = (random.choice(spectrins))
    initial_position = mover.position
    print(mover.position)
    final_position = step(initial_position, xcoords, ycoords)
    mover.position = final_position
    print(mover.position)
    if i%10 == 0:
        with open('coords{}.txt'.format(i), 'w') as f:
            f.write(str(spectrin1.position[0]))
            f.write(" ")
            f.write(str(spectrin1.position[1]))
            f.write('\n')
            f.write(str(spectrin2.position[0]))
            f.write(" ")
            f.write(str(spectrin2.position[1]))
            f.write('\n')
            f.write(str(spectrin3.position[0]))
            f.write(" ")
            f.write(str(spectrin3.position[1]))
            f.write('\n')


















# OLD CODE - KEEP AS MAY NEED LATER ON
# Data structures that I will be applying my functions to
#occupation_status = np.zeros([len(xcoords),len(ycoords)], dtype=int)
#coordinates = np.zeros([len(spectrins),2], dtype = int)


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