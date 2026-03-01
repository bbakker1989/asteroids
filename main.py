import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # update everything that can be updated
        updatable.update(dt)
        for obj in asteroids:
            # check collision with player
            if obj.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            # check collision with shot
            for shot in shots:
                if obj.collides_with(shot):
                    log_event("asteroid_shot")
                    obj.split()
                    shot.kill()
            
        # draw a black screen
        screen.fill("black")
        # draw everything things that can be drawn
        for thing in drawable:
            thing.draw(screen)
        pygame.display.flip()

        # limite frame rate to 60 fps
        dt = (clock.tick(60)/1000) # ms -> s

if __name__ == "__main__":
    main()
