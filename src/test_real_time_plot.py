import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Create a figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Initialize empty lists for x and y data
xdata, ydata = [], []

# Set up the plot parameters
ax.set_xlim(0, 100)
ax.set_ylim(0, 10)
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Real-time Plot')

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot
def update(frame):
    xdata.append(frame)
    ystring = '8'
    yvalue = float(ystring)
    # ydata.append(float(Twist.getMeasurement('V1')))
    ydata.append(yvalue)
    line.set_data(xdata, ydata)
    return line,

# Create an animation
ani = animation.FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)

# Show the plot
plt.show()