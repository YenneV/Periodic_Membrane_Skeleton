#File to read in from nematic order parameter output files and calculate the mean

import numpy

mc_reps = 100
mc_steps = range(1, mc_reps + 1)
qsum = 0

for i in mc_steps:
    with open('D:\Code\Assembly\PMS_PY\Making_Rings\Results\Nematic_Ordering\L100N10\output.{}.txt'.format(i), 'r') as p:
        value = np.genfromtxt(p, dtype = float)
        qsum += value

qsum = qsum/mc_reps
print('average value of nematic order parameter is...', qsum)