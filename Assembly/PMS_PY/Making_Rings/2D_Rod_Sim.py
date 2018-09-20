# Plotting file for rigid rods

import matplotlib.pyplot as plt
import numpy as np

# I'll need to input some variables
xmax = 100 #Specify the max xcoord of the cell you used
ymax = 100 #Specify the max ycoord of the cell you used
steps = list(range(10000000)) #Specify the number of steps in the walk so I can read in the right number of files
nparticles = 90 #Specify how many particles are in the simulation so I know how many lines I need

for i in steps:
    if i%10000 == 0:
        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Rigid_Rods\coords{}.txt'.format(i), 'r') as p:
            data = np.genfromtxt(p, dtype = float, delimiter = " ")
            plt.axis('square')
            plt.xlim((0,xmax))
            plt.ylim((0,ymax))
            plt.xlabel('x coordinate')
            plt.ylabel('y coordinate')
            plt.grid()
            plt.title('Step = {}'.format(i))
            for j in range(0, nparticles):
                particle_data = np.array([[data[j][0], data[j][1]], [data[j][2], data[j][3]]])
                plt.plot(particle_data[:,0], particle_data[:,1], linewidth = 4, marker='o', markersize=4)
            plt.savefig('D:\Images\RigidRod_XV\image{}.pdf'.format(i), dpi=350)
            plt.close()


#for i in steps:
#    if i%250 == 0:
#        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Rigid_Rods\coords{}.txt'.format(i), 'r') as p:
#            data = np.genfromtxt(p, dtype = float, delimiter = " ")
#            #Create an array for each particle with x,y coords of point A on one row, then of point C on row below
#            rod1 = np.array([[data[0][0],data[0][1]], [data[0][2], data[0][3]]])
#            rod2 = np.array([[data[1][0],data[1][1]], [data[1][2], data[1][3]]])
#            rod3 = np.array([[data[2][0],data[2][1]], [data[2][2], data[2][3]]])
#            plt.axis('square')
#            plt.xlim((0,100))
#            plt.ylim((0,100))
#            plt.plot(rod1[:,0], rod1[:,1], linewidth=4, marker='o', markersize=4)
#            plt.plot(rod2[:,0], rod2[:,1], linewidth=4, marker='o', markersize=4)
#            plt.plot(rod3[:,0], rod3[:,1], linewidth=4, marker='o', markersize=4)
#            plt.xlabel('x Coordinate')
#            plt.ylabel('y Coordinate')
#            plt.grid()
#            plt.title('Step = {}'.format(i))
#            plt.savefig('D:\Images\RigidRod_XV\image{}.pdf'.format(i), dpi=350)
#            plt.close()