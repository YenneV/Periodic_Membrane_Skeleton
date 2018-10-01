#Monte Carlo Type Simulation for multiple rodlike objects in a 2D Cartesian space

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
random.seed(10)

# Creating Class for 3 dimensional, rigid rod-like objects
class RigidRod:
    instances = []
    def __init__(self, position, length, radius, alpha, beta):
        self.initialposition = position
        self.length = length #rounded ends so this is total length-2R
        self.radius = radius
        self.initialalpha = alpha #Angle between z axis and rod orientation in radians
        self.initialbeta = beta #Angle between x axis (in xy plane) and rod orientation in radians
        RigidRod.instances.append(self) #Beware! If I need to delete particles later they won't be removed from this list!
    def whereami(self, newcoords, alpha, beta):
        self.position = newcoords
        self.alpha = alpha
        self.beta = beta
        self.projectedlength = self.length*(math.cos((math.pi/2) - abs(self.alpha)))
        #Setting angles alpha and beta to acceptable range (-pi to +pi)
        if self.alpha > math.pi:
            self.alpha = self.alpha - 2*math.pi
        elif self.alpha < -math.pi:
            self.alpha = self.alpha + 2*math.pi
        elif self.beta > math.pi:
            self.beta = self.beta - 2*math.pi
        elif self.beta < - math.pi:
            self.beta = self.beta + 2*math.pi
        #Finding the end points depending on the angles for x and y
        if math.pi/2 > self.beta >= 0:
            self.Ax = -abs((self.projectedlength*math.cos(self.beta))/2)  #This should be the amount that we go back in x by to get left pt
            self.Ay = -abs((self.projectedlength*math.sin(self.beta))/2) #as above for y
            self.Cx = abs((self.projectedlength*math.cos(self.beta))/2)  #amount we go along in x by to get right pt
            self.Cy = abs((self.projectedlength*math.sin(self.beta))/2) #as above for y
        elif math.pi >= self.beta >= math.pi/2:
            self.Ax = abs((self.projectedlength*math.cos(self.beta))/2)  
            self.Ay = -abs((self.projectedlength*math.sin(self.beta))/2)
            self.Cx = -abs((self.projectedlength*math.cos(self.beta))/2) 
            self.Cy = abs((self.projectedlength*math.sin(self.beta))/2)
        elif (-math.pi)/2 > self.beta >= -math.pi: 
            self.Ax = abs((self.projectedlength*math.cos(self.beta))/2)  
            self.Ay = abs((self.projectedlength*math.sin(self.beta))/2)
            self.Cx = -abs((self.projectedlength*math.cos(self.beta))/2) 
            self.Cy = -abs((self.projectedlength*math.sin(self.beta))/2)
        elif 0 > self.beta >= (-math.pi/2): 
            self.Ax = -abs((self.projectedlength*math.cos(self.beta))/2)  
            self.Ay = abs((self.projectedlength*math.sin(self.beta))/2)
            self.Cx = abs((self.projectedlength*math.cos(self.beta))/2) 
            self.Cy = -abs((self.projectedlength*math.sin(self.beta))/2)
        #Repeating for z coordinates
        if math.pi/2 > self.alpha >= 0:
            self.Az = -abs((self.length*math.cos(self.alpha))/2)
            self.Cz = abs((self.length*math.cos(self.alpha))/2)
        elif math.pi >= self.alpha >= math.pi/2:
            self.Az = abs((self.length*math.cos(self.alpha))/2)
            self.Cz = -abs((self.length*math.cos(self.alpha))/2)
        elif (-math.pi)/2 > self.alpha >= - math.pi:
            self.Az = abs((self.length*math.cos(self.alpha))/2)
            self.Cz = -abs((self.length*math.cos(self.alpha))/2)
        elif 0 > self.alpha >= (-math.pi/2):
            self.Az = -abs((self.length*math.cos(self.alpha))/2)
            self.Cz = abs((self.length*math.cos(self.alpha))/2)
        # Locating coordinates of the endpoint A and C based on centre of mass and delta x, y and z
        self.pointA = [(self.position[0] + self.Ax), (self.position[1] + self.Ay), (self.position[2] + self.Az)]
        self.pointC = [(self.position[0] + self.Cx), (self.position[1]+ self.Cy), (self.position[2] + self.Cz)]
        self.output = self.pointA, self.pointC
    def parametrise(self):
        self.deltax = self.pointC[0] - self.pointA[0] # x component of direction vector from A to C
        self.deltay = self.pointC[1] - self.pointA[1] # y component of direction vector from A to C
        self.deltaz = self.pointC[2] - self.pointA[2] # z component of direction vector from A to C
        points = list(range(0,self.length + 1))
        linecoords = []
        for t in points:
            xpoint = self.pointA[0] + t*(self.deltax/self.length)
            ypoint = self.pointA[1] + t*(self.deltay/self.length)
            zpoint = self.pointA[2] + t*(self.deltaz/self.length)
            linecoords.append([xpoint,ypoint,zpoint])
        return linecoords #List of points generated is length + 1 as I need both endpoints
    def neighbourlist(self):
        neighbours = []
        #selfID = (RigidRod.instances.index(self))
        #print('self ID is', selfID)
        for i in range(0,len(RigidRod.instances)):
            deltax = abs(RigidRod.instances[i].position[0] - self.position[0])
            deltay = abs(RigidRod.instances[i].position[1] - self.position[1])
            distance = math.sqrt(deltax**2 + deltay**2)
            if distance < (self.length + 2*self.radius):
                neighbours.append(RigidRod.instances[i])
            else:
                continue
        neighbours.remove(self)
        return neighbours
    def neighbourdist(self, other):
        set1 = self.parametrise()
        set2 = other.parametrise()
        overlap = False
        for i in range(0,len(set1)):
            for j in range(0,len(set2)):
                deltax = abs(set1[i][0] - set2[j][0])
                deltay = abs(set1[i][1] - set2[j][1])
                deltaz = abs(set1[i][2] - set2[j][2])
                distance = math.sqrt(deltax**2 + deltay**2 + deltaz**2)
                if distance < 2*self.radius:
                    overlap = True
                    return overlap #the return statement here should stop everything if condition is true
                else:
                    continue #if condition is false then we continue to iterate
        return overlap



## FUNCTION DEFINITIONS ##

# 'step' function generates a trial move of either a displacement or orientational change in 3D space
def step(initial, alpha, beta):
    x = initial[0]
    y = initial[1]
    z = initial[2]

    step = random.randint(0,9)
    if step == 0:
        x += 1
    elif step == 1:
        x -= 1
    elif step == 2:
        y += 1
    elif step == 3:
        y -= 1
    elif step == 4:
        z += 1
    elif step == 5:
        z -= 1
    elif step == 6:
        alpha += (math.pi/180)
    elif step == 7:
        alpha -= (math.pi/180)
    elif step == 8:
        beta += (math.pi/180)
    elif step == 9:
        beta -= (math.pi/180)
    else: #Not really necessary but just to make sure rand is drawn in range
        print('Step error - out of range')

    trial = [x,y,z,alpha,beta]
    return trial


# 'overlap' function takes a particle and uses neighbourlist and neighbourdist methods to figure out 
# if this particle is too close to any other particle - [should only be called during validate as the 
# whereami method needs to be called first to update position to trial move]
def overlap(mover):
    neighbours = mover.neighbourlist()
    result = False
    for i in range(0,len(neighbours)):
        result = mover.neighbourdist(neighbours[i])
        if result == True:
            return result
        else:
            continue
    return result

# 'transform' function takes a vector of x,y,z Cartesian coordinates and returns a vector of cylindrical coords
def transform(cart_coords):
    x = cart_coords[0]
    y = cart_coords[1]
    z = cart_coords[2]

    r = math.sqrt(x**2 + y**2)
    theta = math.atan(y/x)
    z = z

    cyl_coords = [r,theta,z]
    return cyl_coords


# 'validate' function tests to see whether a particle remains within the cell for a given trial move
def validate(mover, trial_move, radius, length):
    # These are the minimum and maximum endpoint positions allowed in r and z
    minr = -radius + mover.radius
    maxr = radius - mover.radius
    minz = 0 + mover.radius
    maxz = length - mover.radius
    # Particle position and orientation updated with trial move coordinates (Cartesian)
    mover.whereami(trial_move[0:3], trial_move[3], trial_move[4])
    # Cartesian coordinates need transforming to cylindrical
    # ACTUALLY I NEED TO DO THIS WITH THE ENDPOINTS, NOT THE CENTREPOINT!
    cylcoordsA = transform(mover.pointA[0:3])
    cylcoordsC = transform(mover.pointC[0:3])
    rA = cylcoordsA[0]
    zA = cylcoordsA[2]
    rC = cylcoordsC[0]
    zC= cylcoordsC[2]
    # if else statements to check if move allowed
    accept = False
    if rA < minr:
        accept = False
        print('A point out of bounds in r')
    elif rA > maxr:
        accept = False
        print('A point out of bounds in r')
    elif rC < minr:
        accept = False
        print('C point out of bounds in r')
    elif rC > maxr:
        accept = False
        print('C point out of bounds in r')
    elif zA < minz:
        accept = False
        print('A point out of bounds in z')
    elif zA > maxz:
        accept = False
        print('A point out of bounds in z')
    elif zC < minz:
        accept = False
        print('C point out of bounds in z')
    elif zC > maxz:
        accept = False
        print('C point out of bounds in z')
    elif overlap(mover) == True:
        accept = False
        print('trial move would overlap another particle')
    else:
        accept = True
        #print('accepted with endpoints at:')
        #print(mover.output)
    return accept

## END OF FUNCTION DEFINITIONS ##

# SETTING UP INITIAL VALUES
# Setting up some parameters for simulation cell and steps
cellradius = 50 #radius of axon, r coordinate
celllength = 100 #length of axon, z coordinate
steps = list(range(10)) #Number of steps in my random walk

## INITIALISING PARTICLES
length = 10
radius = 2
nparticles = 25 #number of rod particles
edge = radius + (length/2) #the amount of space we need to leave between centrepoint and edges


## CREATING PARTICLES
for i in range(1,nparticles + 1):
    print('particle no', i)
    #maybe start in cylindrical coords, choose r, z and theta in range for position, then alpha and beta
    #for orientation, with all the necessary restrictions, then switch the r,z,theta to x,y,z and continue
    startr = random.uniform(-cellradius + edge, cellradius - edge)
    print('r coordinate', startr)
    starttheta = random.uniform(0, 2*math.pi)
    print('theta', starttheta)
    startz = random.uniform(0 + edge, celllength - edge)
    print('z coordinate', startz)
    start_cart = transform([startr,starttheta,startz])
    startalpha = random.uniform(-math.pi, math.pi)
    print('alpha', startalpha)
    startbeta = random.uniform(-math.pi, math.pi)
    print('beta', startbeta)
    varname = 'rod{}'.format(i)
    varname = RigidRod(start_cart, length, radius, startalpha, startbeta)
    varname.whereami(start_cart, startalpha, startbeta)
    status = overlap(varname)
    while status == True:
        #print('coordinates not within range')
        newr = random.uniform(-cellradius + edge, cellradius - edge)
        newtheta = random.uniform(0, 2*math.pi)
        newz = random.uniform(0 + edge, celllength - edge)
        new_cart = transform([newr,newtheta,newz])
        newalpha = random.uniform(-math.pi, math.pi)
        newbeta = random.uniform(-math.pi, math.pi)
        varname.whereami(new_cart, newalpha, newbeta)
        #print('new position to try', varname.pointA, varname.pointC)
        status = overlap(varname)
        print('status is', status)







## MAIN FUNCTION ##
# Random Walk - particle chosen at random, coordinates read in, 'step' function called
# to take a trial step, 'validate' function called to say if ok or not, coordinates updated accordingly
#for i in steps:
#    print(i)
#    mover = (random.choice(RigidRod.instances)) #Selects a particle to move
#    initial_position = mover.position
#    initial_angle = mover.orientation
#    trial_move = step(initial_position, initial_angle) #Returns list of [x,y,orientation]
#    accept = validate(mover, trial_move, xcoords, ycoords) # function to return a yes or no
#    if accept == True:
#        mover.whereami(trial_move[0:2], trial_move[2])
#        #print('move allowed')
#    else:
#        mover.whereami(initial_position, initial_angle)
#        #print('move not allowed, remains at:')
#        #print(mover.position)
#    if i%10000 == 0:
#        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Rigid_Rods\coords{}.txt'.format(i), 'w') as f:
#            for j in RigidRod.instances:
#                f.write(str(j.pointA[0]))
#                f.write(" ")
#                f.write(str(j.pointA[1]))
#                f.write(" ")
#                f.write(str(j.pointC[0]))
#                f.write(" ")
#                f.write(str(j.pointC[1]))
#                f.write('\n')
    
# CREATING TEST PLOT
# NEED TO USE VECTOR RETURNED FROM WALK TO DO A 3D PLOT OF THE POINTS 
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#x = [7.5, 12.5]
#y = [7.5, 2.5]
#z = [5.34, -1.54]
#ax.plot(x,y,z)
#plt.show()