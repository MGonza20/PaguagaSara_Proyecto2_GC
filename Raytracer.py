from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 1024
height = 1024

# Materiales
table = Material(diffuse = (67/255, 63/255, 60/255), spec = 30, matType = OPAQUE)
porcelain = Material(diffuse= (218/255, 217/255, 215/255), spec = 80, matType = OPAQUE)
coffee = Material(diffuse = (176/255, 140/255, 119/255), spec = 64, ior = 1.3354, matType= TRANSPARENT)
spoon = Material(diffuse = (136/255, 132/255, 131/255), spec = 20, matType= REFLECTIVE)

rtx = Raytracer(width, height)
# Enviroment Map
rtx.envMap = Texture("resources/envMap/brown_photostudio.bmp")

# Lights
rtx.lights.append( AmbientLight(intensity = 0.5 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.55 ))
rtx.lights.append( SpotLight(size=25, point = (0, -0.75, 0), attenuation=1, color = (243/255, 238/255, 196/255)))

# Mesa
rtx.scene.append( Disk(position = (0,-1.5,-4), radius = 1.5, normal = (0,1,0), material = table ))

# Taza de cafe
rtx.glLoadModel("resources/models/coffeeCup/coffeeCup6.obj",
                 translate = V3(0, -1.5, -3.5),
                 scale = V3(0.5, 0.5, 0.5),
                 rotate = V3(7,0,0),
                 material = porcelain)

# Plato
rtx.glLoadModel("resources/models/coffeePlate/coffeePlate3.obj",
                 translate = V3(0, -1.5, -3.5),
                 scale = V3(0.5, 0.5, 0.5),
                 rotate = V3(7,0,0),
                 material = porcelain)

# Galleta
rtx.glLoadModel("resources/models/cookie/cookie.obj",
                 translate = V3(-1.8, -4.3, -2.5),
                 scale = V3(1, 1, 1),
                 rotate = V3(0,40,0),
                 material = Material(texture = Texture("resources/models/cookie/cookieTex.bmp")))

# Cuchara
rtx.glLoadModel("resources/models/coffeeSpoon/coffeeSpoon9.obj",
                 translate = V3(1.65-0.35, -4.1+0.35, -1.65-0.2),
                 scale = V3(0.8,0.8,0.8),
                 rotate = V3(0,80,0),
                 material = spoon)

# Cafe
rtx.scene.append( Disk(position = (0,-0.7,-3.5), radius = 0.5, normal = (0,1,0), material = coffee ))


rtx.glRender()

rtx.glFinish("output.bmp")