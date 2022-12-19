import ctypes
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame as pg
from pygame.locals import *

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
  gl_FragColor = vec4(1.0,0.0,0.0,1.0);
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


def midpoint_ellipse(rx, ry, xc, yc, res):
    x = 0
    y = ry

    x_coordinates = np.array([])
    y_coordinates = np.array([])

    # Initial decision parameter of region 1
    d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y
    # For region 1
    while dx < dy:
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)

        if d1 < 0:
            x += 1
            dx = dx + (2 * ry * ry)
            d1 = d1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)

    # Decision parameter of region 2
    d2 = (
        ((ry * ry) * ((x + 0.5) * (x + 0.5)))
        + ((rx * rx) * ((y - 1) * (y - 1)))
        - (rx * rx * ry * ry)
    )

    # Plotting points of region 2
    while y >= 0:
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)

        if d2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)

    return normalize(x_coordinates, y_coordinates, res)


tempData = midpoint_ellipse(800, 400, 0, 0, 1000)
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


def main():
    running = True
    while running:
        width, height = 800, 800
        pg.init()
        pg.display.set_mode((width, height), DOUBLEBUF | OPENGL | GL_RGBA)
        pg.display.set_caption("Midpoint Ellipse - Lab 3 | Aayush Pokharel")
        glViewport(0, 0, width, height)
        # here inti()
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)
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
        glDrawArrays(GL_POINTS, 0, len(data))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


if __name__ == "__main__":
    main()
