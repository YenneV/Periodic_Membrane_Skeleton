# Plotting file for rigid rods

import matplotlib.pyplot as plt
import numpy as np

# I'll need to input some variables
xmax = 100 #Specify the max xcoord of the cell you used
ymax = 100 #Specify the max ycoord of the cell you used
steps = list(range(10)) #Specify the number of steps in the walk so I can read in the right number of files

for i in steps:
    if i%100 == 0:
        with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Rigid_Rods\coords{}.txt'.format(i), 'r') as p:
            data = np.genfromtxt(p, dtype = float, delimiter = " ")
            #Create an array for each particle with x,y coords of point A on one row, then of point C on row below
            rod1 = np.array([[data[0][0],data[0][1]], [data[0][2], data[0][3]]])
            rod2 = np.array([[data[1][0],data[1][1]], [data[1][2], data[1][3]]])
            rod3 = np.array([[data[2][0],data[2][1]], [data[2][2], data[2][3]]])
            plt.axis('square')
            plt.xlim((0,100))
            plt.ylim((0,100))
            plt.plot(rod1[:,0], rod1[:,1], linewidth=4, marker='o', markersize=4)
            plt.plot(rod2[:,0], rod2[:,1], linewidth=4, marker='o', markersize=4)
            plt.plot(rod3[:,0], rod3[:,1], linewidth=4, marker='o', markersize=4)
            plt.xlabel('x Coordinate')
            plt.ylabel('y Coordinate')
            plt.grid()
            plt.title('Step = {}'.format(i))
            plt.show()




            #print(data)
            #xcoords = data[:,0]
            #ycoords = data[:,1]
            #plt.axis('square')
            #plt.xlim((0,100))
            #plt.ylim((0,100))
            #circle1 = plt.Circle((xcoords[0],ycoords[0]), radius = 10, fc = 'r')
            #circle2 = plt.Circle((xcoords[1],ycoords[1]), radius = 10, fc = 'g')
            #circle3 = plt.Circle((xcoords[2],ycoords[2]), radius = 10, fc = 'b')
            #plt.gca().add_patch(circle1)
            #plt.gca().add_patch(circle2)
            #plt.gca().add_patch(circle3)
            ##plt.scatter(xcoords,ycoords, color = ['red', 'green', 'blue'])
            #plt.xlabel('x Coordinate')
            #plt.ylabel('y Coordinate')
            #plt.grid()
            #plt.title('Step = {}'.format(i))
            #plt.savefig('D:\Images\Multi_3_No_Overlap\image{}.pdf'.format(i), dpi=350)
            #plt.close()
            #plt.show()

