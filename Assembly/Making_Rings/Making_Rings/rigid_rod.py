#Monte Carlo Type Simulation for multiple rodlike objects in a 2D Cartesian space

import numpy as np
import math
import matplotlib.pyplot as plt
import random
random.seed(10)

# Creating Class for rod-like objects
class Particle:
    instances = []
    def __init__(self, position, length, radius, orientation):
        self.initialposition = position
        self.length = length #rounded ends so this is total length-2R
        self.radius = radius
        self.initialorientation = orientation #Angle in radians
        Particle.instances.append(self) #Beware! If I need to delete particles later they won't be removed from this list!
    def whereami(self, newcoords, orientation):
        self.position = newcoords
        self.orientation = orientation
        if self.orientation >= 2*math.pi: #This keeps the angle between 0 and less than 2pi
            self.orientation = self.orientation - 2*math.pi
        #Finding the end points depending on the angle
        if math.pi/2 > self.orientation >= 0:
            self.Ax = -(self.length*math.cos(self.orientation))/2  #This should be the amount that we go back in x by to get left pt
            self.Ay = -(self.length*math.sin(self.orientation))/2 #as above for y
            self.Cx = (self.length*math.cos(self.orientation))/2  #amount we go along in x by to get right pt
            self.Cy = (self.length*math.sin(self.orientation))/2 #as above for y
        elif math.pi >= self.orientation >= math.pi/2:
            self.Ax = (self.length*math.cos(self.orientation))/2  
            self.Ay = -(self.length*math.sin(self.orientation))/2
            self.Cx = -(self.length*math.cos(self.orientation))/2 
            self.Cy = (self.length*math.sin(self.orientation))/2
        elif (3*math.pi)/2 > self.orientation >= math.pi:
            self.Ax = (self.length*math.cos(self.orientation))/2  
            self.Ay = (self.length*math.sin(self.orientation))/2
            self.Cx = -(self.length*math.cos(self.orientation))/2 
            self.Cy = -(self.length*math.sin(self.orientation))/2
        elif (2* math.pi) > self.orientation >= (3*math.pi)/2:
            self.Ax = -(self.length*math.cos(self.orientation))/2  
            self.Ay = (self.length*math.sin(self.orientation))/2
            self.Cx = (self.length*math.cos(self.orientation))/2 
            self.Cy = -(self.length*math.sin(self.orientation))/2
        # Locating coordinates of the endpoint A and C based on centre of mass and delta x and y
        self.pointA = [(self.position[0] + self.Ax), (self.position[1] + self.Ay)]
        self.pointC = [(self.position[0] + self.Cx), (self.position[1]+ self.Cy)]
        self.output = self.pointA, self.pointC
    def proximity(self, other): #this is between centres of mass - i may not need this if i use a grid
        deltax = abs(other.position[0] - self.position[0])
        deltay = abs(other.position[1] - self.position[1])
        distance = math.sqrt(deltax**2 + deltay**2)
        return distance

# Setting up some parameters for the simulation cell and the number of steps 
xcoords = list(range(100)) #Length 100
ycoords = list(range(100)) #Length 100
steps = list(range(10000)) #10000 Steps
#occ_grid = np.zeros((len(xcoords), len(ycoords)), dtype = bool) #grid of 'False' values for occupation

# Initialising a few objects (IN FUTURE I'LL NEED TO AUTOMATE THIS SO WE HAVE MANY PARTICLES)
rod1 = Particle([50,50], 10, 2, 0)
rod1.whereami([50,50], 0)
rod2 = Particle([20,30], 10, 2, (math.pi/6))
rod2.whereami([20,30], (math.pi/6))
rod3 = Particle([10,10], 10, 2, (math.pi/4))
rod3.whereami([10,10], (math.pi/4))


# 'step' function generates a trial move, based on an initial position
def step(initial, angle):
    x = initial[0]
    y = initial[1]

    step = random.randint(0,4)
    if step == 0:
        x += 1
    elif step == 1:
        x -= 1
    elif step == 2:
        y += 1
    elif step == 3:
        y -= 1
    elif step == 4:
        angle += (math.pi/4)
    else: #Not really necessary but just to make sure rand is drawn in range
        print('Step error - out of range')

    trial = [x,y,angle]
    return trial

# Function takes a particle, a trial move and the cell limits, and returns true if 
# the move is accepted and false if it is not (because it leaves the cell or gets 
# too close to another particle
def validate(mover, trial_move, xrange, yrange):
    x = trial_move[0] #redundant?
    y = trial_move[1] #redundant?
    angle = trial_move[2] #redundant?
    #find the valid range of x values for any move, and same for y, and return as list
    validx = list(range((min(xrange) + mover.radius), (max(xrange) - mover.radius))) # new part 
    validy = list(range((min(yrange) + mover.radius), (max(yrange) - mover.radius))) # new part
    mover.whereami(trial_move[0:2], trial_move[2])
    moverID = (Particle.instances.index(mover)) #Gives me the index in the class instance list for the moving particle
    #iterations = list(range(0,3)) #List of 0,1,2 - think of a better way of doing this
    #distances = np.zeros([1,3], dtype = float) #Array to hold distances of all particles from the mover
    #for j in iterations:
    #    distances[:,j] = (Particle.instances[moverID].proximity(Particle.instances[j]))
    #neighbourdist = distances[distances != 0]
    #closest = np.min(neighbourdist)
    accept = True
    if (int(mover.pointA[0]) or int(mover.pointC[0])) not in validx or (int(mover.pointA[1]) or int(mover.pointC[1])) not in validy:
        accept = False
        print('step rejected - out of range')
    #elif closest < mindist:
    #    accept = False
    #    print('step rejected - overlaps another particle')
    else:
        accept = True
    return accept

# Random Walk - particle chosen at random, coordinates read in, 'step' function called
# to take a trial step, 'validate' function called to say if ok or not, coordinates updated accordingly
for i in steps:
    print(i)
    mover = (random.choice(Particle.instances)) #Selects a particle to move
    initial_position = mover.position
    initial_angle = mover.orientation
    trial_move = step(initial_position, initial_angle) #Returns list of [x,y,orientation]
    accept = validate(mover, trial_move, xcoords, ycoords) # function to return a yes or no
    if accept == True:
        mover.whereami(trial_move[0:2], trial_move[2])
        print('move allowed to:')
        print(mover.position)
    else:
        mover.whereami(initial_position, initial_angle)
        print('move not allowed, remains at:')
        print(mover.position)
    if i%10 == 0:
        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Rigid_Rods\coords{}.txt'.format(i), 'w') as f:
            f.write(str(rod1.pointA[0]))
            f.write(" ")
            f.write(str(rod1.pointA[1]))
            f.write(" ")
            f.write(str(rod1.pointC[0]))
            f.write(" ")
            f.write(str(rod1.pointC[1]))
            f.write('\n')
            f.write(str(rod2.pointA[0]))
            f.write(" ")
            f.write(str(rod2.pointA[1]))
            f.write(" ")
            f.write(str(rod2.pointC[0]))
            f.write(" ")
            f.write(str(rod2.pointC[1]))
            f.write('\n')
            f.write(str(rod3.pointA[0]))
            f.write(" ")
            f.write(str(rod3.pointA[1]))
            f.write(" ")
            f.write(str(rod3.pointC[0]))
            f.write(" ")
            f.write(str(rod3.pointC[1]))
            f.write('\n')
            