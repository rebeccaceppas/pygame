import random, pygame, PyParticles

class UniverseScreen:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dx, self.dy = (0, 0)
        self.mx, self.my = (0, 0)
        self.magnification = 1.0

    def scroll(self, dx=0, dy=0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
        
    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0



(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star Formation')

universe = PyParticles.Environment((width, height))
universe.colour = (0, 0, 0)
universe.add_functions(['move', 'attract', 'combine'])
universe_screen = UniverseScreen(width, height)

def calculate_radius(mass):
    return 2 * mass ** 0.5

for n in range(100):
    particle_mass = random.randint(1, 4)
    particle_size = calculate_radius(particle_mass)
    universe.add_particles(mass=particle_mass, size=calculate_radius(particle_mass), speed=0, colour=(255, 255, 255))

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.scroll(dx = 1)),
    pygame.K_RIGHT:  (lambda x: x.scroll(dx = -1)),
    pygame.K_DOWN:   (lambda x: x.scroll(dy = -1)),
    pygame.K_UP:     (lambda x: x.scroll(dy = 1)),
    pygame.K_EQUALS: (lambda x: x.zoom(2)),
    pygame.K_MINUS:  (lambda x: x.zoom(0.5)),
    pygame.K_r:      (lambda x: x.reset())}

clock = pygame.time.Clock()
paused = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                universe_screen.scroll(dx=1)
            elif event.key == pygame.K_RIGHT:
                universe_screen.scroll(dx=-1)
            elif event.key == pygame.K_UP:
                universe_screen.scroll(dy=1)
            elif event.key == pygame.K_DOWN:
                universe_screen.scroll(dy=-1)
            elif event.key == pygame.K_EQUALS:
                universe_screen.zoom(2)
            elif event.key == pygame.K_MINUS:
                universe_screen.zoom(0.5)
            elif event.key == pygame.K_r:
                universe_screen.reset()
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        universe.update()

    screen.fill(universe.colour)

    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculate_radius(p.mass)
            del p.__dict__['collide_with']

        mag = universe_screen.magnification
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * mag)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * mag)
        size = int(p.size * mag)

        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), int(p.size), 0)

    for p in particles_to_remove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()
    clock.tick(80)