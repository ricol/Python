import pygame
import math
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
FPS = 60
AU = 149.6e6 * 1000  # 1 Astronomical Unit in meters
G = 6.67430e-11  # Gravitational constant
SCALE = 100 / AU  # Scale for display (pixels per meter)
TIME_STEP = 3600 * 24  # 1 day per frame (in seconds)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)
LIGHT_GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
DARK_BLUE = (0, 0, 139)
GOLD = (255, 215, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation - Moving Planets")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont('Arial', 16)
large_font = pygame.font.SysFont('Arial', 24)

SUN_MASS = 1.9885e30

class Planet:
    def __init__(self, name, radius, color, mass, distance, orbital_period):
        self.name = name
        self.radius = radius
        self.color = color
        self.mass = mass
        self.distance = distance * AU
        self.orbital_period = orbital_period
        self.angle = 0
        self.x = 0
        self.y = 0
        
        # Calculate orbital speed (simplified circular orbit)
        if self.name != "Sun":
            self.orbital_speed = math.sqrt(G * SUN_MASS / self.distance)
        
    def update(self, dt):
        if self.name == "Sun":
            return
        
        # Update angle based on orbital period
        self.angle += (2 * math.pi / (self.orbital_period * 86400)) * dt * simulation_speed
        
        # Calculate position
        self.x = self.distance * math.cos(self.angle)
        self.y = self.distance * math.sin(self.angle)
    
    def draw(self, surface):
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        # Calculate screen position
        screen_x = center_x + self.x * SCALE
        screen_y = center_y + self.y * SCALE
        
        # Draw the planet
        display_radius = max(2, self.radius * SCALE * 1000)  # Scale up for visibility
        
        if self.name == "Sun":
            # Draw sun with gradient effect
            for r in range(display_radius, 0, -2):
                alpha = int(255 * (r / display_radius))
                color = (255, min(255, 150 + alpha//2), max(0, alpha//3))
                pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), r)
        else:
            pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), int(display_radius))
        
        # Draw planet name
        if show_names:
            text = font.render(self.name, True, WHITE)
            text_rect = text.get_rect(center=(screen_x, screen_y - display_radius - 10))
            surface.blit(text, text_rect)
        
        return pygame.Rect(screen_x - display_radius, screen_y - display_radius, 
                          display_radius * 2, display_radius * 2)

# Create the solar system
sun = Planet("Sun", 696340, YELLOW, SUN_MASS, 0, 0)

planets = [
    Planet("Mercury", 2439.7, DARK_GRAY, 3.3011e23, 0.39, 88),
    Planet("Venus", 6051.8, LIGHT_GRAY, 4.8675e24, 0.72, 225),
    Planet("Earth", 6371, BLUE, 5.97237e24, 1.0, 365.25),
    Planet("Mars", 3389.5, RED, 6.4171e23, 1.52, 687),
    Planet("Jupiter", 69911, ORANGE, 1.8982e27, 5.20, 4333),
    Planet("Saturn", 58232, GOLD, 5.6834e26, 9.58, 10759),
    Planet("Uranus", 25362, CYAN, 8.6810e25, 19.22, 30687),
    Planet("Neptune", 24622, DARK_BLUE, 1.02413e26, 30.05, 60190)
]

# Simulation controls
paused = False
simulation_speed = 2
show_names = True
hover_info = "Hover over a planet for details"

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                paused = not paused
            elif event.key == K_UP:
                simulation_speed = min(100, simulation_speed + 5)
            elif event.key == K_DOWN:
                simulation_speed = max(1, simulation_speed - 5)
            elif event.key == K_n:
                show_names = not show_names
        elif event.type == MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            hover_info = "Hover over a planet for details"
            
            # Check if mouse is over the sun
            sun_rect = sun.draw(screen)
            if sun_rect.collidepoint(mouse_pos):
                hover_info = f"Sun\nRadius: 696,340 km\nMass: 1 Sun"
            else:
                # Check planets
                for planet in planets:
                    planet_rect = planet.draw(screen)
                    if planet_rect.collidepoint(mouse_pos):
                        hover_info = (
                            f"{planet.name}\n"
                            f"Radius: {planet.radius:,.1f} km\n"
                            f"Mass: {planet.mass / 1.9885e30:.6f} Suns\n"
                            f"Distance: {planet.distance / AU:.2f} AU\n"
                            f"Orbit: {planet.orbital_period} days"
                        )
                        break
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Update planets
    if not paused:
        for planet in planets:
            planet.update(TIME_STEP)
    
    # Draw all celestial bodies
    sun.draw(screen)
    for planet in planets:
        planet.draw(screen)
    
    # Draw UI
    # Info box
    info_lines = hover_info.split('\n')
    for i, line in enumerate(info_lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (10, 10 + i * 20))
    
    # Controls info
    controls = [
        "Controls:",
        "Space - Pause/Resume",
        "Up/Down - Change speed",
        "N - Toggle names",
        f"Speed: {simulation_speed}x",
        f"Status: {'Paused' if paused else 'Running'}"
    ]
    
    for i, line in enumerate(controls):
        text = font.render(line, True, WHITE)
        screen.blit(text, (WIDTH - 150, 10 + i * 20))
    
    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()