# For statistical analysis of multiple single particle walks

import numpy as np
import matplotlib.pyplot as plt

#Loading in data from file and saving in numpy array
with open('D:\Code\Assembly\Making_Rings\Making_Rings\Results\Single_Point\Distances.txt', 'r') as d:
    distances = np.genfromtxt(d, dtype = float, delimiter = '\n')

#Taking mean walk distance
avg_walk = np.mean(distances)
print(avg_walk)

#Plotting histogram of walk distances
hist_plot = plt.hist(distances, bins = 35)
plt.xlabel('End to End Distance of Random Walk')
plt.ylabel('Frequency')
plt.show(hist_plot)
