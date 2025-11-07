import sys

import pygame

from asteroidfield import *
from circleshape import CircleShape
from constants import *
from logger import log_state
from player import Player
from shot import Shot

pygame.init()
pygame.font.init()


# Set up the font object
font = pygame.font.Font(None, 36)


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    asteroids = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable,)
    Shot.containers = (updateable, drawable, shots)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    dt = clock.tick(60) / 1000
    asteroid_field = AsteroidField()

    score = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updateable.update(dt)

        # Draw the score to the screen
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game Over!")
                print(f"Final Score: {score}")
                sys.exit()
            for shot in shots:
                if shot.collision(asteroid):
                    score += SCORE_INCREMENT
                    asteroid.split()
                    shot.kill()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
