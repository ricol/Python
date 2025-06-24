#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from collections import namedtuple

# Astronomical constants (SI units)
AU = 1.496e11  # Astronomical unit (meters)
G = 6.67430e-11  # Gravitational constant
DAY = 86400  # Seconds in a day
YEAR = 365.25 * DAY  # Seconds in a year

# Planet data (mass, semi-major axis, eccentricity, orbital period, color)
Planet = namedtuple('Planet', ['name', 'mass', 'distance', 'eccentricity', 'period', 'color'])
planets = [
    Planet("Mercury", 3.3011e23, 0.3871*AU, 0.206, 0.2408*YEAR, 'gray'),
    Planet("Venus", 4.8675e24, 0.7233*AU, 0.007, 0.6152*YEAR, 'orange'),
    Planet("Earth", 5.972e24, AU, 0.017, YEAR, 'blue'),
    Planet("Mars", 6.417e23, 1.5237*AU, 0.093, 1.8809*YEAR, 'red'),
    Planet("Jupiter", 1.899e27, 5.2028*AU, 0.048, 11.862*YEAR, 'brown'),
    Planet("Saturn", 5.685e26, 9.5388*AU, 0.056, 29.456*YEAR, 'gold'),
    Planet("Uranus", 8.682e25, 19.1914*AU, 0.046, 84.07*YEAR, 'lightblue'),
    Planet("Neptune", 1.024e26, 30.0611*AU, 0.010, 164.81*YEAR, 'darkblue')
]

sun_mass = 1.989e30  # kg

class SolarSystem:
    def __init__(self):
        self.time = 0
        self.dt = DAY * 5  # Time step (5 days)
        self.planet_positions = []
        self.planet_velocities = []
        
        # Initialize planet positions and velocities (starting at perihelion)
        for planet in planets:
            # Position at perihelion (closest point to sun)
            r = planet.distance * (1 - planet.eccentricity)
            pos = np.array([r, 0.0])
            self.planet_positions.append(pos)
            
            # Calculate orbital velocity at perihelion
            v = np.sqrt(G * sun_mass * (2/r - 1/planet.distance))
            vel = np.array([0.0, v])
            self.planet_velocities.append(vel)
    
    def update(self):
        self.time += self.dt
        
        # Update each planet's position and velocity
        for i in range(len(planets)):
            # Calculate gravitational force from Sun
            r_vec = self.planet_positions[i]
            r = np.linalg.norm(r_vec)
            force_mag = G * sun_mass * planets[i].mass / (r**2)
            force_dir = -r_vec / r
            force = force_mag * force_dir
            
            # Update velocity (F = ma, so a = F/m)
            self.planet_velocities[i] += (force / planets[i].mass) * self.dt
            
            # Update position
            self.planet_positions[i] += self.planet_velocities[i] * self.dt
    
    def get_positions(self):
        return [pos/AU for pos in self.planet_positions]  # Convert to AU

def animate(i, solar_system, scat, time_text):
    solar_system.update()
    positions = solar_system.get_positions()
    
    # Update scatter plot
    scat.set_offsets(positions)
    
    # Update time display
    years = solar_system.time / YEAR
    time_text.set_text(f'Time: {years:.2f} Earth years')
    
    return scat, time_text

def run_simulation():
    solar_system = SolarSystem()
    
    # Set up plot
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title('Solar System Simulation')
    ax.set_xlabel('Distance from Sun (AU)')
    ax.set_ylabel('Distance from Sun (AU)')
    
    # Draw Sun
    sun = Circle((0, 0), 0.5, color='yellow')
    ax.add_patch(sun)
    
    # Initialize planets
    positions = solar_system.get_positions()
    colors = [planet.color for planet in planets]
    sizes = [np.log(planet.mass/1e23) for planet in planets]  # Scale size by mass
    
    scat = ax.scatter(
        [pos[0] for pos in positions],
        [pos[1] for pos in positions],
        s=sizes,
        c=colors
    )
    
    # Add time display
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    
    # Add legend
    for planet in planets:
        ax.plot([], [], 'o', color=planet.color, label=planet.name)
    ax.legend(loc='upper right')
    
    # Create animation
    ani = FuncAnimation(
        fig, animate, frames=1000,
        fargs=(solar_system, scat, time_text),
        interval=50, blit=True
    )
    
    plt.show()

if __name__ == '__main__':
    run_simulation()