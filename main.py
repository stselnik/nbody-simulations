import math
import time
import tkinter
import numpy as np
import requests
import re
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

class OrbitalEntity:
    def __init__(self, name, x, y, z, vx, vy, vz, mass, ax, color=""):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass
        self.xpoints = np.array([])
        self.ypoints = np.array([])
        self.zpoints = np.array([])
        self.ln, = ax.plot([], [], [], color,label=name)
        self.a = [0, 0, 0]

    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Velocity: ({self.vx}, {self.vy}, {self.vx}) , Mass: {self.mass}"

root = tkinter.Tk()
root.wm_title("N-Body Solar System Simulator")

fig, ax = plt.subplots()
ax = fig.add_subplot(projection='3d')

orbital_entities = []
# Keep track of execution time to debug
process_times = np.array([]) 
def add_orbital_entity(name, horizon_id, mass, ax, color=""):
    # Fetch all values for 
    # Define the time span:
    start_time = '2025-05-17'
    stop_time = '2025-05-18'

    url = 'https://ssd.jpl.nasa.gov/api/horizons.api'
    url += "?format=text&EPHEM_TYPE=VECTORS&OBJ_DATA=NO&CENTER='500@0'"
    url += "&COMMAND='{}'&VEC_TABLE='2'&START_TIME='{}'&STOP_TIME='{}'&STEP_SIZE='2d'".format(horizon_id, start_time, stop_time)

    x = requests.get(url)
    data = x.text
    data = data.split("TDB")[4].split("$$EOE")[0]
    values = re.split('X|Y|Z|VX|VY|VZ|=|\n| ', data)
    values = list(map((lambda x: float(x)), filter(lambda x: x != '', values)))
    print(values)
    orbital_entities.append(OrbitalEntity(name, values[0], values[1], values[2], values[3], values[4], values[5], mass, ax, color))

add_orbital_entity("Sun", 10, 1.989e30, ax, "#F9CA0B")
add_orbital_entity("Mercury", 199, 3.302e23, ax, "#9FC8E2")
add_orbital_entity("Venus", 299, 48.685e23, ax, "#ECA72F")
add_orbital_entity("Earth", 399, 5.972e24, ax, "#46B1CE")
add_orbital_entity("Mars", 499, 6.4171e23, ax, "#EE614E")
add_orbital_entity("Jupiter", 599, 18.9819e26, ax, "#EDBA76")
add_orbital_entity("Saturn", 699, 5.6834e26, ax, "#F4E27F")
add_orbital_entity("Uranus", 799, 86.813e23, ax, "#B9EEF1")
add_orbital_entity("Neptune", 899, 102.409e24, ax, "#4B80E4")
add_orbital_entity("Pluto", 999, 1.307e22, ax, "#FFC8B7")



canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=True)
toolbar.update()

G = 6.6743e-20 # in km^3 / kg s^2
dt = 86400 # in seconds
time_start = 0
time_final = 15768000 * 2
i = 0


def all_entity_lines():
    lines  = []
    for e in orbital_entities:
        lines.append(e.ln)
    return tuple(lines)

def init():
    ax.set_xlim(-5.9e9, 5.9e9)
    ax.set_ylim(-5.9e9, 5.9e9)
    ax.set_zlim(-5.9e9, 5.9e9)
    return all_entity_lines()

def update(frame):
    t = frame
    return multiple_orbit(t)

def multiple_orbit(t):
    global process_times
    s = time.process_time()
    for iteration in range(0, int(365 / 16)):
        # Drift (Move each orbital entity)
        for i in range(0, len(orbital_entities)):
            entity = orbital_entities[i]
            # Keep track of all positions of an entity
            entity.xpoints = np.append(entity.xpoints, [entity.x])
            entity.ypoints = np.append(entity.ypoints, [entity.y])
            entity.zpoints = np.append(entity.zpoints, [0])
            if (len(entity.xpoints) > 365 / 2):
                entity.xpoints = np.delete(entity.xpoints, 0)
                entity.ypoints = np.delete(entity.ypoints, 0)
                entity.zpoints = np.delete(entity.zpoints, 0)
            entity.x = entity.x + (entity.vx * dt)
            entity.y = entity.y + (entity.vy * dt)
            entity.z = entity.z + (entity.vz * dt)

        # Kick
        # Clear previous acceleration values
        for i in range (0, len(orbital_entities)):
            orbital_entities[i].a = [0, 0, 0]
        for i in range(0, len(orbital_entities)):
            e = orbital_entities[i]
            for j in range(i + 1, len(orbital_entities)):
                e2 =orbital_entities[j]
                rx = e.x - e2.x
                ry = e.y - e2.y
                rz = e.z - e2.z
                r_mag = math.sqrt(rx * rx + ry * ry + rz * rz)
                F = (-1) * G * e.mass * e2.mass / (r_mag ** 2)
                # Update current entities accelerations (ax, ay, az)
                e.a[0] += F / e.mass * (rx / r_mag) * dt
                e.a[1] += F / e.mass * (ry / r_mag) * dt
                e.a[2] += F / e.mass * (rz / r_mag) * dt
                # Update acceleration on current selected companion
                e2.a[0] += F / e2.mass * (-1 * rx / r_mag) * dt
                e2.a[1] += F / e2.mass * (-1 * ry / r_mag) * dt
                e2.a[2] += F / e2.mass * (-1 * rz / r_mag) * dt
            e.vx += e.a[0]
            e.vy += e.a[1]
            e.vz += e.a[2]
            e.ln.set_data_3d(e.xpoints, e.ypoints, e.zpoints)

    e = time.process_time()
    process_times = np.append(process_times, [e-s])
    print("Avg Time: ", np.average(process_times) , " Current time: ",e - s)
    return all_entity_lines()


ani = FuncAnimation(fig, update, frames=np.arange(time_start, time_final * 166, dt), init_func=init, blit=True, interval=0.1, repeat=False)
#ax.plot(np.arange(0, time_final, dt), vxpoints, "b", label="vx")
#ax.plot(np.arange(0, time_final, dt), vypoints, "r", label="vy")
#ax.scatter(xpoints, ypoints)
#ax.set_facecolor((0, 0, 0))
#fig.set_facecolor((0, 0, 0))
#ax.set_axis_off()

#ax.grid()
ax.legend()
#plt.show()


toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()


