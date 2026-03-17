#!/usr/bin/env python3
"""
Rocket to the Moon Simulator
A realistic rocket launch simulation game with physics-based mechanics
"""

import pygame
import math
import random
import sys
from enum import Enum, auto
from typing import Tuple, Optional, List
import dataclasses

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors as RGB tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
ORANGE = (255, 150, 50)
LIGHT_BLUE = (100, 150, 255)

# Physics constants (scaled for gameplay)
G = 0.5  # Gravitational constant (scaled for gameplay)
EARTH_MASS = 5000  # Scaled for gameplay
MOON_MASS = 500   # Scaled for gameplay
EARTH_RADIUS = 150
MOON_RADIUS = 40
MOON_DISTANCE = 600
SAFE_LANDING_SPEED = 3.0
ORBIT_ALTITUDE = 200

class GameState(Enum):
    """Enum for different game states"""
    PRE_LAUNCH = auto()
    COUNTDOWN = auto()
    LAUNCH = auto()
    FLYING = auto()
    ORBIT = auto()
    TRANS_LUNAR = auto()
    LUNAR_ORBIT = auto()
    LUNAR_LANDING = auto()
    ON_MOON = auto()
    RETURN = auto()
    EARTH_REENTRY = auto()
    LANDED = auto()
    GAME_OVER = auto()

@dataclasses.dataclass
class TelemetryData:
    """Data class for rocket telemetry"""
    fuel: float
    velocity: float
    velocity_x: float
    velocity_y: float
    stage: int
    heat_shield: float
    altitude_earth: float
    altitude_moon: float
    distance_to_moon: float
    distance_to_earth: float
    angle: float

class Rocket:
    """Rocket class with physics and mechanics"""
    
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        """Reset rocket to initial state"""
        # Start on Earth's surface
        self.x: float = SCREEN_WIDTH // 2
        self.y: float = SCREEN_HEIGHT // 2 + EARTH_RADIUS - 20
        self.vx: float = 0
        self.vy: float = 0
        self.angle: float = 90  # Pointing up (0 = right, 90 = up)
        self.thrust: float = 0
        self.fuel: float = 2000
        self.max_fuel: float = 2000
        self.mass: float = 1000  # kg
        self.stage: int = 1
        self.stage1_fuel: float = 1200
        self.stage2_fuel: float = 800
        self.heat_shield: float = 100
        self.landing_gear: bool = False
        self.engine_temp: float = 20
        self.on_ground: bool = True
        
    def apply_thrust(self, power: float) -> None:
        """Apply thrust to the rocket"""
        if self.fuel > 0 and self.engine_temp < 1000:
            thrust_force = power * 30000  # Thrust force
            self.thrust = thrust_force
            
            # Calculate thrust components
            thrust_x = thrust_force * math.cos(math.radians(self.angle))
            thrust_y = -thrust_force * math.sin(math.radians(self.angle))
            
            # Apply acceleration (F = ma)
            self.vx += thrust_x / self.mass
            self.vy += thrust_y / self.mass
            
            # Consume fuel
            fuel_consumption = power * 1.5
            self.fuel -= fuel_consumption
            if self.stage == 1:
                self.stage1_fuel -= fuel_consumption
            else:
                self.stage2_fuel -= fuel_consumption
            
            # Increase engine temperature
            self.engine_temp += power * 2
            
            # Stage separation
            if self.stage == 1 and self.stage1_fuel <= 0:
                self.stage = 2
                self.mass *= 0.7
        else:
            self.thrust = 0
            # Cool down engine
            self.engine_temp = max(20, self.engine_temp - 0.5)
    
    def rotate(self, direction: int) -> None:
        """Rotate the rocket"""
        self.angle += direction * 2
        self.angle %= 360
    
    def calculate_gravity_force(self, body_x: float, body_y: float, 
                               body_mass: float, body_radius: float) -> Tuple[float, float]:
        """Calculate gravitational force from a celestial body"""
        dx = body_x - self.x
        dy = body_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Minimum distance to prevent infinite force
        min_distance = max(distance, body_radius + 10)
        
        if min_distance > 0:
            force = G * body_mass * self.mass / (min_distance**2)
            force_x = force * dx / min_distance
            force_y = force * dy / min_distance
            return force_x / self.mass, force_y / self.mass
        return 0, 0
    
    def update(self, earth: 'CelestialBody', moon: 'CelestialBody') -> None:
        """Update rocket position and velocity"""
        # Apply gravity from Earth and Moon
        ax_earth, ay_earth = self.calculate_gravity_force(earth.x, earth.y, earth.mass, earth.radius)
        ax_moon, ay_moon = self.calculate_gravity_force(moon.x, moon.y, moon.mass, moon.radius)
        
        # Apply gravitational accelerations
        self.vx += ax_earth + ax_moon
        self.vy += ay_earth + ay_moon
        
        # Update position
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        
        # Check if we're inside Earth or Moon (collision)
        dist_to_earth = math.sqrt((new_x - earth.x)**2 + (new_y - earth.y)**2)
        dist_to_moon = math.sqrt((new_x - moon.x)**2 + (new_y - moon.y)**2)
        
        # Only update position if not colliding
        if dist_to_earth > earth.radius + 5 or dist_to_moon > moon.radius + 5:
            self.x = new_x
            self.y = new_y
            self.on_ground = False
        else:
            # We're colliding - reduce velocity
            self.vx *= 0.9
            self.vy *= 0.9
    
    def get_telemetry(self, earth: 'CelestialBody', moon: 'CelestialBody') -> TelemetryData:
        """Get current telemetry data"""
        dist_to_earth = math.sqrt((self.x - earth.x)**2 + (self.y - earth.y)**2)
        dist_to_moon = math.sqrt((self.x - moon.x)**2 + (self.y - moon.y)**2)
        
        return TelemetryData(
            fuel=self.fuel,
            velocity=math.sqrt(self.vx**2 + self.vy**2),
            velocity_x=self.vx,
            velocity_y=self.vy,
            stage=self.stage,
            heat_shield=self.heat_shield,
            altitude_earth=dist_to_earth - earth.radius,
            altitude_moon=dist_to_moon - moon.radius,
            distance_to_moon=dist_to_moon,
            distance_to_earth=dist_to_earth,
            angle=self.angle
        )
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the rocket on screen"""
        # Calculate rocket shape
        length = 30
        width = 10
        
        # Calculate points for a simple rocket shape
        tip_x = self.x + length * math.cos(math.radians(self.angle))
        tip_y = self.y - length * math.sin(math.radians(self.angle))
        
        back_x = self.x - length * 0.5 * math.cos(math.radians(self.angle))
        back_y = self.y + length * 0.5 * math.sin(math.radians(self.angle))
        
        # Calculate fins
        fin_angle1 = self.angle + 30
        fin_angle2 = self.angle - 30
        
        fin1_x = back_x - 10 * math.cos(math.radians(fin_angle1))
        fin1_y = back_y + 10 * math.sin(math.radians(fin_angle1))
        
        fin2_x = back_x - 10 * math.cos(math.radians(fin_angle2))
        fin2_y = back_y + 10 * math.sin(math.radians(fin_angle2))
        
        # Draw rocket body
        pygame.draw.line(screen, WHITE, (self.x, self.y), (tip_x, tip_y), 3)
        pygame.draw.line(screen, WHITE, (self.x, self.y), (back_x, back_y), 3)
        
        # Draw fins
        pygame.draw.line(screen, GRAY, (back_x, back_y), (fin1_x, fin1_y), 2)
        pygame.draw.line(screen, GRAY, (back_x, back_y), (fin2_x, fin2_y), 2)
        
        # Draw landing gear if deployed
        if self.landing_gear:
            gear_offset = 15
            left_gear_x = self.x + gear_offset * math.cos(math.radians(self.angle + 90))
            left_gear_y = self.y - gear_offset * math.sin(math.radians(self.angle + 90))
            right_gear_x = self.x + gear_offset * math.cos(math.radians(self.angle - 90))
            right_gear_y = self.y - gear_offset * math.sin(math.radians(self.angle - 90))
            
            pygame.draw.line(screen, GRAY, (self.x, self.y), (left_gear_x, left_gear_y), 2)
            pygame.draw.line(screen, GRAY, (self.x, self.y), (right_gear_x, right_gear_y), 2)
        
        # Draw thrust flame if thrusting
        if self.thrust > 0:
            flame_length = 20 + random.randint(0, 10)
            flame_x = self.x - flame_length * math.cos(math.radians(self.angle))
            flame_y = self.y + flame_length * math.sin(math.radians(self.angle))
            
            # Flame color based on engine temperature
            if self.engine_temp > 800:
                flame_color = (255, 100, 100)
            elif self.engine_temp > 400:
                flame_color = ORANGE
            else:
                flame_color = YELLOW
                
            pygame.draw.line(screen, flame_color, (self.x, self.y), (flame_x, flame_y), 5)

class CelestialBody:
    """Celestial body class (Earth, Moon)"""
    
    def __init__(self, x: float, y: float, radius: int, color: Tuple[int, int, int], 
                 name: str, mass: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.name = name
        self.mass = mass
        self.orbit_angle = 0
        self.rotation = 0
        
    def update(self) -> None:
        """Update celestial body position"""
        if self.name == "Moon":
            # Moon orbits Earth
            self.orbit_angle += 0.002
            orbit_radius = MOON_DISTANCE
            # Elliptical orbit
            self.x = SCREEN_WIDTH // 2 + orbit_radius * math.cos(self.orbit_angle)
            self.y = SCREEN_HEIGHT // 2 + orbit_radius * math.sin(self.orbit_angle) * 0.5
        elif self.name == "Earth":
            # Earth rotates slowly
            self.rotation += 0.01
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the celestial body"""
        # Draw body with gradient effect
        for i in range(self.radius, 0, -10):
            alpha = int(255 * (i / self.radius))
            color = tuple(min(255, c * i // self.radius) for c in self.color)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), i)
        
        # Draw atmosphere for Earth
        if self.name == "Earth":
            pygame.draw.circle(screen, LIGHT_BLUE, (int(self.x), int(self.y)), 
                             self.radius + 15, 2)
        
        # Draw label
        label = f"{self.name}"
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y - self.radius - 20))
        screen.blit(text, text_rect)

class Particle:
    """Particle class for visual effects"""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], lifetime: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
    
    def update(self) -> bool:
        """Update particle position and return False if dead"""
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the particle"""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        size = max(1, int(3 * self.lifetime / self.max_lifetime))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Game:
    """Main game class"""
    
    def __init__(self) -> None:
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rocket to the Moon Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)
        
        # Stars for background
        self.stars = [(random.randint(0, SCREEN_WIDTH), 
                       random.randint(0, SCREEN_HEIGHT),
                       random.randint(1, 3)) 
                      for _ in range(200)]
        
        # Particles for effects
        self.particles: List[Particle] = []
        
        self.reset_game()
    
    def reset_game(self) -> None:
        """Reset the game to initial state"""
        self.rocket = Rocket()
        self.earth = CelestialBody(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                                   EARTH_RADIUS, BLUE, "Earth", EARTH_MASS)
        self.moon = CelestialBody(SCREEN_WIDTH // 2 + MOON_DISTANCE, SCREEN_HEIGHT // 2 - 100,
                                 MOON_RADIUS, GRAY, "Moon", MOON_MASS)
        self.state = GameState.PRE_LAUNCH
        self.countdown = 3
        self.countdown_timer = 0
        self.mission_time = 0
        self.particles.clear()
        self.message = ""
        self.message_timer = 0
        
    def create_exhaust_particles(self) -> None:
        """Create exhaust particles for visual effect"""
        if self.rocket.thrust > 0:
            for _ in range(5):
                angle_offset = random.uniform(-20, 20)
                particle_angle = self.rocket.angle + 180 + angle_offset
                speed = random.uniform(2, 5)
                vx = speed * math.cos(math.radians(particle_angle)) - self.rocket.vx * 0.1
                vy = speed * math.sin(math.radians(particle_angle)) - self.rocket.vy * 0.1
                
                self.particles.append(Particle(
                    self.rocket.x - 15 * math.cos(math.radians(self.rocket.angle)),
                    self.rocket.y + 15 * math.sin(math.radians(self.rocket.angle)),
                    vx, vy, ORANGE, 30
                ))
    
    def handle_events(self) -> bool:
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == GameState.PRE_LAUNCH:
                        self.state = GameState.COUNTDOWN
                        self.countdown_timer = pygame.time.get_ticks()
                        self.message = "Countdown started!"
                        self.message_timer = 120
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_l:
                    if self.state == GameState.LUNAR_ORBIT:
                        self.rocket.landing_gear = True
                        self.state = GameState.LUNAR_LANDING
                        self.message = "Landing gear deployed - Descending to Moon!"
                        self.message_timer = 120
                elif event.key == pygame.K_t:
                    if self.state == GameState.ON_MOON:
                        self.state = GameState.RETURN
                        self.message = "Beginning return journey to Earth!"
                        self.message_timer = 120
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Continuous key handling
        keys = pygame.key.get_pressed()
        
        if self.state in [GameState.LAUNCH, GameState.FLYING, GameState.ORBIT, 
                          GameState.TRANS_LUNAR, GameState.LUNAR_ORBIT, 
                          GameState.LUNAR_LANDING, GameState.RETURN,
                          GameState.EARTH_REENTRY]:
            if keys[pygame.K_UP]:
                self.rocket.apply_thrust(1.0)
                self.create_exhaust_particles()
                if self.state == GameState.LAUNCH:
                    self.state = GameState.FLYING
            if keys[pygame.K_LEFT]:
                self.rocket.rotate(5)
            if keys[pygame.K_RIGHT]:
                self.rocket.rotate(-5)
            if keys[pygame.K_DOWN]:
                # Retro thrust (braking)
                if self.rocket.fuel > 0:
                    self.rocket.apply_thrust(0.5)
                    self.create_exhaust_particles()
        
        return True
    
    def update(self) -> None:
        """Update game state"""
        self.mission_time += 1/60
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
        
        # Update celestial bodies
        self.earth.update()
        self.moon.update()
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Get telemetry
        telemetry = self.rocket.get_telemetry(self.earth, self.moon)
        
        # State-specific updates
        if self.state == GameState.COUNTDOWN:
            elapsed = (pygame.time.get_ticks() - self.countdown_timer) / 1000
            self.countdown = max(0, 3 - int(elapsed))
            if self.countdown == 0:
                self.state = GameState.LAUNCH
                self.message = "LAUNCH! Press UP to thrust!"
                self.message_timer = 120
        
        elif self.state in [GameState.LAUNCH, GameState.FLYING, GameState.ORBIT, 
                           GameState.TRANS_LUNAR, GameState.LUNAR_ORBIT, 
                           GameState.LUNAR_LANDING, GameState.RETURN,
                           GameState.EARTH_REENTRY]:
            
            # Update rocket physics
            self.rocket.update(self.earth, self.moon)
            
            # Check for phase transitions
            if self.state == GameState.FLYING:
                if telemetry.altitude_earth > ORBIT_ALTITUDE:
                    self.state = GameState.ORBIT
                    self.message = "Achieved Earth orbit! Head to the Moon!"
                    self.message_timer = 120
            
            elif self.state == GameState.ORBIT:
                if telemetry.distance_to_moon < MOON_DISTANCE * 0.8:
                    self.state = GameState.TRANS_LUNAR
                    self.message = "Trans-lunar injection! Approaching Moon!"
                    self.message_timer = 120
            
            elif self.state == GameState.TRANS_LUNAR:
                if telemetry.altitude_moon < MOON_RADIUS * 3:
                    self.state = GameState.LUNAR_ORBIT
                    self.message = "Lunar orbit achieved! Press L to land!"
                    self.message_timer = 120
            
            elif self.state == GameState.LUNAR_LANDING:
                # Check for lunar landing
                if telemetry.altitude_moon < 5:
                    if telemetry.velocity < SAFE_LANDING_SPEED:
                        self.state = GameState.ON_MOON
                        self.message = "SUCCESS! Landed on the Moon! Press T to return!"
                        self.message_timer = 180
                    else:
                        self.state = GameState.GAME_OVER
                        self.message = "CRASH! Landing too fast!"
                        self.message_timer = 180
            
            elif self.state == GameState.RETURN:
                if telemetry.altitude_earth < EARTH_RADIUS * 1.5:
                    self.state = GameState.EARTH_REENTRY
                    self.message = "Earth reentry! Use retro thrust to slow down!"
                    self.message_timer = 120
            
            elif self.state == GameState.EARTH_REENTRY:
                # Heat shield degradation
                self.rocket.heat_shield -= telemetry.velocity * 0.005
                
                if telemetry.altitude_earth < 5:
                    if telemetry.velocity < SAFE_LANDING_SPEED * 2 and self.rocket.heat_shield > 0:
                        self.state = GameState.LANDED
                        self.message = "MISSION ACCOMPLISHED! Successfully returned to Earth!"
                        self.message_timer = 180
                    else:
                        self.state = GameState.GAME_OVER
                        if self.rocket.heat_shield <= 0:
                            self.message = "Heat shield failed! Vehicle destroyed!"
                        else:
                            self.message = "CRASH! Landing too fast!"
                        self.message_timer = 180
        
        elif self.state == GameState.ON_MOON:
            # Keep rocket on moon surface
            dist_to_moon = math.sqrt((self.rocket.x - self.moon.x)**2 + 
                                    (self.rocket.y - self.moon.y)**2)
            if dist_to_moon < self.moon.radius + 5:
                # Place rocket on moon surface
                angle_to_moon = math.atan2(self.rocket.y - self.moon.y, 
                                          self.rocket.x - self.moon.x)
                self.rocket.x = self.moon.x + (self.moon.radius + 10) * math.cos(angle_to_moon)
                self.rocket.y = self.moon.y + (self.moon.radius + 10) * math.sin(angle_to_moon)
                self.rocket.vx = 0
                self.rocket.vy = 0
        
        elif self.state == GameState.LANDED:
            # Keep rocket on earth surface
            dist_to_earth = math.sqrt((self.rocket.x - self.earth.x)**2 + 
                                     (self.rocket.y - self.earth.y)**2)
            if dist_to_earth < self.earth.radius + 5:
                angle_to_earth = math.atan2(self.rocket.y - self.earth.y, 
                                           self.rocket.x - self.earth.x)
                self.rocket.x = self.earth.x + (self.earth.radius + 10) * math.cos(angle_to_earth)
                self.rocket.y = self.earth.y + (self.earth.radius + 10) * math.sin(angle_to_earth)
                self.rocket.vx = 0
                self.rocket.vy = 0
    
    def draw_hud(self) -> None:
        """Draw the heads-up display"""
        # Get telemetry
        telemetry = self.rocket.get_telemetry(self.earth, self.moon)
        
        # Draw mission time
        minutes = int(self.mission_time // 60)
        seconds = int(self.mission_time % 60)
        time_text = self.font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 200, 10))
        
        # Draw current state
        state_names = {
            GameState.PRE_LAUNCH: "Pre-Launch",
            GameState.COUNTDOWN: "Countdown",
            GameState.LAUNCH: "Launch",
            GameState.FLYING: "Ascending",
            GameState.ORBIT: "Earth Orbit",
            GameState.TRANS_LUNAR: "Trans-Lunar",
            GameState.LUNAR_ORBIT: "Lunar Orbit",
            GameState.LUNAR_LANDING: "Landing",
            GameState.ON_MOON: "On Moon",
            GameState.RETURN: "Returning",
            GameState.EARTH_REENTRY: "Re-entry",
            GameState.LANDED: "Landed",
            GameState.GAME_OVER: "Game Over"
        }
        state_text = self.small_font.render(f"Phase: {state_names.get(self.state, 'Unknown')}", 
                                           True, YELLOW)
        self.screen.blit(state_text, (SCREEN_WIDTH - 200, 40))
        
        # Draw telemetry panel
        panel_x = 10
        panel_y = 10
        line_height = 22
        
        # Fuel bar
        fuel_pct = telemetry.fuel / self.rocket.max_fuel
        bar_width = 150
        bar_height = 15
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, panel_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN, (panel_x, panel_y, 
                        int(bar_width * fuel_pct), bar_height))
        fuel_text = self.small_font.render(f"Fuel: {int(telemetry.fuel)}", True, WHITE)
        self.screen.blit(fuel_text, (panel_x + bar_width + 10, panel_y - 2))
        
        # Heat shield bar
        shield_pct = telemetry.heat_shield / 100
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, panel_y + 20, bar_width, bar_height))
        shield_color = GREEN if shield_pct > 0.5 else YELLOW if shield_pct > 0.2 else RED
        pygame.draw.rect(self.screen, shield_color, (panel_x, panel_y + 20,
                        int(bar_width * shield_pct), bar_height))
        shield_text = self.small_font.render(f"Shield: {int(telemetry.heat_shield)}%", True, WHITE)
        self.screen.blit(shield_text, (panel_x + bar_width + 10, panel_y + 18))
        
        # Other telemetry
        y_offset = 60
        telemetry_data = [
            f"Velocity: {telemetry.velocity:.1f} m/s",
            f"Vertical Speed: {-telemetry.velocity_y:.1f} m/s",
            f"Stage: {telemetry.stage}",
            f"Alt (Earth): {telemetry.altitude_earth:.0f}",
            f"Alt (Moon): {telemetry.altitude_moon:.0f}",
            f"Engine Temp: {self.rocket.engine_temp:.0f}°C",
            f"Landing Gear: {'✓' if self.rocket.landing_gear else '✗'}"
        ]
        
        for line in telemetry_data:
            text = self.small_font.render(line, True, GREEN)
            self.screen.blit(text, (panel_x, panel_y + y_offset))
            y_offset += line_height
    
    def draw(self) -> None:
        """Draw everything on screen"""
        self.screen.fill(BLACK)
        
        # Draw stars
        for x, y, size in self.stars:
            brightness = random.randint(150, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), 
                             (int(x), int(y)), size)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw celestial bodies
        self.earth.draw(self.screen, self.small_font)
        self.moon.draw(self.screen, self.small_font)
        
        # Draw rocket
        self.rocket.draw(self.screen, self.small_font)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw message if active
        if self.message_timer > 0 and self.message:
            # Semi-transparent background
            msg_surface = self.font.render(self.message, True, YELLOW)
            bg_rect = pygame.Rect(SCREEN_WIDTH//2 - msg_surface.get_width()//2 - 10,
                                 SCREEN_HEIGHT - 100,
                                 msg_surface.get_width() + 20,
                                 msg_surface.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
            self.screen.blit(msg_surface, 
                           (SCREEN_WIDTH//2 - msg_surface.get_width()//2, 
                            SCREEN_HEIGHT - 95))
        
        # Draw countdown
        if self.state == GameState.COUNTDOWN:
            countdown_text = self.title_font.render(str(self.countdown), True, RED)
            text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(countdown_text, text_rect)
        
        # Draw game over or success screen
        if self.state == GameState.GAME_OVER:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.title_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            if self.message:
                reason_text = self.font.render(self.message, True, WHITE)
                reason_rect = reason_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
                self.screen.blit(reason_text, reason_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
            self.screen.blit(restart_text, restart_rect)
        
        elif self.state == GameState.LANDED:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            success_text = self.title_font.render("MISSION SUCCESSFUL!", True, GREEN)
            text_rect = success_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(success_text, text_rect)
            
            time_text = self.font.render(f"Mission Time: {int(self.mission_time//60):02d}:{int(self.mission_time%60):02d}", 
                                        True, WHITE)
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(time_text, time_rect)
            
            restart_text = self.small_font.render("Press R to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main() -> None:
    """Main entry point"""
    print("=" * 60)
    print("                     ROCKET TO THE MOON SIMULATOR")
    print("=" * 60)
    print("\n█ CONTROLS:")
    print("  ↑ UP Arrow    - Apply thrust")
    print("  ↓ DOWN Arrow  - Retro thrust (braking)")
    print("  ← → Arrows    - Rotate rocket")
    print("  SPACE         - Start countdown")
    print("  L             - Deploy landing gear (in lunar orbit)")
    print("  T             - Begin return journey (on Moon)")
    print("  R             - Reset game")
    print("  ESC           - Quit")
    print("\n█ MISSION OBJECTIVES:")
    print("  1. Launch from Earth (press UP during countdown)")
    print("  2. Achieve Earth orbit (reach altitude > 200)")
    print("  3. Travel to the Moon")
    print("  4. Enter lunar orbit")
    print("  5. Land safely on the Moon (speed < 3 m/s)")
    print("  6. Return to Earth")
    print("  7. Survive reentry and land safely")
    print("\n█ TIPS:")
    print("  • Use gentle thrust - don't waste fuel")
    print("  • Monitor your speed during landing")
    print("  • Deploy landing gear before lunar descent")
    print("  • Use retro thrust (DOWN) to slow down")
    print("=" * 60)
    print("\nStarting game...\n")
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()