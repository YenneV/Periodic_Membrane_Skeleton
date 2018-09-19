# Testing 3D and 3D plotting with cylindrical coordinates and a single point particle

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
random.seed(10)

# CONVERT FUNCTION SWITCHES FROM CYLINDRICAL COORDINATES TO CARTESIAN COORDINATES
def convert(r,theta,z):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = z
    newcoords = [x,y,z]
    return newcoords


# STEP FUNCTION REWRITTEN TO STEP IN R,THETA AND Z DIRECTIONS
def step(initial, radius, height):
    r = initial[0]
    theta = initial[1]
    z = initial[2]

    step = random.randint(0,5)
    if step == 0:
        r += 1
    elif step == 1:
        r -= 1
    elif step == 2:
        theta += 1
    elif step == 3:
        theta -= 1
    elif step == 4:
        z += 1
    elif step == 5:
        z -= 1
    else: #Not really necessary but just to make sure rand is drawn in range
        print('Step error - out of range')

    if abs(r) > radius or abs(z) > height:
        r = initial[0]
        theta = initial[1]
        z = initial[2]
        print('step rejected - out of range')
        final = [r,theta,z]
        return final
    else:
        final = [r,theta,z]
        return final


# WALK FUNCTION REWRITTEN TO TAKE STEPS AND TRACK LOCATION IN R,THETA,Z

def walk(initial_position, timesteps):
    location = np.zeros([len(timesteps) + 1,3], dtype = float)
    location_cart = np.zeros([len(timesteps) + 1,3], dtype = float)
    location[0,:] = initial_position
    location_cart[0,:] = convert(location[0,0], location[0,1], location[0,2])

    for i in timesteps:
        initial = location[i-1,:]
        final = step(initial, radius, height)
        location[i,:] = final
        #print('location in cylindrical', location[i,:])
        location_cart[i,:] = convert(location[i,0], location[i,1], location[i,2])
        #print('location in cartesian', location_cart[i,:])

    return location_cart

# CALL THE FUNCTION AND PUT INITIAL VALUES IN HERE
radius = 5 #maximum value of r
height = 25 #maximum value of z
timesteps = list(range(1,1000001))
initial_position = [0,0,0]

test2 = walk(initial_position,timesteps)
print(test2)


# NEED TO USE VECTOR RETURNED FROM WALK TO DO A 3D PLOT OF THE POINTS 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.axis('square')
x = test2[:,0]
y = test2[:,1]
z = test2[:,2]
ax.scatter(x,y,z)
plt.show()
#Axes3D.scatter(xs=1,ys=2,zs=1)

#SCATTER PLOT - Code to visualise a single random walk as a scatter plot for a given number of steps
#route = walk(initial_position, timesteps)
#plt.scatter(route[:,0], route[:,1])
#plt.title('100,000 Step Single Point Particle Random Walk')
#plt.xlabel('x Coordinate')
#plt.ylabel('y Coordinate')
#plt.xlim(0,200)
#plt.ylim(0,200)
#plt.show()
