from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 128
height = 128

# Materiales
brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
wallMat = Material(diffuse = (37/255, 150/255, 190/255), spec = 8)
white = Material(diffuse = (0.1, 0.1, 0.1), spec = 8)
marble = Material(spec=64, texture= Texture("marble-tex-example.bmp"), matType= REFLECTIVE)

glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType= TRANSPARENT)
diamond = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 2.417, matType= TRANSPARENT)
mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
blueMat = Material(diffuse = (0, 0, 1), spec = 64, matType = OPAQUE)
marble5 = Material( diffuse = (171/255, 240/255, 1), texture = Texture("colored-tex-8.bmp"), spec = 32,  ior = 1.5, matType = TRANSPARENT) 

table = Material(diffuse = (67/255, 63/255, 60/255), spec = 30, matType = OPAQUE)
porcelain = Material(diffuse= (218/255, 217/255, 215/255), spec = 100, matType = OPAQUE)
coffee = Material(diffuse = (87/255,69/255,62/255), spec = 64, ior = 1.3354, matType= TRANSPARENT)
spoon = Material(diffuse = (136/255, 132/255, 131/255), spec = 20, matType= REFLECTIVE)
neon = Material(diffuse = (6/255,1,1/255), spec = 64, ior = 1.3354, matType= TRANSPARENT)

rtx = Raytracer(width, height)
# rtx.envMap = Texture("resources/envMap/brown_photostudio.bmp")

rtx.lights.append( AmbientLight(intensity = 0.5 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 1 ))

# rtx.lights.append( SpotLight(size=5, point = (0, -4, 0), lDir=[0, -1, 0], attenuation=1/2))
# rtx.lights.append( SpotLight(size=5, point = (0, 0, 0), lDir=[0, 0, -1], attenuation=1/2))

# rtx.scene.append(Triangle(A = (-0.5-1.5,0+0.5-0.5,-4), B = (1-1.5,1.7+0.5-0.5,-4), C = (0-1.5, 1.5+0.5-0.5, -4), material = marble5))
# rtx.scene.append( Disk(position = (0,-1.5,-4), radius = 1.5, normal = (0,1,0), material = table ))

# rtx.scene.append( AABB(position = (0,-3,-7), size = (2,2,2), material = marble))


# rtx.scene.append(Plane(position = (0, -10, 0), normal = (0, 1, 0), material = wallMat))
# rtx.scene.append(Plane(position = (0, 20, 0), normal = (0, -1, 0), material = wallMat))
# rtx.scene.append(Plane(position = (-10, 0, 0), normal = (1, 0, 0), material = wallMat))
# rtx.scene.append(Plane(position = (10, 0, 0), normal = (-1, 0, 0), material = wallMat))
# rtx.scene.append(Plane(position = (0, 0, -50), normal = (0, 0, 1), material = wallMat))

# rtx.scene.append(Triangle(A = (-0.5-1.5,0+0.5-0.5,-4), B = (1-1.5,1.7+0.5-0.5,-4), C = (0-1.5, 1.5+0.5-0.5, -4), material = marble5))
# rtx.scene.append(Triangle(A = (-1*(-0.5-1.5)-0.5 +0.35 ,-1*(0+0.5-1)-0.5-0.25,-4), B = (-1*(1-1.5)-0.5 + 0.35, -1*(1.7+0.5-1)-0.5-0.25,-4), C = (-1*(0-1.5)+0.25 + 0.35, -1*(1.5+0.5-1)-0.5-0.25, -4), material = wallMat))
# rtx.scene.append(Triangle(A = (-1 -0.1,0-0.5,-3.5), B = (1 -0.1,0-0.5,-3.5), C = (0 -0.1, 1.5-0.5, -3.5), material = wallMat))

# rtx.glLoadModel("resources/models/coffeeCup/coffeeCup6.obj",
#                  translate = V3(0, -1.4, -3.5),
#                  scale = V3(0.5, 0.5, 0.5),
#                  rotate = V3(7,0,0),
#                  material = porcelain)

rtx.glLoadModel("resources/models/coffeePlate/coffeePlate3.obj",
                 translate = V3(0, -1.5, -3.5),
                 scale = V3(0.5, 0.5, 0.5),
                 rotate = V3(7,0,0),
                 material = porcelain)


rtx.glLoadModel("resources/models/cookie/cookie.obj",
                 translate = V3(-1.8, -4.3, -2.5),
                 scale = V3(1, 1, 1),
                 rotate = V3(0,40,0),
                 material = Material(texture = Texture("resources/models/cookie/cookieTex.bmp")))

# rtx.glLoadModel("resources/models/coffeeSpoon/coffeeSpoon7.obj",
#                  translate = V3(0,0,0),
#                  scale = V3(5, 5, 5),
#                  rotate = V3(0,0,0))




# rtx.scene.append( Disk(position = (0,-0.6,-3.5), radius = 0.5, normal = (0,1,0), material = coffee ))


rtx.glRender()

rtx.glFinish("output-lights.bmp")