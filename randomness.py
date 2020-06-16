import pygame
import random

pygame.init()

background_colour = (255,255,255)
(width, height) = (300, 200)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Circles')
screen.fill(background_colour)

class Particle:

    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        
    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

number_of_particles = 10
my_particles = []

for n in range(number_of_particles):
    size = random.randint(10,20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    my_particles.append(Particle((x, y), size))

for particle in my_particles:
    particle.display()

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False