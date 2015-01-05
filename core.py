# -*- coding: utf-8 -*-

__author__ = 'nyash myash'


from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image
import sys
import random

# Rotation angle for tori and core
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
x=y=z=0.0
vib = 0.028



def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v/norm



def drawTriangle(*args):
    glEnable(GL_TEXTURE_2D)
    glBindTexture (GL_TEXTURE_2D, texture)

    texcoords = [(0.0,0.0),(1.0,0.0),(0.0,1.1)]
    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[1,1,1,1])
    glBegin(GL_TRIANGLES)
    j=0
    for i in args:
        glNormal3f(*i)
        glTexCoord2f(*texcoords[j])
        glVertex3f(*i)
        j+=1
    glEnd()

def subdivide(v1, v2, v3):

    v1 = np.array(v1)
    v2 = np.array(v2)
    v3 = np.array(v3)

    v12 = np.zeros(3)
    v23 = np.zeros(3)
    v31 = np.zeros(3)

    for i in xrange(3):
        v12[i] = v1[i]+v2[i]
        v23[i] = v2[i]+v3[i]
        v31[i] = v3[i]+v1[i]

    v12 = normalize(v12)
    v23 = normalize(v23)
    v31 = normalize(v31)
    drawTriangle(v1, v12, v31)
    drawTriangle(v2, v23, v12)
    drawTriangle(v3, v31, v23)
    drawTriangle(v12, v23, v31)


def drawCore ():

    X = 0.4657834624921632
    Z = 0.884898732098092389

    vdata = [
       [-X, 0.0, Z], [X, 0.0, Z], [-X, 0.0, -Z], [X, 0.0, -Z],
       [0.0, Z, X], [0.0, Z, -X], [0.0, -Z, X], [0.0, -Z, -X],
       [Z, X, 0.0], [-Z, X, 0.0], [Z, -X, 0.0], [-Z, -X, 0.0]]


    tindices= [
       [0,4,1], [0,9,4], [9,5,4], [4,5,8], [4,8,1],
       [8,10,1], [8,3,10], [5,3,8], [5,2,3], [2,7,3],
       [7,10,3], [7,6,10], [7,11,6], [11,0,6], [0,1,6],
       [6,1,10], [9,0,11], [9,11,2], [9,2,5], [7,2,11] ]


    for i in xrange(20):
        subdivide(vdata[tindices[i][0]],
                  vdata[tindices[i][1]],
                  vdata[tindices[i][2]])


def drawTorus_0():
    glDisable(GL_TEXTURE_2D)
    glRotatef(225, 1, 1, 0)
    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[0.31,0.3,0.18,0.9])
    glutSolidTorus(0.02,1.9,10,100)


def drawTorus_1():
    glDisable(GL_TEXTURE_2D)
    glRotatef(45, 1, 1, 0)
    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[0.31,0.3,0.18,0.9])
    glutSolidTorus(0.02,1.4,10,100)

def drawTorus_2():
    glDisable(GL_TEXTURE_2D)

    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[0.32,0.29,0.18,0.8])
    glutSolidTorus(.08, 2.7, 10, 100)


def drawTorus_3():
    glDisable(GL_TEXTURE_2D)
    glRotatef(90, 0, 1, 0)

    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[0.32,0.29,0.18,0.8])
    glutSolidTorus(.08, 2.7, 10, 100)

def drawTorus_4():
    glDisable(GL_TEXTURE_2D)
    glRotatef(45, 0, 1, 0)

    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[0.32,0.29,0.18,0.8])
    glutSolidTorus(.08, 2.7, 10, 100)

def drawTorus_5():
    glDisable(GL_TEXTURE_2D)
    glRotatef(270, 0, 1, 0)

    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,[0.32,0.29,0.18,0.8])
    glutSolidTorus(.08, 2.7, 10, 100)

def display():
    global x, y, z, vib

    #clear the screen and the depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reset The View
    glLoadIdentity()

    # Move Right And Into The Screen
    glTranslatef(0.0,0.0,-7.0)
    glPushMatrix()
    glPushMatrix()
    glPushMatrix()
    glPushMatrix()

    glPopMatrix()
    glRotatef(-X_AXIS,1,1,0.0)
    drawTorus_0()

    glPopMatrix()
    glRotatef(X_AXIS,1,1,0.0)
    drawTorus_1()

    glPopMatrix()
    glRotatef(Y_AXIS,0.0,1.0,0.0)
    drawTorus_2()

    drawTorus_3()
    drawTorus_4()
    drawTorus_5()

    glPopMatrix()
    glRotatef(Z_AXIS,1.0,1.0,1.0)
    # glTranslatef(-x + random.uniform(-vib,vib), -y + random.uniform(-vib,vib), -z + random.uniform(-vib,vib))
    drawCore()
    # glTranslatef(x, y, z)
    glutSwapBuffers()



def getTexture (file):
    image  = Image.open (file)
    width  = image.size [0]
    height = image.size [1]
    image  = image.tostring ( "raw", "RGBX", 0, -1 )
    texture = glGenTextures (1)
    glBindTexture     ( GL_TEXTURE_2D, texture )   # 2d texture (x and y size)
    glPixelStorei     ( GL_UNPACK_ALIGNMENT,1 )
    glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameteri   ( GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR )
    glTexParameteri   ( GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR )
    gluBuild2DMipmaps ( GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image )

    return texture


def reshape (width, height):
    glViewport     ( 0, 0, width, height )
    glMatrixMode   ( GL_PROJECTION )
    glLoadIdentity ()
    gluPerspective ( 60.0, float(width)/float (height), 1.0, 60.0 )
    glMatrixMode   ( GL_MODELVIEW )
    glLoadIdentity ()
    # gluLookAt      ( 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0 )


def motion():
    global X_AXIS,Y_AXIS,Z_AXIS

    X_AXIS  = 0.02 * glutGet ( GLUT_ELAPSED_TIME )
    Y_AXIS = 0.03 * glutGet ( GLUT_ELAPSED_TIME )
    Z_AXIS  = 0.01 * glutGet ( GLUT_ELAPSED_TIME )

    glutPostRedisplay ()


def keyPressed ( *args ):
    if args [0] == '\033':
        sys.exit ()

def init ():
    glClearColor ( 0.0, 0.0, 0.0, 0.0 )
    glClearDepth ( 1.0 )
    glDepthFunc  ( GL_LEQUAL )
    glEnable     ( GL_DEPTH_TEST )
    glEnable     ( GL_TEXTURE_2D )
    glHint       ( GL_POLYGON_SMOOTH_HINT,         GL_NICEST )
    glHint       ( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [20.0]
    light_position = [1.0, 1.0, 1.0, 1.0]
    glShadeModel (GL_SMOOTH)

    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def main ():

    global texture

    glutInit (sys.argv)
    glutInitDisplayMode (GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (0, 0)

    glutCreateWindow ("Moving core")
    glutDisplayFunc  (display)
    glutIdleFunc     (motion)

    glutReshapeFunc  (reshape)
    glutKeyboardFunc (keyPressed)
    init ()

    texture = getTexture ( "metal.jpg" )

    glutMainLoop()

print "Press ESC to quit."

if __name__ == '__main__':
    main()