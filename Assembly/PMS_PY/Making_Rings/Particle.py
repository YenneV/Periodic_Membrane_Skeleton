# Class for rod-like particles
class Particle:
    instances = []
    def __init__(self, position, length, radius, orientation):
        self.initialposition = position
        self.position = position #position of A end?
        self.length = length #rounded ends so this is total length-2R
        self.radius = radius
        # Setting angle of orientation (in radians) and keeping this between limits
        self.orientation = orientation #I must give this in radians
        if self.orientation >= 2*math.pi: #This keeps the angle between 0 and less than 2pi
            self.orientation = self.orientation - 2*math.pi
        # Finding the end points depending on the angle
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
        # Now we've calculated the delta x and delta y component for each end point, we can find coordinates
        self.pointA = [(self.position[0] + self.Ax), (self.position[1] + self.Ay)]
        self.pointC = [(self.position[0] + self.Cx), (self.position[1]+ self.Cy)]
        self.output = self.pointA, self.pointC
        # All instances of this class are appended to a list
        Particle.instances.append(self) #Beware! If I need to delete particles later they won't be removed from this list!
    def whereami(self, newcoords):
        self.position = newcoords
        self.pointA = [(self.position[0] + self.Ax), (self.position[1] + self.Ay)]
        self.pointC = [(self.position[0] + self.Cx), (self.position[1]+ self.Cy)]
        self.output = self.pointA, self.pointC
    def proximity(self, other): #this is between centres of mass - i may not need this if i use a grid
        deltax = abs(other.position[0] - self.position[0])
        deltay = abs(other.position[1] - self.position[1])
        distance = math.sqrt(deltax**2 + deltay**2)
        return distance


