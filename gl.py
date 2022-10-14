import struct
from collections import namedtuple
from figures import *
from lights import *
from math import cos, sin, tan, pi
from obj import Obj
from figures import *


STEPS = 1
MAX_RECURSION_DEPTH = 3

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)] )

def baryCoords(A, B, C, P):

    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w

class Raytracer(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.fov = 60
        self.nearPlane = 0.1
        self.camPosition = V3(0,0,0)

        self.scene = [ ]
        self.lights = [ ]

        self.envMap = None


        self.clearColor = color(0,0,0)
        self.currColor = color(1,1,1)

        self.glViewport(0,0,self.width, self.height)
        
        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[ self.clearColor for y in range(self.height)]
                         for x in range(self.width)]

    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)


    def glPoint(self, x, y, clr = None): # Window Coordinates
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def glCreateRotationMatrix(self, pitch = 0, yaw = 0, roll = 0):
        
        pitch *= pi/180
        yaw   *= pi/180
        roll  *= pi/180

        pitchMat = [[1, 0, 0, 0],
                    [0, cos(pitch),-sin(pitch), 0],
                    [0, sin(pitch), cos(pitch), 0],
                    [0, 0, 0, 1]]

        yawMat = [[cos(yaw), 0, sin(yaw), 0],
                  [0, 1, 0, 0],
                  [-sin(yaw), 0, cos(yaw), 0],
                  [0, 0, 0, 1]]

        rollMat = [[cos(roll),-sin(roll), 0, 0],
                   [sin(roll), cos(roll), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]]

        return mm(mm(pitchMat, yawMat), rollMat)


    def glCreateObjectMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):

        translation = [[1, 0, 0, translate.x],
                       [0, 1, 0, translate.y],
                       [0, 0, 1, translate.z],
                       [0, 0, 0, 1]]

        rotation = self.glCreateRotationMatrix(rotate.x, rotate.y, rotate.z)

        scaleMat = [[scale.x, 0, 0, 0],
                    [0, scale.y, 0, 0],
                    [0, 0, scale.z, 0],
                    [0, 0, 0, 1]]

        return mm(mm(translation, rotation), scaleMat)

    def scene_intersect(self, orig, dir, sceneObj):
        depth = float('inf')
        intersect = None

        for obj in self.scene:
            hit = obj.ray_intersect(orig, dir)
            if hit != None:
                if sceneObj != hit.sceneObj:
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance

        return intersect

    def cast_ray(self, orig, dir, sceneObj = None, recursion = 0):
        intersect = self.scene_intersect(orig, dir, sceneObj)

        if intersect == None or recursion >= MAX_RECURSION_DEPTH:
            if self.envMap:
                return self.envMap.getEnvColor(dir)
            else:
                return (self.clearColor[0] / 255,
                        self.clearColor[1] / 255,
                        self.clearColor[2] / 255)

        material = intersect.sceneObj.material

        finalColor = [0,0,0]
        objectColor = [material.diffuse[0],
                       material.diffuse[1],
                       material.diffuse[2]]

        if material.matType == OPAQUE:
            for light in self.lights:
                diffuseColor = light.getDiffuseColor(intersect, self)
                specColor = light.getSpecColor(intersect, self)
                shadowIntensity = light.getShadowIntensity(intersect, self)

                lightColorSum = addVectors(diffuseColor, specColor)

                lightColor = [lightColorSum[0] * (1 - shadowIntensity),
                              lightColorSum[1] * (1 - shadowIntensity),
                              lightColorSum[2] * (1 - shadowIntensity)]

                finalColor = addVectors(finalColor, lightColor)

        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intersect.normal, [dir[0] * -1, dir[1] * -1, dir[2] * -1,])
            reflectColor = self.cast_ray(intersect.point, reflect, intersect.sceneObj, recursion + 1)
            reflectColor = reflectColor

            specColor = [0,0,0]
            for light in self.lights:
                specColor = addVectors(specColor, light.getSpecColor(intersect, self))

            finalColor = addVectors(reflectColor, specColor)

        elif material.matType == TRANSPARENT:
            outside = dotProduct(dir, intersect.normal) < 0 # Verificar si el rayo viene de adentro o fuero
            bias =  [intersect.normal[0] * 0.001, 
                     intersect.normal[1] * 0.001, 
                     intersect.normal[2] * 0.001]

            specColor = [0,0,0]
            for light in self.lights:
                specColor = addVectors(specColor, light.getSpecColor(intersect, self))

            reflect = reflectVector(intersect.normal, [dir[0] * -1, dir[1] * -1, dir[2] * -1,])
            reflectOrig = addVectors(intersect.point, bias) if outside else subtractVList(intersect.point, bias)
            reflectColor = self.cast_ray(reflectOrig, reflect, None, recursion + 1)

            kr = fresnel(intersect.normal, dir, material.ior)

            refractColor = [0, 0, 0]
            if kr < 1:
                refract = refractVector(intersect.normal, dir, material.ior)
                refractOrig = subtractVList(intersect.point, bias) if outside else  addVectors(intersect.point, bias)
                refractColor = self.cast_ray(refractOrig, refract, None, recursion + 1)

            nReflectColor = [reflectColor[0] * kr, reflectColor[1] * kr, reflectColor[2] * kr]
            nRefractColor = [refractColor[0] * (1 - kr), refractColor[1] * (1 - kr), refractColor[2] * (1 - kr)]

            firstSum = addVectors(nReflectColor, nRefractColor)
            secondSum = addVectors(firstSum, specColor)
            finalColor = secondSum


        finalColorArr = [finalColor[0] * objectColor[0],
                         finalColor[1] * objectColor[1],
                         finalColor[2] * objectColor[2]]

        if material.texture and intersect.texcoords:
            texColor = material.texture.getColor(intersect.texcoords[0], intersect.texcoords[1])

            if texColor is not None:
                finalColorArr = [finalColorArr[0] * texColor[0],
                                finalColorArr[1] * texColor[1],
                                finalColorArr[2] * texColor[2]]

        r = min(1, finalColorArr[0])
        g = min(1, finalColorArr[1])
        b = min(1, finalColorArr[2])

        return (r,g,b)


    def glTransform(self, vertex, matrix):
        v = V4(vertex[0], vertex[1], vertex[2], 1)
        v = [[v.x], [v.y], [v.z], [v.w]]

        vt = mm(matrix, v)
        vf = V3(vt[0][0] / vt[3][0], 
                vt[1][0] /vt[3][0], 
                vt[2][0] /vt[3][0])

        return vf


    def glLoadModel(self, filename, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1), material = Material(diffuse = (0.1, 0.1, 0.1), spec = 1.0, ior = 1.0, texture = None, matType = OPAQUE)):
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]
            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]

            v0 = self.glTransform(v0, modelMatrix)
            v0 = [v0.x, v0.y, v0.z]
            v1 = self.glTransform(v1, modelMatrix)
            v1 = [v1.x, v1.y, v1.z]
            v2 = self.glTransform(v2, modelMatrix)
            v2 = [v2.x, v2.y, v2.z]

            if material.texture:
                self.scene.append(Triangle(A=v0, B=v1, C=v2, material=material, vts = (vt0, vt1, vt2)))
            else:
                self.scene.append(Triangle(A=v0, B=v1, C=v2, material=material))


            if vertCount == 4:
                v3 = model.vertices[ face[3][0] - 1]
                v3 = self.glTransform(v3, modelMatrix)
                v3 = [v3.x, v3.y, v3.z]
                vt3 = model.texcoords[face[3][1] - 1]

                if material.texture:
                    self.scene.append(Triangle(A=v0, B=v2, C=v3, material=material, vts = (vt0, vt2, vt3)))
                else:
                    self.scene.append(Triangle(A=v0, B=v2, C=v3, material=material))

                




    def glRender(self):
        # Proyeccion
        t = tan((self.fov * pi / 180) / 2) * self.nearPlane
        r = t * self.vpWidth / self.vpHeight

        for y in range(self.vpY, self.vpY + self.vpHeight + 1, STEPS):
            for x in range(self.vpX, self.vpX + self.vpWidth + 1, STEPS):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC (-1 a 1)
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                Px *= r
                Py *= t

                direction = V3(Px, Py, -self.nearPlane)
                direction = normV(direction)

                rayColor = self.cast_ray(self.camPosition, direction)

                if rayColor is not None:
                    rayColor = color(rayColor[0],rayColor[1],rayColor[2])
                    self.glPoint(x, y, rayColor)

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            #InfoHeader
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

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])






