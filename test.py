import pygame
import PyParticles

pygame.display.set_caption('Tutorial 10')
dimensions = (400, 400)
screen = pygame.display.set_mode(dimensions)
env = PyParticles.Environment(dimensions)

env.add_particles(5)

running = True
selected_particle = None
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