import struct
from collections import namedtuple
from obj import _color

import numpy as np
from numpy import sin, cos, tan
import random
from mathLi import *

STEPS = 1
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3 # Cuantas veces se puede reobatr un rayo para hacer un reflejo

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

def _color(r, g, b):
    # Acepta valores de 0 a 1
    # Se asegura que la información de color se guarda solamente en 3 bytes
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    try:
        #PCB/ABC
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        #PCA/ABC
        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

def reflectVector(normal, dirVector):
    # R = 2 * ( N . L) * N - L
    #reflect = 2 * np.dot(normal, dirVector)
    reflect = 2 * pShader(normal, dirVector)
    #reflect = np.multiply(reflect, normal)
    reflect = np.multiply(reflect, normal)
    #reflect = np.subtract(reflect, dirVector)
    reflect = resta2(reflect, dirVector) #verificar porque sale una línea en vez de un punto
    #reflect = reflect / np.linalg.norm(reflect)
    reflect = reflect / np.linalg.norm(reflect)
    return reflect

def refractVector(normal, dirVector, ior): # ior = índice de refracción
    # Snell´s law
    # Asegurar que no se apse de una valor de -1 a 1
    #cosi = max(-1, min(1, np.dot(dirVector, normal)))
    cosi = max(-1, min(1, pShader(dirVector, normal)))
    etai = 1
    etat = ior

    # Rayo adentro del objeto, por lo que se estaría reflejando por dentro del objeto
    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        normal = np.array(normal) * -1

    eta = etai / etat

    # Determina si se tiene reflección interna
    k = 1 - eta * eta * (1 - (cosi * cosi))

    # Ya no hay refracción, solo reflección
    if k < 0:
        return None

    # Se genera un rayo de refracción
    R = eta * np.array(dirVector) + (eta * cosi - k**0.5) * normal
    return R / np.linalg.norm(R)

def fresnel(normal, dirVector, ior):
    #cosi = max(-1, min(1, np.dot(dirVector, normal)))
    cosi = max(-1, min(1, pShader(dirVector, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    # Revisar si hay reflección interna o no
    # Solo hay reflección y no refracción
    if sint >= 1:
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))

    return (Rs * Rs + Rp * Rp) / 2

BLACK = _color(0,0,0)
WHITE = _color(1,1,1)


class Raytracer(object):
    def __init__(self, width, height):
        #Constructor
        self.curr_color = (1,1,1)
        self.clear_color = (0,0,0)
        self.glCreateWindow(width, height)

        self.camPosition = V3(0,0,0)
        self.fov = 60

        self.background = None

        self.scene = []

        self.pointLights = []
        self.ambLight = None
        self.dirLight = None
        self.envmap = None


    def glFinish(self, filename):
        #Crea un archivo BMP y lo llena con la información dentro de self.pixels
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write( _color(self.pixels[x][y][0],
                                       self.pixels[x][y][1],
                                       self.pixels[x][y][2]))


    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)


    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = int(width)
        self.vpHeight = int(height)


    def glClearColor(self, r, g, b):
        self.clear_color = (r, g, b)


    def glClear(self):
        #Crea una lista 2D de pixeles y a cada valor le asigna 3 bytes de color
        self.pixels = [[ self.clear_color for y in range(self.height)]
                         for x in range(self.width)]

    def glClearBackground(self):
        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth):
                for y in range(self.vpY, self.vpY + self.vpHeight):

                    tx = (x - self.vpX) / self.vpWidth
                    ty = (y - self.vpY) / self.vpHeight

                    self.glPoint(x,y, self.background.getColor(tx, ty))



    def glViewportClear(self, color = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x, y, color)


    def glColor(self, r, g, b):
        self.curr_color = (r,g,b)

    def glPoint(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color


    def glRender(self):
        for y in range(0, self.height, STEPS):
            for x in range(0, self.width , STEPS):
                # pasar de coordenadas de ventana a coordenadas NDC (-1 a 1)
                Px = 2 * ((x + 0.5) / self.width) - 1
                Py = 2 * ((y + 0.5) / self.height) - 1

                # Angulo de vision, asumiendo que el near plane esta a 1 unidad de la camara
                t = tan( (self.fov * pi() / 180) / 2)
                r = t * self.width / self.height

                Px *= r
                Py *= t

                #La camara siempre esta viendo hacia -Z
                direction = V3(Px, Py, -1)
                direction = direction / np.linalg.norm(direction)

                self.glPoint(x,y, self.cast_ray(self.camPosition, direction))


    def scene_intersect(self, orig, dir, origObj = None): # Se genera desde la cámara con None
        depth = float('inf')
        intersect = None

        for obj in self.scene:
            # No revisará si se genera desde el mismo objeto
            if obj is not origObj:
                hit = obj.ray_intersect(orig,dir)
                if hit != None:
                    if hit.distance < depth:
                        depth = hit.distance
                        intersect = hit

        return intersect

    def cast_ray(self, orig, dir, origObj = None, recursion = 0):
        intersect = self.scene_intersect(orig, dir, origObj)

        # No toca con nada regresar color de fondo pero también si es más garnde que los saltos
        if intersect == None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(dir) # Se le pasa la dirección del rayo
            return self.clear_color

        material = intersect.sceneObject.material

        # Colors
        finalColor = np.array([0,0,0])
        objectColor = np.array([material.diffuse[0],
                                material.diffuse[1],
                                material.diffuse[2]])

        ambientColor = np.array([0,0,0])
        dirLightColor = np.array([0,0,0])
        pLightColor = np.array([0,0,0])
        finalSpecColor = np.array([0,0,0])
        reflectColor = np.array([0,0,0])
        refractColor = np.array([0,0,0])

        # Direccion de vista
        #view_dir = np.subtract(self.camPosition, intersect.point)
        view_dir = resta2(self.camPosition, intersect.point)
        view_dir = view_dir / np.linalg.norm(view_dir)

        if self.ambLight:
            ambientColor = np.array(self.ambLight.getColor())

        if self.dirLight:
            diffuseColor = np.array([0,0,0])
            specColor = np.array([0,0,0])
            shadow_intensity = 0

            # Iluminacion difusa
            light_dir = np.array( self.dirLight.direction) * -1
            #intensity = max(0, np.dot(intersect.normal, light_dir)) * self.dirLight.intensity
            intensity = max(0, pShader(intersect.normal, light_dir)) * self.dirLight.intensity
            diffuseColor = np.array([intensity * self.dirLight.color[0],
                                     intensity * self.dirLight.color[1],
                                     intensity * self.dirLight.color[2]])

            # Iluminacion especular
            reflect = reflectVector(intersect.normal, light_dir)
            #spec_intensity = self.dirLight.intensity * max(0,np.dot(view_dir, reflect)) ** material.spec
            spec_intensity = self.dirLight.intensity * max(0, pShader(view_dir, reflect)) ** material.spec
            specColor = np.array([spec_intensity * self.dirLight.color[0],
                                  spec_intensity * self.dirLight.color[1],
                                  spec_intensity * self.dirLight.color[2]])

            # Shadow
            shadInter = self.scene_intersect(intersect.point, light_dir, intersect.sceneObject)
            
            # Sombra de la luz direccional 
            if shadInter:
                shadow_intensity = 1

            # Sombra de la luz direccional 
            dirLightColor = (1 - shadow_intensity) * diffuseColor
            finalSpecColor = np.add(finalSpecColor, (1 - shadow_intensity) * specColor)


        for pointLight in self.pointLights:
            diffuseColor = np.array([0,0,0])
            specColor = np.array([0,0,0])
            shadow_intensity = 0

            # Iluminacion difusa
            #light_dir = np.subtract(pointLight.position, intersect.point)
            light_dir = resta2(pointLight.position, intersect.point)
            light_dir = light_dir / np.linalg.norm(light_dir)
            #intensity = max(0, np.dot(intersect.normal, light_dir)) * pointLight.intensity
            intensity = max(0, pShader(intersect.normal, light_dir)) * pointLight.intensity
            diffuseColor = np.array([intensity * pointLight.color[0],
                                     intensity * pointLight.color[1],
                                     intensity * pointLight.color[2]])

            # Iluminacion especular
            reflect = reflectVector(intersect.normal, light_dir)
            spec_intensity = pointLight.intensity * max(0,np.dot(view_dir, reflect)) ** material.spec
            specColor = np.array([spec_intensity * pointLight.color[0],
                                  spec_intensity * pointLight.color[1],
                                  spec_intensity * pointLight.color[2]])

            # Shadows
            shadInter = self.scene_intersect(intersect.point, light_dir, intersect.sceneObject)
            
            # Sombra del pointlight 
            #lightDistance = np.linalg.norm( np.subtract(pointLight.position, intersect.point) )
            lightDistance = np.linalg.norm(resta2(pointLight.position, intersect.point) )
            if shadInter and shadInter.distance < lightDistance:
                shadow_intensity = 1

            #pLightColor = np.add(pLightColor, (1 - shadow_intensity) * diffuseColor)
            pLightColor = suma(pLightColor, (1 - shadow_intensity) * diffuseColor)
            #finalSpecColor = np.add(finalSpecColor, (1 - shadow_intensity) * specColor)
            finalSpecColor = suma(finalSpecColor, (1 - shadow_intensity) * specColor)


        if material.matType == OPAQUE:
            finalColor = pLightColor + ambientColor + dirLightColor + finalSpecColor

        elif material.matType == REFLECTIVE:
            # Nuevo vector de reflejo
            reflect = reflectVector(intersect.normal, np.array(dir) * -1)
            # Generar el rayo
            reflectColor = self.cast_ray(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = np.array([reflectColor[0],
                                     reflectColor[1],
                                     reflectColor[2]])

            finalColor = reflectColor + finalSpecColor

        elif material.matType == TRANSPARENT:
            # Vector interno o externo
            #outside = np.dot(dir, intersect.normal) < 0
            outside = pShader(dir, intersect.normal) < 0
            # Gerenara rayos a cierta superficie para evitar que colapsen entre sí mismos y que no toque la superficie
            bias = 0.001 * intersect.normal
            kr = fresnel(intersect.normal, dir, material.ior)

            reflect = reflectVector(intersect.normal, np.array(dir) * -1)
            #reflectOrig = np.add(intersect.point, bias) if outside else np.subtract(intersect.point, bias)
            reflectOrig = suma(intersect.point, bias) if outside else resta2(intersect.point, bias)
            # Rayo
            reflectColor = self.cast_ray(reflectOrig, reflect, None, recursion + 1)
            reflectColor = np.array(reflectColor)

            if kr < 1:
                refract = refractVector(intersect.normal, dir, material.ior ) # dir = dirección del rayo entrante
                # Para que empiece abajito de la superficie
                #refractOrig = np.subtract(intersect.point, bias) if outside else np.add(intersect.point, bias)
                refractOrig = resta2(intersect.point, bias) if outside else suma(intersect.point, bias)
                refractColor = self.cast_ray(refractOrig, refract, None, recursion + 1)
                refractColor = np.array(refractColor)

            finalColor = reflectColor * kr + refractColor * (1 - kr) + finalSpecColor

        # Le aplicamos el color del objeto
        finalColor *= objectColor

        #Nos aseguramos que no suba el valor de color de 1
        r = min(1, finalColor[0])
        g = min(1, finalColor[1])
        b = min(1, finalColor[2])
    
        return (r,g,b)

