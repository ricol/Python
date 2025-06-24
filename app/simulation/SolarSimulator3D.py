#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from collections import namedtuple

# Constants
AU = 1.496e11  # Astronomical unit (meters)
G = 6.67430e-11  # Gravitational constant
DAY = 86400  # Seconds in a day
YEAR = 365.25 * DAY  # Seconds in a year

# Planet data (name, mass, semi-major axis, eccentricity, inclination (deg), orbital period, color)
Planet = namedtuple('Planet', ['name', 'mass', 'distance', 'eccentricity', 'inclination', 'period', 'color'])
planets = [
    Planet("Mercury", 3.3011e23, 0.3871*AU, 0.206, 7.0, 0.2408*YEAR, 'gray'),
    Planet("Venus", 4.8675e24, 0.7233*AU, 0.007, 3.4, 0.6152*YEAR, 'orange'),
    Planet("Earth", 5.972e24, AU, 0.017, 0.0, YEAR, 'blue'),
    Planet("Mars", 6.417e23, 1.5237*AU, 0.093, 1.9, 1.8809*YEAR, 'red'),
    Planet("Jupiter", 1.899e27, 5.2028*AU, 0.048, 1.3, 11.862*YEAR, 'brown'),
    Planet("Saturn", 5.685e26, 9.5388*AU, 0.056, 2.5, 29.456*YEAR, 'gold'),
    Planet("Uranus", 8.682e25, 19.1914*AU, 0.046, 0.8, 84.07*YEAR, 'lightblue'),
    Planet("Neptune", 1.024e26, 30.0611*AU, 0.010, 1.8, 164.81*YEAR, 'darkblue')
]

sun_mass = 1.989e30  # kg

class SolarSystem3D:
    def __init__(self):
        self.time = 0
        self.dt = DAY * 5  # Time step (5 days)
        self.planet_positions = []
        self.planet_velocities = []
        
        # Initialize planet positions and velocities with inclinations
        for planet in planets:
            # Position at perihelion (closest point to sun)
            r = planet.distance * (1 - planet.eccentricity)
            inc = np.radians(planet.inclination)
            
            # Initial position (inclined orbit)
            pos = np.array([
                r * np.cos(inc),
                0.0,
                r * np.sin(inc)
            ])
            self.planet_positions.append(pos)
            
            # Calculate orbital velocity at perihelion
            v = np.sqrt(G * sun_mass * (2/r - 1/planet.distance))
            vel = np.array([
                0.0,
                v * np.cos(inc),
                v * np.sin(inc)
            ])
            self.planet_velocities.append(vel)
    
    def update(self):
        self.time += self.dt
        
        for i in range(len(planets)):
            # Calculate gravitational force from Sun
            r_vec = self.planet_positions[i]
            r = np.linalg.norm(r_vec)
            force_mag = G * sun_mass * planets[i].mass / (r**2)
            force_dir = -r_vec / r
            force = force_mag * force_dir
            
            # Update velocity
            self.planet_velocities[i] += (force / planets[i].mass) * self.dt
            
            # Update position
            self.planet_positions[i] += self.planet_velocities[i] * self.dt
    
    def get_positions(self):
        return [pos/AU for pos in self.planet_positions]  # Convert to AU

def animate(i, solar_system, scatters, time_text, trails):
    solar_system.update()
    positions = solar_system.get_positions()
    
    # Update planet positions
    for j, scatter in enumerate(scatters):
        scatter._offsets3d = ([positions[j][0]], [positions[j][1]], [positions[j][2]])
        
        # Update trails (store last 100 positions)
        trails[j].append(positions[j])
        if len(trails[j]) > 100:
            trails[j].pop(0)
        
        # Plot trails
        if len(trails[j]) > 1:
            x, y, z = zip(*trails[j])
            scatters[j]._offsets3d = (x, y, z)
    
    # Update time display
    years = solar_system.time / YEAR
    time_text.set_text(f'Time: {years:.2f} Earth years')
    
    return scatters + [time_text]

def run_simulation():
    solar_system = SolarSystem3D()
    
    # Set up 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set viewing angle and limits
    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)
    ax.set_zlim(-15, 15)
    ax.set_box_aspect([1, 1, 0.5])  # Flatten z-axis slightly
    
    # Set labels and title
    ax.set_title('3D Solar System Simulation (Uniform Planet Sizes)', pad=20)
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    
    # Create Sun
    ax.scatter([0], [0], [0], color='yellow', s=200, label='Sun')
    
    # Initialize planets and trails
    scatters = []
    trails = [[] for _ in planets]
    
    for i, planet in enumerate(planets):
        # Initial position
        pos = solar_system.get_positions()[i]
        
        # Create planet (all same size)
        scatter = ax.scatter(
            [pos[0]], [pos[1]], [pos[2]],
            s=50,  # Uniform size for all planets
            color=planet.color,
            label=planet.name
        )
        scatters.append(scatter)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    
    # Add time display
    time_text = ax.text2D(0.02, 0.95, '', transform=ax.transAxes)
    
    # Create animation
    ani = FuncAnimation(
        fig, animate, frames=1000,
        fargs=(solar_system, scatters, time_text, trails),
        interval=50, blit=False
    )
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_simulation()