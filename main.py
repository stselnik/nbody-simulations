import math
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
total_time = 15768000 * 2
ax, ay = 0, 0
entity = orbital_entities[1]
i = 0
for t in range(0, total_time, dt):
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
fig, ax = plt.subplots()

#ax.plot(np.arange(0, total_time, dt), vxpoints, "b", label="vx")
#ax.plot(np.arange(0, total_time, dt), vypoints, "r", label="vy")
ax.scatter(xpoints, ypoints)

ax.legend()
plt.show()


