import numpy as np
from gl import WHITE
from mathLi import *

class Material(object):
    def __init__(self, diffuse = WHITE):
        self.diffuse = diffuse

class Intersect(object):
    def __init__(self, distance):
        self.distance = distance

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):

        # P = O + t * D

        #L = np.subtract(self.center, orig)
        L = resta2(self.center, orig)
       
        l = np.linalg.norm(L)
        #l = normalized(L)

        #tca = np.dot(L, dir)
        tca = pShader(L, dir)

        d = (l**2 - tca**2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius**2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        return Intersect( distance = t0 )

