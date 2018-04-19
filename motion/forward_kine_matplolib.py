
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

L1 = 10.0  # length of arm 1
L2 = 10.0  # length of arm 2 
theta1 =np.radians([209,210,210,209,207,204,200,194,186,
177,166,154,143,132,123,114,107,100,94,88,83,84,85,86,87,
88,89,89,90,90,90,96,102,107,113,119,126,132,138,144,150,
156,161,165,169,173,175,177,179,180,180,183,186,189,192,
194,197,200,203,206])

theta2 = np.radians([97,92,86,80,73,65,57,48,37,27,15,4,354,
346,340,335,333,331,330,330,331,334,336,339,342,345,349,
351,355,357,360,1,2,2,4,7,11,15,19,24,30,36,42,48,54,61,66,
72,79,85,90,90,91,91,92,91,92,93,94,9])

#create plotting area
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-20, 20), ylim=(-20, 20))
ax.set_aspect('equal')
ax.grid()
line, = ax.plot([], [], 'o-', lw=2)

def init():
 line.set_data([], [])
 return line, 


def animate(i):
 x1 = L1 * np.cos([theta1[i]])
 x2 = L2 * np.cos([theta2[i]])
 
 y1 = L1 * np.sin([theta1[i]])
 y2 = L2 * np.sin([theta2[i]])
 
 thisx = [0, x1,x1+x2]
 thisy = [0, y1,y1+y2]
 line.set_data(thisx, thisy)
 return line, 

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(theta1)),
                              interval=80, blit=True, init_func=init)

ani.save('animation.gif', writer='imagemagick', fps=12)
plt.show()

