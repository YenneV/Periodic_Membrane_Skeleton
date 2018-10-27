#3D Rigid Rod Random Walk and calculation of nematic order parameter
#FOR PARALLEL USE ON SHARC

import numpy as np
import math
import random
random.seed()

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
    def vectorise(self): #vectorise as nematic
        self.deltax = self.pointC[0] - self.pointA[0] # x component of direction vector from A to C
        self.deltay = self.pointC[1] - self.pointA[1] # y component of direction vector from A to C
        self.deltaz = self.pointC[2] - self.pointA[2] # z component of direction vector from A to C
        self.polarvec = [(self.pointC[0] - self.pointA[0]), (self.pointC[1] - self.pointA[1]), (self.pointC[2] - self.pointA[2])]
        self.vector = [(self.pointC[0] - self.pointA[0]), (self.pointC[1] - self.pointA[1]), (self.pointC[2] - self.pointA[2])] # vector components
        self.magnitude = math.sqrt(self.deltax**2 + self.deltay**2 + self.deltaz**2) # vector magnitude
        reversevec = [(self.pointA[0] - self.pointC[0]), (self.pointA[1] - self.pointC[1]), (self.pointA[2] - self.pointC[2])]
        if self.deltaz < 0: #changed from deltay to deltaz
            self.vector = reversevec
        elif self.deltaz == 0 and self.deltax < 0:
            self.vector = reversevec
        elif self.deltaz == 0 and self.deltax == 0 and self.deltay <0:
            self.vector = reversevec
        self.unitvector = [self.vector[0]/self.magnitude, self.vector[1]/self.magnitude, self.vector[2]/self.magnitude]
        self.polarunit = [self.polarvec[0]/self.magnitude, self.polarvec[1]/self.magnitude, self.polarvec[2]/self.magnitude]
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

# 'particle_creation' takes the number of particles, their dimensions, and those of the cell and 
# places them randomly within the space
# NOTE - NO EXCEPTIONS WRITTEN SO IT WILL NOT TIME OUT IF THEY CANNOT BE PLACED!
def particle_creation(nparticles, length, radius, celllength, cellradius):
    for i in range(1,nparticles + 1):
        #print('particle no', i)
        edge = radius + (length/2)
        #choosing some random cylindrical coordinates
        startr = random.uniform(0 + edge, cellradius - edge)
        starttheta = random.uniform(0, 2*math.pi)
        startz = random.uniform(0 + edge, celllength - edge)
        start_cyl = [startr,starttheta,startz]
        #converting to cartesian
        start_cart = transform_cylcar([startr,starttheta,startz]) 
        #alpha and beta determine the orientation of the rod
        startalpha = random.uniform(-math.pi, math.pi)
        startbeta = random.uniform(-math.pi, math.pi)
        #creating a rod with these coords
        varname = 'rod{}'.format(i)
        varname = RigidRod(start_cart, length, radius, startalpha, startbeta)
        varname.whereami(start_cart, startalpha, startbeta)
        initial_coords = [start_cart[0], start_cart[1], start_cart[2], startalpha, startbeta]
        status = validate(varname, initial_coords, cellradius, celllength)
        #status = overlap(varname)
        while status == False:
            #print('coordinates not within range')
            newr = random.uniform(0 + edge, cellradius - edge)
            #print('new r value is', newr)
            newtheta = random.uniform(0, 2*math.pi)
            newz = random.uniform(0 + edge, celllength - edge)
            #print('new z value is', newz)
            new_cart = transform_cylcar([newr,newtheta,newz])
            newalpha = random.uniform(-math.pi, math.pi)
            newbeta = random.uniform(-math.pi, math.pi)
            varname.whereami(new_cart, newalpha, newbeta)
            new_coords = [new_cart[0], new_cart[1], new_cart[2], newalpha, newbeta]
            #print('new position to try', varname.pointA, varname.pointC)
            status = validate(varname, new_coords, cellradius, celllength)

# 'random_walk' function calls particle_creation to generate some particles, then chooses one randomly
# and calls 'step' to take a trial step then 'validate' to check that this is an allowed move,
# coordinates and orientation updated if particle moved 
def random_walk(nparticles, length, radius, celllength, cellradius, steps):
    particle_creation(nparticles, length, radius, celllength, cellradius)
    for i in steps:
        #print('step number is', i)
        mover = (random.choice(RigidRod.instances)) #Selects a particle to move
        initial_position = mover.position
        #print('initial position is', initial_position)
        initial_alpha = mover.alpha
        initial_beta = mover.beta
        trial_move = step(initial_position, initial_alpha, initial_beta) #Returns list of [x,y,z,alpha,beta]
        #print('trial position is', trial_move)
        accept = validate(mover, trial_move, cellradius, celllength) # function to return a yes or no
        if accept == True:
            mover.whereami(trial_move[0:3], trial_move[3], trial_move[4])
            #print('move allowed')
        else:
            mover.whereami(initial_position, initial_alpha, initial_beta)
            #print('move not allowed, remains at:')
            #print(mover.position)
        #if i%1000 == 0: #code to print out placement of rod endpoints to a text file
        #    with open('D:\Code\Assembly\PMS_PY\Making_Rings\Results\Rigid_Rods_3D\Testing\coords{}.txt.'.format(i), 'w') as f:
        #        for j in RigidRod.instances:
        #            f.write(str(j.pointA[0]))
        #            f.write(" ")
        #            f.write(str(j.pointA[1]))
        #            f.write(" ")
        #            f.write(str(j.pointA[2]))
        #            f.write(" ")
        #            f.write(str(j.pointC[0]))
        #            f.write(" ")
        #            f.write(str(j.pointC[1]))
        #            f.write(" ")
        #            f.write(str(j.pointC[2]))
        #            f.write('\n')
        if i == 9999: #code to call director field and calculate the nematic order parameter for the given config
            orderparameter = directorfield1()
    return orderparameter



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

# 'transformcarcyl' function takes a vector of x,y,z Cartesian coordinates and returns a vector of cylindrical coords
def transform_carcyl(cart_coords):
    x = cart_coords[0]
    y = cart_coords[1]
    z = cart_coords[2]

    r = math.sqrt(x**2 + y**2)
    theta = math.atan(y/x)
    z = z

    cyl_coords = [r,theta,z]
    return cyl_coords


# 'transformcylcar' function takes a vector of r, theta, z cylindrical coordinates and returns a vector of cartesian coords
def transform_cylcar(cyl_coords):
    r = cyl_coords[0]
    theta = cyl_coords[1]
    z = cyl_coords[2]

    x = r*math.cos(theta)
    y = r*math.sin(theta)
    z = z

    cart_coords = [x,y,z]
    return cart_coords


# 'validate' function tests to see whether a particle remains within the cell for a given trial move
def validate(mover, trial_move, radius, length):
    # These are the minimum and maximum endpoint positions allowed in r and z
    minr = 0 + mover.radius
    maxr = radius - mover.radius
    minz = 0 + mover.radius
    maxz = length - mover.radius
    # Particle position and orientation updated with trial move coordinates (Cartesian)
    mover.whereami(trial_move[0:3], trial_move[3], trial_move[4])
    # Cartesian coordinates need transforming to cylindrical
    # ACTUALLY I NEED TO DO THIS WITH THE ENDPOINTS, NOT THE CENTREPOINT!
    cylcoordsA = transform_carcyl(mover.pointA[0:3])
    cylcoordsC = transform_carcyl(mover.pointC[0:3])
    rA = cylcoordsA[0]
    zA = cylcoordsA[2]
    rC = cylcoordsC[0]
    zC= cylcoordsC[2]
    # if else statements to check if move allowed
    accept = False
    if rA < minr:
        accept = False
        #print('A point out of bounds in r - less than min')
    elif rA > maxr:
        accept = False
        #print('A point out of bounds in r - more than max')
    elif rC < minr:
        accept = False
        #print('C point out of bounds in r - less than min')
    elif rC > maxr:
        accept = False
        #print('C point out of bounds in r - more than max')
    elif zA < minz:
        accept = False
        #print('A point out of bounds in z - less than min')
    elif zA > maxz:
        accept = False
        #print('A point out of bounds in z - more than max')
    elif zC < minz:
        accept = False
        #print('C point out of bounds in z - less than min')
    elif zC > maxz:
        accept = False
        #print('C point out of bounds in z - more than max')
    elif overlap(mover) == True:
        accept = False
        #print('trial move would overlap another particle')
    else:
        accept = True
        #print('accepted with endpoints at:')
        #print(mover.output)
    return accept


# 'directorfield1' finds the average direction of (nematic) orientation using components then calculates the 
# nematic order parameter and returns it to the calling function
def directorfield1():
    #vectors = []
    xcomp = 0
    ycomp = 0
    zcomp = 0
    n = len(RigidRod.instances)
    for i in range(0, n):
        RigidRod.instances[i].vectorise()
        vector = RigidRod.instances[i].vector
        #print('my vector is...', vector)
        xcomp += vector[0]
        ycomp += vector[1]
        zcomp += vector[2]
        #vectors.append(RigidRod.instances[i].vector)
    xcomp = xcomp/n
    ycomp = ycomp/n
    zcomp = zcomp/n
    #print('components of director', xcomp, ycomp, zcomp)
    dirmag = math.sqrt(xcomp**2 + ycomp**2 + zcomp**2)
    director = [xcomp/dirmag, ycomp/dirmag, zcomp/dirmag]
    #print('the director field is...', director)
    distributionsum = 0
    for j in range(0,n):
        #print('rod number', j)
        rodunit = RigidRod.instances[j].polarunit 
        #print('the unit vector for the rod is', rodunit)
        costheta = (director[0]*rodunit[0] + director[1]*rodunit[1] + director[2]*rodunit[2]) 
        angle = math.acos(costheta)
        #print('angle is ', angle)
        distfunc = 3*(costheta**2) - 1
        #print('expression is', distfunc)
        distributionsum += distfunc
    #print('distribution sum is', distributionsum)
    orderparameter = distributionsum/(2*n)
    #print('order parameter is', orderparameter)
    return orderparameter


## END OF FUNCTION DEFINITIONS ##

# SETTING UP INITIAL VALUES
# Setting up some parameters for simulation cell and steps
cellradius = 400 #radius of axon, r coordinate
celllength = 2000 #length of axon, z coordinate
steps = list(range(10000)) #Number of steps in my random walk

## INITIALISING PARTICLES
length = 100
radius = 4
nparticles = 10 #number of rod particles

orderparam = random_walk(nparticles, length, radius, celllength, cellradius, steps)
print(orderparam)


