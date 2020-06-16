import pygame
import random
import math

background_colour = (255,255,255)
(width, height) = (400, 400)
drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.002)


def add_vectors(v1, v2):
    angle1, length1 = v1
    angle2, length2 = v2 
    x = math.cos(angle1) * length1 + math.cos(angle2) * length2
    y = math.sin(angle1) * length1 + math.sin(angle2) * length2
    length = math.hypot(x, y)
    angle = math.pi/2 - math.atan2(y, x)
    return (length, angle)

class Particle():

    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = add_vectors((self.angle, self.speed), gravity)
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = - self.angle
            self.speed *= elasticity


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Movement')


number_of_particles = 10
my_particles = []

for n in range(number_of_particles):
    size = random.randint(10,20)
    position = (random.randint(size, width - size), random.randint(size, height - size))
    particle = Particle(position, size)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)
    my_particles.append(particle)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)

    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()
        
    pygame.display.flip()