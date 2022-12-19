import ctypes
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

# Define Shaders
vertexShader = """
attribute vec2 position;
void main()
{
  gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragmentShader = """
void main()
{
  gl_FragColor = vec4(0.0,1.0,0.0,1.0);
}
"""


def normalize(xList, yList, resolution):
    xList = [x / resolution for x in xList]
    yList = [y / resolution for y in yList]

    coordinateList = np.zeros((len(xList), 2))
    i = 0
    for _ in xList:
        coordinateList[i] = [xList[i], yList[i]]
        i += 1
    return coordinateList


def midpoint_circle(x_center, y_center, r, res):
    x = r
    y = 0
    # Printing the initial point the
    # axes after translation
    x_coordinates = np.array([])
    y_coordinates = np.array([])

    x_coordinates = np.append(x_coordinates, x + x_center)
    y_coordinates = np.append(y_coordinates, y + y_center)
    # When radius is zero only a single
    # point be printed
    if r > 0:
        x_coordinates = np.append(x_coordinates, x + x_center)
        x_coordinates = np.append(x_coordinates, y + x_center)
        x_coordinates = np.append(x_coordinates, -y + x_center)
        y_coordinates = np.append(y_coordinates, -y + y_center)
        y_coordinates = np.append(y_coordinates, x + y_center)
        y_coordinates = np.append(y_coordinates, x + y_center)

    P = 1 - r

    while x > y:

        y += 1

        if P <= 0:
            P = P + 2 * y + 1

        else:
            x -= 1
            P = P + 2 * y - 2 * x + 1

        if x < y:
            break

        x_coordinates = np.append(x_coordinates, x + x_center)
        x_coordinates = np.append(x_coordinates, -x + x_center)
        x_coordinates = np.append(x_coordinates, x + x_center)
        x_coordinates = np.append(x_coordinates, -x + x_center)
        y_coordinates = np.append(y_coordinates, y + y_center)
        y_coordinates = np.append(y_coordinates, y + y_center)
        y_coordinates = np.append(y_coordinates, -y + y_center)
        y_coordinates = np.append(y_coordinates, -y + y_center)

        if x != y:
            x_coordinates = np.append(
                x_coordinates,
                y + x_center,
            )
            x_coordinates = np.append(x_coordinates, -y + x_center)
            x_coordinates = np.append(x_coordinates, y + x_center)
            x_coordinates = np.append(x_coordinates, -y + x_center)
            y_coordinates = np.append(y_coordinates, x + y_center)
            y_coordinates = np.append(y_coordinates, x + y_center)
            y_coordinates = np.append(y_coordinates, -x + y_center)
            y_coordinates = np.append(y_coordinates, -x + y_center)

    return normalize(x_coordinates, y_coordinates, res)


tempData = midpoint_circle(0, 0, 500, 1000)
data = np.zeros(int(len(tempData)), [("position", np.float32, 2)])
data["position"] = tempData


def compileShader(source, type):
    shader = glCreateShader(type)
    glShaderSource(shader, source)

    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(error)
        raise RuntimeError(f"{source} shader compilation error")
    return shader


def createProgram(vertex, fragment):
    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError("Error Linking program")

    glDetachShader(program, vertex)
    glDetachShader(program, fragment)

    return program


def init():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glLoadIdentity()

    program = createProgram(
        compileShader(vertexShader, GL_VERTEX_SHADER),
        compileShader(fragmentShader, GL_FRAGMENT_SHADER),
    )

    glUseProgram(program)

    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    stride = data.strides[0]
    offset = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)


def draw():
    glDrawArrays(GL_POINTS, 0, len(data))
    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)


def keyboard(key, x, y):
    if key == b"\x1b":
        sys.exit()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  # type: ignore #ignore
glutCreateWindow("Midpoint Circle - Lab 3 | Aayush Pokharel")
glutReshapeWindow(800, 800)
glutReshapeFunc(reshape)
init()
glutDisplayFunc(draw)
glutPostRedisplay()
glutKeyboardFunc(keyboard)
glutMainLoop()
