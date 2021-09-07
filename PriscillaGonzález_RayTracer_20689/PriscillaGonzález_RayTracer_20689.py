from gl import Raytracer, V3, _color
from obj import Obj, Texture

from figures import Sphere, Material

width = 512
height = 512

# Materiales
nose = Material(diffuse = _color(0.95,0.56,0.23))
snow = Material(diffuse = _color(1,1,1))
smile = Material(diffuse = _color(0.4,0.4,0.4))
button = Material(diffuse = _color(1,0,0))
eyes = Material(diffuse = _color(0.8,0.8,0.8))
pupil = Material(diffuse = _color(0,0,0))


rtx = Raytracer(width,height)

# Cuerpo
rtx.scene.append( Sphere(V3(0,10,-28), 4, snow) )
rtx.scene.append( Sphere(V3(0,-5,-20), 5, snow) )
rtx.scene.append( Sphere(V3(0,1.5,-20), 4, snow) )

# Boca
rtx.scene.append( Sphere(V3(0.5,8,-25), 0.5, smile) )
rtx.scene.append( Sphere(V3(-0.5,8,-25), 0.5, smile) )
rtx.scene.append( Sphere(V3(1.5,8.5,-25), 0.5, smile) )
rtx.scene.append( Sphere(V3(-1.5,8.5,-25), 0.5, smile) )

# Nariz
rtx.scene.append( Sphere(V3(0,5.7,-15), 0.5, nose) )

# Botones
rtx.scene.append( Sphere(V3(0,-4,-15), 1.2, button) )
rtx.scene.append( Sphere(V3(0,-0.5,-15), 0.8, button) )
rtx.scene.append( Sphere(V3(0,2.5,-15), 0.5, button) )

# Ojos
rtx.scene.append( Sphere(V3(0.7,8.5,-19), 0.5, eyes) )
rtx.scene.append( Sphere(V3(-0.7,8.5,-19), 0.5, eyes) )

# Pupila
rtx.scene.append( Sphere(V3(0.7,8,-18), 0.2, pupil) )
rtx.scene.append( Sphere(V3(-0.7,8,-18), 0.2, pupil) )

rtx.glRender()

rtx.glFinish('output.bmp')
