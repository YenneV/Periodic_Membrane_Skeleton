# Monte Carlo Type Simulation for a Single, Structureless Spectrin Tetramer in a 2D Cartesian Space

from random import randint
import math
import numpy as np
import matplotlib.pyplot as plt

# Function that does a full walk on 1 particle for a given no. of steps
def rand_walk(steps, initial, xrange, yrange):
    # Array to store coordinates for each timestep
    walk_path = np.zeros([len(steps),2], dtype=int)

    # Taking steps
    for i in steps:
        print('Current iteration = ')
        print(i)
        grid_status = np.zeros([len(xrange),len(yrange)], dtype=int) #grid of zeros to store occupation status
        if i == 0: # Initial position set based on initial values given when calling function
            x = initial[0]
            y = initial[1]
        else: #Calculating next set of x,y coordinates for time step i > 0 using random numbers
            step = randint(0,3)
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
                break
        #grid_status[x,y] = 1 #Setting status of x,y position as occupied
        walk_path[i,] = [x,y] #Recording new coordinates in array
        #print('current location')
        #print(walk_path[i,])
        if walk_path[i,0] not in xrange or walk_path[i,1] not in yrange: #Checking that particle is within cell
            x = walk_path[i-1,0] #if outside cell, set coordinates to previous - i.e. particle doesn't move
            y = walk_path[i-1,1]
            walk_path[i,] = walk_path[i-1,] #recording edited coordinates in array
            print('step rejected - out of range')
            #print(walk_path[i,])

    return walk_path

# Function that does a single step given an initial position
def step(initial, xrange, yrange):
    x = initial[0]
    y = initial[1]

    step = randint(0,3)
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


# Parameters for the allowed set of coordinates, number of timesteps etc
xcoords = list(range(100))
ycoords = list(range(100))
timesteps = list(range(1,101)) # Number of iterations, integers from 1 to 100 inclusive
initial_position = [50,50] #Initial x,y coordinates of spectrin

# Next I want to make a function that creates a random walk of a given number of steps

def walk(initial_position, timesteps):
    location = np.zeros([len(timesteps) + 1,2], dtype = int)
    location[0,:] = initial_position

    for i in timesteps:
        initial = location[i-1,:]
        final = step(initial, xcoords, ycoords)
        location[i,:] = final

    return location

# I now want to make a function that calls, walk, generates a random walk, and calculates the
# end to end distance travelled by the particle during the walk, then returns it 

def distance():
    route = walk(initial_position, timesteps)
    start_x = route[0,0]
    start_y = route[0,1]
    end_x = route[100,0]
    end_y = route[100,1]
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    distance = math.sqrt((delta_x)**2 + (delta_y)**2)
    return distance

# And finally a function that runs distance loads of times and gives me all of the values
# so that I can plot a histogram

def travels():
    iterations = list(range(250000))
    walks = np.zeros(len(iterations), dtype = float)

    for i in iterations:
        walks[i] = distance()

    return walks

stuff = travels()
print(stuff)

thing = plt.hist(stuff, bins = 25)
plt.xlabel('End to End Distance of Random Walk')
plt.ylabel('Frequency')
plt.show(thing)


#final = step(initial_position, xcoords, ycoords)

# Call to random walk function
#walk = rand_walk(timesteps, initial_position, xcoords, ycoords) #function call to random walk, with my input values
#print(walk)

# Plotting the position of the particle for all time steps with matplotlib

#plt.xlabel("X Coordinate")
#plt.xlim(0,100)
#plt.ylim(0,100)
#plt.ylabel("Y Coordinate")
#plt.scatter(walk[:,0],walk[:,1])
#plt.show()