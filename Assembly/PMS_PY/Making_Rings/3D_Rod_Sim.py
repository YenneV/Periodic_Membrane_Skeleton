# Plotting file for 3D rigid rods

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# I'll need to input some variables
steps = list(range(10000)) #Specify the number of steps in the walk so I can read in the right number of files
nparticles = 500 #Specify how many particles are in the simulation so I know how many lines I need

for i in steps:
    if i%1000 == 0:
        with open('D:\Code\Assembly\PMS_PY\Making_Rings\Results\Rigid_Rods_3D\Testing\coords{}.txt'.format(i), 'r') as p:
            data = np.genfromtxt(p, dtype = float, delimiter = " ")
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlim(-50,50)
            ax.set_ylim(-50,50)
            ax.set_zlim(0,100)
            ax.set_xlabel('x coordinate')
            ax.set_ylabel('y coordinate')
            ax.set_zlabel('z coordinate')
            plt.grid()
            plt.title('Step = {}'.format(i))
            for j in range(0, nparticles):
                xpoints = [data[j][0], data[j][3]]
                ypoints = [data[j][1], data[j][4]]
                zpoints = [data[j][2], data[j][5]]
                ax.plot(xpoints, ypoints, zpoints, linewidth=4, marker='o', markersize=4)
            plt.savefig('D:\Images\RigidRod_3D\image{}.pdf'.format(i), dpi=350)
            #plt.show()
            plt.close()

# CREATING TEST PLOT
# NEED TO USE VECTOR RETURNED FROM WALK TO DO A 3D PLOT OF THE POINTS 
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#x = [7.5, 12.5]
#y = [7.5, 2.5]
#z = [5.34, -1.54]
#ax.plot(x,y,z)
#plt.show()