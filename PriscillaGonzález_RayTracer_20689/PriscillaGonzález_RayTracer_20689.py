from gl import Raytracer, V3
from obj import *
from figures import *

# Dimensiones
width = 1024
height = 1024
#width = 512
#height = 512

# Materiales
other = Material(diffuse = (0.6,0.4,0.8), spec = 64)
other2 = Material(diffuse = (0.35,0.77,0.7), spec = 64)
mirror = Material(spec = 128, matType = REFLECTIVE)
gold = Material(diffuse = (1, 0.8, 0 ),spec = 32, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType = TRANSPARENT)
water = Material(spec = 64, ior = 1.33, matType = TRANSPARENT)
#wood = Material(diffuse = (0.4,0.4,0.4), spec = 64)
stone = Material(diffuse = (0.4,0.4,0.4), spec = 64)
silver = Material(diffuse = (0.75,0.75,0.75),spec = 32, matType = REFLECTIVE)

# Inicializacion
rtx = Raytracer(width,height)
rtx.envmap = EnvMap('envMap2.bmp')

# Luces
rtx.ambLight = AmbientLight(strength = 0.1)
rtx.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
rtx.pointLights.append( PointLight(position = V3(0, 2, 0), intensity = 0.5))

# Objetos
rtx.scene.append( Sphere(V3(-3,3,-8), 1, other ))
rtx.scene.append( Sphere(V3(3,3,-8), 1, silver ))
rtx.scene.append( Sphere(V3(-3,-3,-8), 1, gold ))
rtx.scene.append( Sphere(V3(3,-3,-8), 1, other2 ))
rtx.scene.append( Sphere(V3(3,-3,-8), 1, other2 ))
rtx.scene.append( Sphere(V3(-1.5,0,-8), 1, glass ))
rtx.scene.append( Sphere(V3(1.5,0,-8), 1, water ))
#rtx.scene.append( Sphere(V3(-2,0,-8), 1, glass ))
#rtx.scene.append( Sphere(V3(2,0,-8), 1, water ))
#rtx.scene.append( Plane(V3(0,-3,0), V3(0,1,0), stone))
#rtx.scene.append( Plane(V3(0,3,0), V3(0,-1,0), stone))
#rtx.scene.append( Plane(V3(-3,0,0), V3(1,0,0), other))
#rtx.scene.append( Plane(V3(3,0,0), V3(-1,0,0), other))
#rtx.scene.append( Plane(V3(0,0,-15), V3(0,0,1), other))
##rtx.scene.append( Sphere(V3(-1,1,-5), 0.5, mirror ))
#rtx.scene.append( Sphere(V3(0.5,0.5,-5), 0.5, gold ))
#rtx.scene.append( AABB(V3(-2,-2,-8), V3(2,2,2), glass))

# Terminar
rtx.glRender()
rtx.glFinish('output.bmp')

## Materiales
#nose = Material(diffuse = _color(0.95,0.56,0.23))
#snow = Material(diffuse = _color(1,1,1))
#smile = Material(diffuse = _color(0.4,0.4,0.4))
#button = Material(diffuse = _color(1,0,0))
#eyes = Material(diffuse = _color(0.8,0.8,0.8))
#pupil = Material(diffuse = _color(0,0,0))

#rtx = Raytracer(width,height)

## Cuerpo
#rtx.scene.append( Sphere(V3(0,10,-28), 4, snow) )
#rtx.scene.append( Sphere(V3(0,-5,-20), 5, snow) )
#rtx.scene.append( Sphere(V3(0,1.5,-20), 4, snow) )

## Boca
#rtx.scene.append( Sphere(V3(0.5,8,-25), 0.5, smile) )
#rtx.scene.append( Sphere(V3(-0.5,8,-25), 0.5, smile) )
#rtx.scene.append( Sphere(V3(1.5,8.5,-25), 0.5, smile) )
#rtx.scene.append( Sphere(V3(-1.5,8.5,-25), 0.5, smile) )

## Nariz
#rtx.scene.append( Sphere(V3(0,5.7,-15), 0.5, nose) )

## Botones
#rtx.scene.append( Sphere(V3(0,-4,-15), 1.2, button) )
#rtx.scene.append( Sphere(V3(0,-0.5,-15), 0.8, button) )
#rtx.scene.append( Sphere(V3(0,2.5,-15), 0.5, button) )

## Ojos
#rtx.scene.append( Sphere(V3(0.7,8.5,-19), 0.5, eyes) )
#rtx.scene.append( Sphere(V3(-0.7,8.5,-19), 0.5, eyes) )

## Pupila
#rtx.scene.append( Sphere(V3(0.7,8,-18), 0.2, pupil) )
#rtx.scene.append( Sphere(V3(-0.7,8,-18), 0.2, pupil) )

