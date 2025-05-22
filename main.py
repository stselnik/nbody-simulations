import math
import datetime
import re
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from matplotlib.animation import FuncAnimation
from tkcalendar import DateEntry
from matplotlib import pyplot as plt
import numpy as np
import requests

class NBodySolarSystem:

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

    # Create list that stores all entities in the given system
    orbital_entities = []

    # Append an entity to a systems's orbital entities list given a name, mass, and respective JPL Epehemeris / Horizon ID number to fetch it's initial conditions through the API
    def add_orbital_entity(self, name, horizon_id, mass, ax, color=""):
        # Define the time span:
        start_time = '2025-05-17'
        stop_time = '2025-05-18'

        url = 'https://ssd.jpl.nasa.gov/api/horizons.api'
        url += "?format=text&EPHEM_TYPE=VECTORS&OBJ_DATA=NO&CENTER='500@0'"
        url += "&COMMAND='{}'&VEC_TABLE='2'&START_TIME='{}'&STOP_TIME='{}'&STEP_SIZE='2d'".format(horizon_id, start_time, stop_time)

        # Fetch the response through the JPL Emphemeris / Horizons system API and parse the vector table
        x = requests.get(url)
        data = x.text
        data = data.split("TDB")[4].split("$$EOE")[0]
        values = re.split('X|Y|Z|VX|VY|VZ|=|\n| ', data)
        values = list(map((lambda x: float(x)), filter(lambda x: x != '', values)))
        print(values)
        self.orbital_entities.append(self.OrbitalEntity(name, values[0], values[1], values[2], values[3], values[4], values[5], mass, ax, color))

    def create_simulation(self, start_date):
        print("Running simulation beggining at: ", start_date)
        self.simulation_time.set(start_date)

        if (len(plt.get_fignums()) != 0):
            plt.close()

         # Initialize Matplotlib Plots
        fig, ax = plt.subplots()
        ax = fig.add_subplot(projection='3d')

        # Populate System with Solar System planets (Centered at Solar System Barycenter)
        self.add_orbital_entity("Sun", 10, 1.989e30, ax, "#F9CA0B")
        self.add_orbital_entity("Mercury", 199, 3.302e23, ax, "#9FC8E2")
        self.add_orbital_entity("Venus", 299, 48.685e23, ax, "#ECA72F")
        self.add_orbital_entity("Earth", 399, 5.972e24, ax, "#46B1CE")
        self.add_orbital_entity("Mars", 499, 6.4171e23, ax, "#EE614E")
        self.add_orbital_entity("Jupiter", 599, 18.9819e26, ax, "#EDBA76")
        self.add_orbital_entity("Saturn", 699, 5.6834e26, ax, "#F4E27F")
        self.add_orbital_entity("Uranus", 799, 86.813e23, ax, "#B9EEF1")
        self.add_orbital_entity("Neptune", 899, 102.409e24, ax, "#4B80E4")
        self.add_orbital_entity("Pluto", 999, 1.307e22, ax, "#FFC8B7")

        G = 6.6743e-20 # in km^3 / kg s^2
        dt = 86400 # in seconds
        time_start = 0
        time_final = 15768000 * 2

        def all_entity_lines():
            lines  = []
            for e in self.orbital_entities:
                lines.append(e.ln)
            return tuple(lines)

        def init():
            ax.set_xlim(-5.9e9, 5.9e9)
            ax.set_ylim(-5.9e9, 5.9e9)
            ax.set_zlim(-5.9e9, 5.9e9)
            return all_entity_lines()
        
        def multiple_orbit(frame):
            t = frame
            days = 0
            for iteration in range(0, self.iterations.get()):
                days += 1
                # Drift (Move each orbital entity)
                for i in range(0, len(self.orbital_entities)):
                    entity = self.orbital_entities[i]
                    # Keep track of all positions of an entity
                    entity.xpoints = np.append(entity.xpoints, [entity.x])
                    entity.ypoints = np.append(entity.ypoints, [entity.y])
                    entity.zpoints = np.append(entity.zpoints, [0])
                    while (len(entity.xpoints) > self.trail.get()):
                        entity.xpoints = np.delete(entity.xpoints, 0)
                        entity.ypoints = np.delete(entity.ypoints, 0)
                        entity.zpoints = np.delete(entity.zpoints, 0)
                    
                    entity.x = entity.x + (entity.vx * dt)
                    entity.y = entity.y + (entity.vy * dt)
                    entity.z = entity.z + (entity.vz * dt)

                # Kick
                # Clear previous acceleration values
                for i in range (0, len(self.orbital_entities)):
                    self.orbital_entities[i].a = [0, 0, 0]
                for i in range(0, len(self.orbital_entities)):
                    e = self.orbital_entities[i]
                    for j in range(i + 1, len(self.orbital_entities)):
                        e2 =self.orbital_entities[j]
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
                    # Increment velocities
                    e.vx += e.a[0]
                    e.vy += e.a[1]
                    e.vz += e.a[2]
                    e.ln.set_data_3d(e.xpoints, e.ypoints, e.zpoints)
            # Update Date in Simulation on Menu
            previous_date = datetime.strptime(self.simulation_time.get(), "%Y-%m-%d")
            new_date = previous_date + timedelta(days=days)
            self.simulation_time.set(new_date.strftime("%Y-%m-%d"))
            return all_entity_lines()
        # Run Animation
        ani = FuncAnimation(fig, multiple_orbit, frames=np.arange(time_start, time_final * 166, dt), init_func=init, blit=False, interval=0.1, repeat=False)
        # Adjust Plot Appearance
        ax.legend()

        plt.show(block=True)


    def __init__(self, root):
        root.title("N-Body Solar System Simulation")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Start Date")
        self.date = StringVar()
        date_entry = DateEntry(mainframe, width=15, textvariable=self.date, date_pattern='yyyy-mm-dd')
        ttk.Label(mainframe, textvariable=self.date)

        ttk.Label(mainframe, text="Number of Interval Iterations per Frame (days):")
        self.iterations = IntVar(value=10)
        iterations_entry = ttk.Entry(mainframe, width=7, textvariable=self.iterations)

        ttk.Label(mainframe, text="Trail Length (days of previous positions):")
        self.trail = IntVar(value=(int(365/2)))
        trail_entry = ttk.Entry(mainframe, width=7, textvariable=self.trail)

        self.simulation_time = StringVar()

        def handle_simulation_button_press():
            run_simulation_button.config(state='disabled')
            self.create_simulation(start_date=self.date.get())

        run_simulation_button = ttk.Button(mainframe, text="Run Simulation", command=handle_simulation_button_press)

        ttk.Label(mainframe, text="Date in Simulation:").grid(column=1)
        ttk.Label(mainframe, textvariable=self.simulation_time).grid(column=1)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        run_simulation_button.focus()
        #root.bind("<Return>", self.calculate)
        

root = Tk()
NBodySolarSystem(root)
root.mainloop()