#Monte Carlo Type Simulation for multiple structureless spectrin particles in a 2D Cartesian space

import numpy as np
import math
import matplotlib.pyplot as plt
import random
random.seed(10)

# Creating Class for Particles
class Particle:
    instances = []
    def __init__(self, position, radius):
        self.initialposition = position
        self.position = position
        self.radius = radius
        Particle.instances.append(self) #Beware! If I need to delete particles later they won't be removed from this list!
    def position(self, newcoords):
        self.position = newcoords
    def proximity(self, other):
        deltax = abs(other.position[0] - self.position[0])
        deltay = abs(other.position[1] - self.position[1])
        distance = math.sqrt(deltax**2 + deltay**2)
        return distance

# Initialising a few objects of the class, Particles
spectrin1 = Particle([50,50], 10)
spectrin2 = Particle([20,30], 10)
spectrin3 = Particle([10,10], 10)

# Setting up some parameters for the simulation cell and the number of steps 
xcoords = list(range(100)) #Length 100
ycoords = list(range(100)) #Length 100
steps = list(range(10000)) #10000 Steps
mindist = 20 #Circular particles radius assumed to be 10 at the minute


# 'step' function generates a trial move, based on an initial position
def step(initial):
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

    trial = [x,y]
    return trial

# Function takes a particle, a trial move and the cell limits, and returns true if 
# the move is accepted and false if it is not (because it leaves the cell or gets 
# too close to another particle
def validate(mover, trial_move, xrange, yrange):
    x = trial_move[0]
    y = trial_move[1]
    #find the valid range of x values for any move, and same for y, and return as list
    validx = list(range((min(xrange) + mover.radius), (max(xrange) - mover.radius))) # new part 
    validy = list(range((min(yrange) + mover.radius), (max(yrange) - mover.radius))) # new part
    mover.position = trial_move
    moverID = (Particle.instances.index(mover)) #Gives me the index in the class instance list for the moving particle
    iterations = list(range(0,3)) #List of 0,1,2 - think of a better way of doing this
    distances = np.zeros([1,3], dtype = float) #Array to hold distances of all particles from the mover
    for j in iterations:
        distances[:,j] = (Particle.instances[moverID].proximity(Particle.instances[j]))
    neighbourdist = distances[distances != 0]
    closest = np.min(neighbourdist)
    print(closest)
    accept = True
    if x not in validx or y not in validy:
        accept = False
        print('step rejected - out of range')
    elif closest < mindist:
        accept = False
        print('step rejected - overlaps another particle')
    else:
        accept = True
    return accept

# Random Walk - particle chosen at random, coordinates read in, 'step' function called
# to take a trial step, 'validate' function called to say if ok or not, coordinates updated accordingly
for i in steps:
    print(i)
    mover = (random.choice(Particle.instances)) #Selects a particle to move
    initial_position = mover.position
    trial_move = step(initial_position)
    accept = validate(mover, trial_move, xcoords, ycoords) # function to return a yes or no
    if accept == True:
        mover.position = trial_move
        print('move allowed to:')
        print(mover.position)
    else:
        mover.position = initial_position
        print('move not allowed, remains at:')
        print(mover.position)
    if i%10 == 0:
        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Multi_Sphere\coords{}.txt'.format(i), 'w') as f:
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