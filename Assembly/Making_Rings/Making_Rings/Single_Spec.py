# Monte Carlo Type Simulation for a Single, Structureless Spectrin Tetramer in a 2D Cartesian Space

#from random import randint
import random
import math
import numpy as np
import matplotlib.pyplot as plt
random.seed(10)

# Function 'step' does a single step given an initial position and a set of allowed coordinates
# The new coordinates are returned to the calling function
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


# Function 'walk' takes a starting position and a given number of timesteps, and creates a random walk 
# of the specified step length by calling the step function.  A vector of coordinates per time step
# is returned to the calling function

def walk(initial_position, timesteps):
    location = np.zeros([len(timesteps) + 1,2], dtype = int)
    location[0,:] = initial_position

    for i in timesteps:
        initial = location[i-1,:]
        final = step(initial, xcoords, ycoords)
        location[i,:] = final

    return location

# Function 'distance' generates a random walk by calling 'walk', then calculates the magnitude of the
# distance walked and returns it to the calling function

def distance():
    route = walk(initial_position, timesteps)
    start_x = route[0,0]
    start_y = route[0,1]
    end_x = route[max(timesteps),0] 
    end_y = route[max(timesteps),1] 
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    distance = math.sqrt((delta_x)**2 + (delta_y)**2)
    print('walk distance')
    print(distance)
    return distance

# Function 'travels' records distances walked by calling 'distance', and returns a vector with the 
# distance travelled in a given number of random walks - for statistical analysis

def travels(iterations):
    walks = np.zeros(len(iterations), dtype = float)
    for i in iterations:
        print('Iteration')
        print(i)
        walks[i] = distance()
        #put a with statement here so it prints the distance to a file

    return walks

# INPUT PARAMETERS
xcoords = list(range(3000)) 
ycoords = list(range(3000))
timesteps = list(range(1,1001)) # Number of steps in each walk, integers from 1 to 1000 inclusive
initial_position = [1500,1500] #Initial x,y coordinates of spectrin for each walk
iterations = list(range(1000000)) # Number of walks that I want to simulate

# SCATTER PLOT - Code to visualise a single random walk as a scatter plot for a given number of steps
#route = walk(initial_position, timesteps)
#plt.scatter(route[:,0], route[:,1])
#plt.xlabel('x Coordinate')
#plt.ylabel('y Coordinate')
#plt.xlim(0,100)
#plt.ylim(0,100)
#plt.show()

# HISTOGRAM - Code to find mean distance travelled and plot a histogram of distances for a given number of walks
multiwalks = travels(iterations)
avg_walk = np.mean(multiwalks)
print(avg_walk)
hist_plot = plt.hist(multiwalks, bins = 25)
plt.xlabel('End to End Distance of Random Walk')
plt.ylabel('Frequency')
plt.show(hist_plot)
