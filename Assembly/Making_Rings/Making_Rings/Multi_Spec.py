#Monte Carlo Type Simulation for Spectrin Tetramers in a 2D Cartesian Space

from random import randint

# stepper takes x,y coordinates as input
# increments randomly in positive/negative x or y
# then returns the updated coordinates

def stepper(coords):
    x = coords[0] # Taking initial coordinates and assigning to x and y
    y = coords[1]
    step = randint(0,3) # Choosing a random number
    if step == 0: #moving left, right, up or down depending on number drawn
        x += 1
    elif step == 1:
        x -= 1
    elif step == 2:
        y += 1
    elif step == 3:
        y -= 1

    return list([x,y]) # returning updated coordinates after step

#Input coordinates
coords = [1,2]

#Call to stepper function
step = stepper(coords)
print(step)
