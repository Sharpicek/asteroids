import pygame, sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # Initialize pygame
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("===============================")

    # Game start settings
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    dt = 0
    pygame.font.init()
    font = pygame.font.SysFont("monospace", 35)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Infinite Game Loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print(f"Game Over! You score is {int(player.score)}.")
                sys.exit()
            
            for asteroid_other in asteroids:
                if asteroid.collides_with(asteroid_other):
                    asteroid.collizion(asteroid_other)
            
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    player.add_shoot_score(asteroid.radius)
                
        screen.fill("black")
        score_surface = font.render(f"Score: {int(player.score)}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        player.score += dt * 5 # 5 points per second alive

        for shape in drawable:
            shape.draw(screen)

        pygame.display.flip()

        # Limit FPS to 60
        dt = game_clock.tick(60) / 1000

if __name__ == "__main__":
    main()
