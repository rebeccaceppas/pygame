import random, pygame, PyParticles

(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star Formation')

universe = PyParticles.Environment((width, height))
universe.colour = (0, 0, 0)
universe.add_functions(['move', 'attract', 'combine'])

def calculate_radius(mass):
    return 3 * mass ** 0.5

for n in range(100):
    particle_mass = random.randint(1, 5)
    particle_size = calculate_radius(particle_mass)
    universe.add_particles(mass=particle_mass, size=calculate_radius(particle_mass), speed=0, colour=(255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    universe.update()
    screen.fill(universe.colour)

    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculate_radius(p.mass)
            del p.__dict__['collide_with']

        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), int(p.size), 0)

    for p in particles_to_remove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()