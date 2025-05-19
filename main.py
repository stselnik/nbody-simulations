import math
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import requests
import re

class OrbitalEntity:
    def __init__(self, name, x, y, z, vx, vy, vz, mass, ax):
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
        self.ln, = ax.plot([], [], [])

    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Velocity: ({self.vx}, {self.vy}, {self.vx}) , Mass: {self.mass}"


fig, ax = plt.subplots()
ax = fig.add_subplot(projection='3d')

orbital_entities = []

def add_orbital_entity(name, horizon_id, mass, ax):
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
    orbital_entities.append(OrbitalEntity(name, values[0], values[1], values[2], values[3], values[4], values[5], mass, ax))

add_orbital_entity("Sun", 10, 1.989e30, ax)
add_orbital_entity("Mercury", 199, 3.302e23, ax)
add_orbital_entity("Venus", 299, 48.685e23, ax)
add_orbital_entity("Earth", 399, 5.972e24, ax)
add_orbital_entity("Mars", 499, 6.4171e23, ax)
add_orbital_entity("Jupiter", 599, 18.9819e26, ax)
add_orbital_entity("Saturn", 699, 5.6834e26, ax)
add_orbital_entity("Uranus", 799, 86.813e23, ax)
add_orbital_entity("Neptune", 899, 102.409e24, ax)
add_orbital_entity("Pluto", 999, 1.307e22, ax)



# Entity representing the Sun
#orbital_entities.append(OrbitalEntity("Sun", 0, 0, 0, 0, 0, 0, 1.989e30, ax))
# Entity representing Earth
#orbital_entities.append(OrbitalEntity(-8.529440084914488E+07, -1.262070629279483E+08, 3.267467302957177E+04, 2.421505166691593E+01, -1.677450100101587E+01, 2.508322287999576E-04, 5.972e24, ax))
# Entity representing the Moon
#orbital_entities.append(OrbitalEntity(-8.519842463576744E+07, -1.265887274718351E+08,-2.688295040652156E+02, 2.516902896545330E+01, -1.649318291651622E+01, 3.262714764303443E-02, 7.348e22, ax))
# Entity representing Venus
#orbital_entities.append(OrbitalEntity(-3.040772888668124E+05, -1.095389886846205E+08,-1.493038011771150E+06, 3.479834176174783E+01, -2.576663714548788E-03, -2.007354317633674E+00, 48.685e23, ax))

print(orbital_entities[1])

G = 6.6743e-20 # in km^3 / kg s^2
dt = 86400 # in seconds
time_start = 0
time_final = 15768000 * 2
entity = orbital_entities[1]
i = 0

ln, = ax.plot([], [], [])
ln2, = ax.plot([], [], [])

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
        for i in range(0, len(orbital_entities)):
            e = orbital_entities[i]
            ax, ay, az = 0, 0, 0
            for j in range(0, len(orbital_entities)):
                e2 = orbital_entities[j]
                if (i != j):
                    rx = e.x - e2.x
                    ry = e.y - e2.y
                    rz = e.z - e2.z
                    r_mag = math.sqrt(rx * rx + ry * ry + rz * rz)
                    a = (-1) * G * e2.mass / (r_mag ** 2)
                    ax += a * (rx / r_mag) * dt
                    ay += a * (ry / r_mag) * dt
                    az += a * (rz / r_mag) * dt
            e.vx += ax
            e.vy += ay
            e.vz += az
            
            e.ln.set_data_3d(e.xpoints, e.ypoints, e.zpoints)
        #print(orbital_entities[0].xpoints, " " , orbital_entities[0].ypoints)
    return all_entity_lines()


ani = FuncAnimation(fig, update, frames=np.arange(time_start, time_final * 166, dt), init_func=init, blit=False, interval=0.1, repeat=False)
#ax.plot(np.arange(0, time_final, dt), vxpoints, "b", label="vx")
#ax.plot(np.arange(0, time_final, dt), vypoints, "r", label="vy")
#ax.scatter(xpoints, ypoints)
#ax.set_facecolor((0, 0, 0))
#fig.set_facecolor((0, 0, 0))


#ax.grid()
ax.legend()
plt.show()



