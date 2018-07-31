#Monte Carlo Type Simulation for multiple rodlike objects in a 2D Cartesian space

import numpy as np
import math
import matplotlib.pyplot as plt
import random
random.seed(10)

# Creating Class for rod-like objects
class Particle:
    instances = []
    def __init__(self, position, length, width):
        self.initialposition = position
        self.position = position
        self.length = length
        self.width = width
        min_x = self.position[0] - (int(0.5*self.length))
        max_x = self.position[0] + (int(0.5*self.length))
        min_y = self.position[1] - (int(0.5*self.width))
        max_y = self.position[1] + (int(0.5*self.width))
        Particle.instances.append(self) #Beware! If I need to delete particles later they won't be removed from this list!
    def position(self, newcoords):
        self.position = newcoords
        self.min_x = self.position[0] - (int(0.5*self.length))
        self.max_x = self.position[0] + (int(0.5*self.length))
        self.min_y = self.position[1] - (int(0.5*self.width))
        self.max_y = self.position[1] + (int(0.5*self.width))
    def proximity(self, other): #this is between centres of mass - i may not need this if i use a grid
        deltax = abs(other.position[0] - self.position[0])
        deltay = abs(other.position[1] - self.position[1])
        distance = math.sqrt(deltax**2 + deltay**2)
        return distance

# Setting up some parameters for the simulation cell and the number of steps 
xcoords = list(range(100)) #Length 100
ycoords = list(range(100)) #Length 100
steps = list(range(10000)) #10000 Steps
occ_grid = np.zeros((len(xcoords), len(ycoords)), dtype = bool) #grid of 'False' values for occupation

# Initialising a few objects of the class, Particles
rod1 = Particle([50,50], 10, 2)
rod2 = Particle([20,30], 10, 2)
rod3 = Particle([10,10], 10, 2)

# A function to take a particle and a position, calculate the XV and check if grid spaces are free
def xv_calc(particle, coordinates):
        

# A function to take a particle and a position and change it's positions to false

# A function to take a particle and a position and change it's position to true

# Initialise grid?
def grid_check(particle):
    for i in range(particle.min_x, particle.max_x):
        for j in range(particle.min_y, particle.max_y):
            occ_grid[i,j] = True
    return occ_grid


# Need a list of particles to iterate over too...
for i in range(min_x, max_x):
    for j in range(min_y, max_y):
        occ_grid[i,j] = True


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
#def validate(mover, trial_move, xrange, yrange):
#    x = trial_move[0]
#    y = trial_move[1]
#    #find the valid range of x values for any move, and same for y, and return as list
#    validx = list(range((min(xrange) + mover.radius), (max(xrange) - mover.radius))) # new part 
#    validy = list(range((min(yrange) + mover.radius), (max(yrange) - mover.radius))) # new part
#    mover.position = trial_move
#    moverID = (Particle.instances.index(mover)) #Gives me the index in the class instance list for the moving particle
#    iterations = list(range(0,3)) #List of 0,1,2 - think of a better way of doing this
#    distances = np.zeros([1,3], dtype = float) #Array to hold distances of all particles from the mover
#    for j in iterations:
#        distances[:,j] = (Particle.instances[moverID].proximity(Particle.instances[j]))
#    neighbourdist = distances[distances != 0]
#    closest = np.min(neighbourdist)
#    print(closest)
#    accept = True
#    if x not in validx or y not in validy:
#        accept = False
#        print('step rejected - out of range')
#    elif closest < mindist:
#        accept = False
#        print('step rejected - overlaps another particle')
#    else:
#        accept = True
#    return accept

# Random Walk - particle chosen at random, coordinates read in, 'step' function called
# to take a trial step, 'validate' function called to say if ok or not, coordinates updated accordingly
#for i in steps:
#    print(i)
#    mover = (random.choice(Particle.instances)) #Selects a particle to move
#    initial_position = mover.position
#    trial_move = step(initial_position)
#    accept = validate(mover, trial_move, xcoords, ycoords) # function to return a yes or no
#    if accept == True:
#        mover.position = trial_move
#        print('move allowed to:')
#        print(mover.position)
#    else:
#        mover.position = initial_position
#        print('move not allowed, remains at:')
#        print(mover.position)
#    if i%10 == 0:
#        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Rigid_Rods\coords{}.txt'.format(i), 'w') as f:
#            f.write(str(spectrin1.position[0]))
#            f.write(" ")
#            f.write(str(spectrin1.position[1]))
#            f.write('\n')
#            f.write(str(spectrin2.position[0]))
#            f.write(" ")
#            f.write(str(spectrin2.position[1]))
#            f.write('\n')
#            f.write(str(spectrin3.position[0]))
#            f.write(" ")
#            f.write(str(spectrin3.position[1]))
#            f.write('\n')
