import pygame
import PyParticles
import math

pygame.display.set_caption('Tutorial 10')
(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))
env = PyParticles.Environment((width, height))
env.add_functions(['move', 'bounce', 'attract'])
#env.acceleration = (math.pi, 0.002)
env.add_particles(100, size = 1)

selected_particle = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_particle = env.find_particle(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        selected_particle.mouse_move(pygame.mouse.get_pos())
    
    env.update()
    screen.fill(env.colour)

    for p in env.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)

    pygame.display.flip()