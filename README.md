# AST 203 Final Project: Computational N-Body Simulation of Planetary Orbits in the Solar System


The purpose of this program is to simulate realistic 3-dimensional planetary motion throughout our solar system centered around the Solar System Barycenter using **Python** with **matplotlib**. 

<img width="652" alt="Image" src="https://github.com/user-attachments/assets/449f0b51-3f77-46ff-ba87-e2d87049b017" />

You can find a quick demo of the program here! https://youtu.be/TFFD7GlUI5I

## Functionality
* Viewing changing positions of entities across the solar system in 3D.
* Specifying simulation start date.
* Viewing in-simulation date
## Dynamic Update Functionality:
* Number of timesteps between frames (speed of simulation)
* Trail length (number of points before current position to track position over time)
* Toggle visual effects
  * Show Grid / Axis
  * Show Legend of Entities
  * Dark Mode (*Like space!*)

## Implementation
This program utilizes <a href=https://en.wikipedia.org/wiki/Leapfrog_integration>Leapfrog Integration</a> to perform numerical integration over small timesteps (in this case chosen to be dt = 1 day (86400s)) in order to preserve accuracy in long-term simulation and reducing uneccessary computational expenses. 
At each timestep, the position of each entity would "drift" by:

$x = x + v_x(dt)$

$y = y + v_y(dt)$

$z = z + v_z(dt)$

Then, it would "kick" by incrementing the velocity in each direction by the calculated acceleration.  Acceleration for a given orbital entity at each timestep is derived from the sum of the gravitational force vectors between the entity and all other entities in the system divided by the mass of the entity:

$\vec a = \frac{1}{m_i} \sum_{ij} \vec F_{g} =\frac{1}{m_i} \sum_{ij} \frac{G m_i m_j}{(r_{mag})^2}$ , where $r_{mag} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2 +(z_i - z_j)^2 }$

So the acceleration for each entity would sum by:

$F / m_i * (r_x / r_{mag}) * dt$

Then, each velocity gets a kick by:

$v_x = v_x  + a_x(dt)$

$v_y = v_y + a_y(dt)$

$v_z = v_z  + a_z(dt)$


The initial vectors for the positions and velocities of each planet are fetched dynamically from the <a href=https://ssd.jpl.nasa.gov/horizons/>JPL Ephemeris / Horizons System</a>, a solar system data and ephemeris computation service that provides accurare ephemerides for solar system objects.

The program makes a call to the JPL Horizons API for each target body by requesting a Vector Table centered at the Solar System Barycenter with the target body specified by the body's given Horizons ID (specified in the Horizons documentation), and a time specifications that is chosen by the user in the menu before running a simulation. The user only needs to input a start date as only the initial vectors are required and the response should only contain one set of vectors. The program then parses the response for the relevant values and assigns them to the object keeping track of the respective entity.


## Closing Remarks
I did mention to you that I was interested in potentially simulating a spiral galaxy a little while ago. I ended up completing the idea I had in my original proposal because I realized they would functionally work the same and that it would've been a safer bet to complete the original idea just in case and time permitting, try to extend the solar system n-body simulation to a larger scale. I realized after some experimentation that my current program isn't prepared to handle all too many particles at the moment because this algorithm is a bit of a "brute-force" approach which has O($n^2$) time complexity and would not scale effectively. This also relates to the other potential goal of this project to demonstrate the idea of <a href=https://web.mit.edu/wisdom/www/pluto-chaos.pdf >Pluto's Chaotic Motion</a>. While demonstrating this actually *should* be possible with this program (!), the time required for my computer to run the simulation across several million years (twice) would have not been feasible for the sake of fitting within the time frame for submitting the project.

I actually hope to keep contributing to this project over my free time during the summer! I would love to extend the idea and eventually achieve the goal of observing bar instability in a model of a galaxy in 3 dimensions. I hope to reimplement the logic for the simulation by utilizing another algorithm such as the Barnes-Hut simulation which utilizes octrees to achieve O($n \log n$) time complexity. Additionally, I would love to do additional research in understanding how to find the initial conditions for such a simulation. 

Working on this project was a ton of fun! Please let me know if you have any questions or concerns whatsoever!

Best,
Samuel Tselnik







