import math
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


class OrbitalEntity:
    def __init__(self, x, y, z, vx, vy, vz, mass, ax):
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
# Entity representing the Sun
orbital_entities.append(OrbitalEntity(0, 0, 0, 0, 0, 0, 1.989e30, ax))
# Entity representing Earth
orbital_entities.append(OrbitalEntity(-8.529440084914488E+07, -1.262070629279483E+08, 3.267467302957177E+04, 2.421505166691593E+01, -1.677450100101587E+01, 2.508322287999576E-04, 5.972e24, ax))
# Entity representing the Moon
#orbital_entities.append(OrbitalEntity(-8.519842463576744E+07, -1.265887274718351E+08,-2.688295040652156E+02, 2.516902896545330E+01, -1.649318291651622E+01, 3.262714764303443E-02, 7.348e22, ax))
# Entity representing Venus
orbital_entities.append(OrbitalEntity(-3.040772888668124E+05, -1.095389886846205E+08,-1.493038011771150E+06, 3.479834176174783E+01, -2.576663714548788E-03, -2.007354317633674E+00, 48.685e23, ax))

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
    ax.set_xlim(-149597871, 149597871)
    ax.set_ylim(-149597871, 149597871)
    ax.set_zlim(-149597871, 149597871)
    return all_entity_lines()

def update(frame):
    t = frame
    return multiple_orbit(t)

def multiple_orbit(t):
    # Drift (Move each orbital entity)
    for i in range(0, len(orbital_entities)):
        entity = orbital_entities[i]
        # Keep track of all positions of an entity
        entity.xpoints = np.append(entity.xpoints, [entity.x])
        entity.ypoints = np.append(entity.ypoints, [entity.y])
        entity.zpoints = np.append(entity.zpoints, [0])
        entity.x = entity.x + (entity.vx * dt)
        entity.y = entity.y + (entity.vy * dt)
        entity.z = entity.z + (entity.vz * dt)
        if (t == 86400):
            print("Hello world: " , entity.x  , ", " , entity.y , ", " , entity.z)
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


def single_orbit(t):
    entity.xpoints = np.append(entity.xpoints, [entity.x])
    entity.ypoints = np.append(entity.ypoints, [entity.y])
    entity.zpoints = np.append(entity.zpoints, [0])
    print(f'(x: {entity.x}, y: {entity.y}) , (vx: {entity.vx}, vy: {entity.vy})')

    # Drift
    entity.x = entity.x + (entity.vx * dt)
    entity.y = entity.y + (entity.vy * dt)
    entity.z = entity.z + (entity.vz * dt)

    # Kick
    rx = entity.x - orbital_entities[0].x
    ry = entity.y - orbital_entities[0].y
    rz = entity.z - orbital_entities[0].z
    r_mag = math.sqrt(rx * rx + ry * ry + rz * rz)
    a = (-1) * G * orbital_entities[0].mass / (r_mag ** 2)
    entity.vx = entity.vx + a * (rx / r_mag) * dt
    entity.vy = entity.vy + a * (ry / r_mag) * dt
    entity.vz = entity.vz + a * (rz / r_mag) * dt


    ln.set_data_3d(entity.xpoints, entity.ypoints, entity.zpoints)
    ln2.set_data_3d(entity.zpoints, entity.xpoints, entity.ypoints)
    return ln, ln2,



ani = FuncAnimation(fig, update, frames=np.arange(time_start, time_final, dt), init_func=init, blit=True, interval=15, repeat=False)
#ax.plot(np.arange(0, time_final, dt), vxpoints, "b", label="vx")
#ax.plot(np.arange(0, time_final, dt), vypoints, "r", label="vy")
#ax.scatter(xpoints, ypoints)
#ax.set_facecolor((0, 0, 0))
#fig.set_facecolor((0, 0, 0))


ax.grid()
#ax.legend()
plt.show()



