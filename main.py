import math
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


class OrbitalEntity:
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass
    def __str__(self):
        return f"Position: ({self.x}, {self.y}, {self.z}), Velocity: ({self.vx}, {self.vy}, {self.vx}) , Mass: {self.mass}"

orbital_entities = []
# Entity representing the Sun
orbital_entities.append(OrbitalEntity(0, 0, 0, 0, 0, 0, 1.989e30))
# Entity representing the Earth
orbital_entities.append(OrbitalEntity(-149597871, 0, 0, 0, 29.78, 0, 5.972e24))

print(orbital_entities[0])

xpoints = np.array([])
ypoints = np.array([])
zpoints = np.array([])

vxpoints = np.array([])
vypoints = np.array([])
vzpoints = np.array([])  

G = 6.6743e-20 # in km^3 / kg s^2
dt = 86400 # in seconds
time_start = 0
time_final = 15768000 * 2
entity = orbital_entities[1]
i = 0
"""
i = 0
for t in range(0, time_final, dt):
    xpoints = np.append(xpoints, [entity.x])
    ypoints = np.append(ypoints, [entity.y])
    vxpoints = np.append(vxpoints, [entity.vx])
    vypoints = np.append(vypoints, [entity.vy])
    print(f'{i}: (x: {entity.x}, y: {entity.y}) , (vx: {entity.vx}, vy: {entity.vy})')

    # Drift
    entity.x = entity.x + (entity.vx * dt)
    entity.y = entity.y + (entity.vy * dt)

    # Kick
    rx = entity.x - orbital_entities[0].x
    ry = entity.y - orbital_entities[0].y
    r_mag = math.sqrt(rx * rx + ry * ry)
    a = (-1) * G * orbital_entities[0].mass / (r_mag ** 2)
    entity.vx = entity.vx + a * (rx / r_mag) * dt
    entity.vy = entity.vy + a * (ry / r_mag) * dt
    i+=1


print(xpoints)
print(ypoints)
"""
fig, ax = plt.subplots()
#ax = fig.add_subplot(projection='3d')
ln, = ax.plot([], [])

def init():
    ax.set_xlim(-149597871, 149597871)
    ax.set_ylim(-149597871, 149597871)
    return ln,

def update(frame):
    global xpoints
    global ypoints
    global vxpoints
    global vypoints
    t = frame
    xpoints = np.append(xpoints, [entity.x])
    ypoints = np.append(ypoints, [entity.y])
    vxpoints = np.append(vxpoints, [entity.vx])
    vypoints = np.append(vypoints, [entity.vy])
    print(f'(x: {entity.x}, y: {entity.y}) , (vx: {entity.vx}, vy: {entity.vy})')

    # Drift
    entity.x = entity.x + (entity.vx * dt)
    entity.y = entity.y + (entity.vy * dt)

    # Kick
    rx = entity.x - orbital_entities[0].x
    ry = entity.y - orbital_entities[0].y
    r_mag = math.sqrt(rx * rx + ry * ry)
    a = (-1) * G * orbital_entities[0].mass / (r_mag ** 2)
    entity.vx = entity.vx + a * (rx / r_mag) * dt
    entity.vy = entity.vy + a * (ry / r_mag) * dt

    ln.set_data(xpoints, ypoints)
    return ln,

ani = FuncAnimation(fig, update, frames=np.arange(time_start, time_final, dt), init_func=init, blit=True, interval=5, repeat=False)
#ax.plot(np.arange(0, time_final, dt), vxpoints, "b", label="vx")
#ax.plot(np.arange(0, time_final, dt), vypoints, "r", label="vy")
#ax.scatter(xpoints, ypoints)
#ax.set_facecolor((0, 0, 0))
#fig.set_facecolor((0, 0, 0))


ax.grid()
#ax.legend()
plt.show()



