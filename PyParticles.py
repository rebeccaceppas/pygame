import math, random

def add_vectors(v1, v2):

    ''' Returns sum of two vectors '''

    angle1, length1 = v1
    angle2, length2 = v2 
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    length = math.hypot(x, y)
    angle = math.pi/2 - math.atan2(y, x)

    return (angle, length)

def collide(p1, p2):

    ''' Tests whether two particles overlap and creates collision event '''

    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy)
    if distance < p1.size + p2.size:
        angle = math.pi/2 + math.atan2(dy, dx)
        total_mass = p1.mass + p2.mass
        
        (p1.angle, p1.speed) = add_vectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = add_vectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))
        
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap

def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y, p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x * p1.mass + p2.x * p2.mass) / total_mass
        p1.y = (p1.y * p1.mass + p2.y * p2.mass) / total_mass
        (p1.angle, p1.speed) = add_vectors((p1.angle, p1.speed * p1.mass / total_mass), p2.angle, p2.speed * p2.mass / total_mass)
        p1.speed *= (p1.elasticity * p2.elasticity)
        p1.mass += p2.mass
        p1.collide_with = p2


class Particle:

    ''' Circular object with a size, mass and velocity '''

    def __init__(self, position, size, mass=1):
        self.x, self.y = position
        self.size = size
        self.mass = mass
        self.colour = (0,0,255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.drag = 1
        self.elasticity = 0.9

    def move(self):

        ''' Updates position based on speed, angle and drag '''

        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def accelerate(self, vector):

        ''' Change angle and speed by a given vector '''

        (self.angle, self.speed) = add_vectors((self.angle, self.speed), vector)

    def experience_drag(self):

        ''' Slow particle down through drag '''
        self.speed *= self.drag

    def mouse_move(self, position):

        """ Change angle and speed to move towards a given point """

        x, y = position
        dx = x - self.x
        dy = y - self.y
        self.angle = math.pi/2 + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

    def attract(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.hypot(dx, dy)

        theta = math.atan2(dy, dx)
        force = 6 * self.mass * other.mass / dist ** 2

        self.accelerate((theta - math.pi/2, force / self.mass))
        other.accelerate((theta + math.pi/2, force / other.mass))


class Environment:

    ''' Defines boundary of simulation and its properties '''

    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.particles = []
        
        self.colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = (0,0)

        self.particle_functions1 = []
        self.particle_functions2 = []
        self.functions_dict = {
            'move': (1, lambda p: p.move()),
            'drag': (1, lambda p: p.experience_drag()),
            'bounce': (1, lambda p: self.bounce(p)),
            'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
            'collide': (2, lambda p1, p2: collide(p1, p2)),
            'attract': (2, lambda p1, p2: p1.attract(p2))
        }

    def add_functions(self, function_list):
        for func in function_list:
            (n, f) = self.functions_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print('No such function %s' % f)



    def add_particles(self, n=1, **kwargs):

        ''' Add n particles with properties given by keyword arguments '''

        for i in range(n):
            size = kwargs.get('size', random.randint(10,20))
            mass = kwargs.get('mass', random.randint(100, 10000))
            x = kwargs.get('x', random.uniform(size, self.width - size))
            y = kwargs.get('y', random.uniform(size, self.height - size))

            p = Particle((x,y), size, mass)
            
            p.speed = kwargs.get('speed', random.random())
            p.angle = kwargs.get('angle', random.uniform(0, math.pi*2))
            p.colour = kwargs.get('colour', (0, 0, 255))
            p.drag = (p.mass/(p.mass + self.mass_of_air)) ** p.size

            self.particles.append(p)

    def update(self):

        ''' Moves particles and tests for collisions '''

        for i, particle in enumerate(self.particles):
            for f in self.particle_functions1:
                f(particle)
            for particle2 in self.particles[i+1:]:
                for f in self.particle_functions2:
                    f(particle, particle2)


    def bounce(self, p):

        ''' Tests whether a particle has hit a boundary '''
        
        if p.x > self.width - p.size:
            p.x = 2 * (self.width - p.size) - p.x
            p.angle = - p.angle
            p.speed *= self.elasticity
        elif p.x < p.size:
            p.x = 2 * p.size - p.x
            p.angle = - p.angle
            p.speed *= self.elasticity

        
        if p.y > self.height - p.size:
            p.y = 2 * (self.height - p.size) - p.y
            p.angle = math.pi - p.angle
            p.speed *= self.elasticity
        elif p.y < p.size:
            p.y = 2 * p.size - p.y
            p.angle = math.pi - p.angle
            p.speed *= self.elasticity
    

    def find_particle(self, position):

        ''' Returns particle that occupies position (x, y) '''
        
        x, y = position
        for p in self.particles:
            if math.hypot(p.x - x, p.y - y) <= p.size:
                return p