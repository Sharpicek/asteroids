import pygame, random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
from player import Player

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH) 
    
    def update(self, dt):
        self.position += self.velocity * dt

    def collizion(self, other):
        # 1. Get the direction vector between them (the collision normal)
        collision_normal = self.position - other.position
        
        # Handle the zero-distance edge case to avoid the crash
        if collision_normal.length() == 0:
            import pygame
            collision_normal = pygame.Vector2(1, 0)
        
        # 2. Separate them so they don't get stuck (your existing logic)
        distance = collision_normal.length()
        overlap = (self.radius + other.radius) - distance
        if overlap > 0:
            nudge = collision_normal.normalize() * (overlap / 2)
            self.position += nudge
            other.position -= nudge

        # 3. Realistic Physics: Reflect velocities
        # We normalize the normal to use it for reflection
        normal = collision_normal.normalize()
        negate_normal = -normal
        
        # self.velocity.reflect(normal) calculates the new bounce direction
        self.velocity = self.velocity.reflect(normal) 
        other.velocity = other.velocity.reflect(negate_normal)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(random_angle)
        velocity_b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_a.velocity = velocity_a * 1.2
        asteroid_b.velocity = velocity_b * 1.2
        
