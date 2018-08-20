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
    def parametrise(self):
        self.deltax = self.pointC[0] - self.pointA[0] # x component of direction vector from A to C
        self.deltay = self.pointC[1] - self.pointA[1] # y component of direction vector from A to C
        points = list(range(0,self.length + 1))
        linecoords = []
        for t in points:
            xpoint = self.pointA[0] + t*(self.deltax/self.length)
            ypoint = self.pointA[1] + t*(self.deltay/self.length)
            linecoords.append([xpoint,ypoint])
        return linecoords #List of points generated is length + 1 as I need both endpoints
    def neighbourlist(self):
        neighbours = []
        for i in range(0,len(Particle.instances)):
            deltax = abs(Particle.instances[i].position[0] - self.position[0])
            deltay = abs(Particle.instances[i].position[1] - self.position[1])
            distance = math.sqrt(deltax**2 + deltay**2)
            if distance < (self.length + 2*self.radius) and distance > 0:
                neighbours.append(Particle.instances[i])
            else:
                continue
        return neighbours
    def neighbourdist(self, other):
        set1 = self.parametrise()
        set2 = other.parametrise()
        overlap = False
        for i in range(0,len(set1)):
            for j in range(0,len(set2)):
                deltax = abs(set1[i][0] - set2[j][0])
                deltay = abs(set1[i][1] - set2[j][1])
                distance = math.sqrt(deltax**2 + deltay**2)
                if distance < 2*self.radius:
                    overlap = True
                    return overlap #the return statement here should stop everything if condition is true
                else:
                    continue #if condition is false then we continue to iterate
        return overlap



# SETTING UP INITIAL VALUES AND INITIALISING PARTICLES
# Setting up some parameters for the simulation cell and the number of steps 
xcoords = list(range(100)) #Length of cell in x direction
ycoords = list(range(100)) #Length of cell in y direction
steps = list(range(10)) #Number of steps in my random walk
# Initialising a few objects (IN FUTURE I'LL NEED TO AUTOMATE THIS SO WE HAVE MANY PARTICLES)
rod1 = Particle([88,88], 10, 2, 0)
rod1.whereami([88,88], 0)
rod2 = Particle([30,30], 10, 2, (math.pi/6))
rod2.whereami([30,30], (math.pi/6))
rod3 = Particle([10,10], 10, 2, (math.pi))
rod3.whereami([10,10], (math.pi))

thing = rod1.neighbourdist(rod2)
print(thing)



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
# the move is accepted and false if it is not
def validate(mover, trial_move, xrange, yrange):
    #find the valid range of x values for any move, and same for y, and return as list
    validx = list(range((min(xrange) + mover.radius), (max(xrange) - mover.radius))) 
    validy = list(range((min(yrange) + mover.radius), (max(yrange) - mover.radius)))
    mover.whereami(trial_move[0:2], trial_move[2]) #Runs function on trial move to update coords of A,B,C points
    #moverID = (Particle.instances.index(mover)) #Gives me the index in the class instance list for the moving particle
    accept = False
    if (int(mover.pointA[0])) not in validx:
        accept = False
    elif (int(mover.pointC[0])) not in validx:
        accept = False
    elif (int(mover.pointA[1])) not in validy:
        accept = False
    elif (int(mover.pointC[1])) not in validy:
        accept = False
    #if (int(mover.pointA[0])) or (int(mover.pointC[0])) not in validx:
    #    accept = False
    #    print('step rejected - xcoordinate out of range')
    #elif ((int(mover.pointA[1]) or int(mover.pointC[1])) not in validy:
    #    accept = False
    #    print('step rejected - ycoordinate out of range')
    else:
        accept = True
        print('accepted with endpoints at:')
        print(mover.output)
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
        print('move allowed')
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
            