# Code to read in data files and do plotting

import matplotlib.pyplot as plt
import numpy as np

# I'll need to input some variables
xmax = 100 #Specify the max xcoord of the cell you used
ymax = 100 #Specify the max ycoord of the cell you used
steps = list(range(10000)) #Specify the number of steps in the walk so I can read in the right number of files

for i in steps:
    if i%100 == 0:
        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Multi_Sphere\coords{}.txt'.format(i), 'r') as p:
            data = np.genfromtxt(p, dtype = int, delimiter = " ")
            xcoords = data[:,0]
            ycoords = data[:,1]
            plt.axis('square')
            plt.xlim((0,100))
            plt.ylim((0,100))
            circle1 = plt.Circle((xcoords[0],ycoords[0]), radius = 10, fc = 'r')
            circle2 = plt.Circle((xcoords[1],ycoords[1]), radius = 10, fc = 'g')
            circle3 = plt.Circle((xcoords[2],ycoords[2]), radius = 10, fc = 'b')
            plt.gca().add_patch(circle1)
            plt.gca().add_patch(circle2)
            plt.gca().add_patch(circle3)
            #plt.scatter(xcoords,ycoords, color = ['red', 'green', 'blue'])
            plt.xlabel('x Coordinate')
            plt.ylabel('y Coordinate')
            plt.grid()
            plt.title('Step = {}'.format(i))
            plt.savefig('D:\Images\Multi_3_No_Overlap\image{}.pdf'.format(i), dpi=350)
            plt.close()
            #plt.show()

