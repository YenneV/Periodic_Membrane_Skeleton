# Monte Carlo Type Simulation for a Single, Structureless Spectrin Tetramer in a 2D Cartesian Space

from random import randint
import numpy as np
import matplotlib.pyplot as plt


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


# Values to set myself, to say where the particle begins, the space in which it can move, and for how many iterations
xcoords = list(range(100))
ycoords = list(range(100))
timesteps = list(range(1000)) # Number of iterations
initial_position = [50,50] #Initial x,y coordinates of spectrin

# Call to random walk function
walk = rand_walk(timesteps, initial_position, xcoords, ycoords) #function call to random walk, with my input values
print(walk)

# Plotting the position of the particle for all time steps with matplotlib

plt.xlabel("X Coordinate")
plt.xlim(0,100)
plt.ylim(0,100)
plt.ylabel("Y Coordinate")
plt.scatter(walk[:,0],walk[:,1])
plt.show()