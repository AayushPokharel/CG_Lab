import ctypes
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame as pg
from pygame.locals import *
import glm as glm

# Define Shaders
vertexShader = """
attribute vec3 color;
attribute vec3 position;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 transform;
varying vec4 v_color;
void main()
{
  gl_Position = transform * vec4(position, 1.0);
  v_color = vec4(color, 1.0);
}
"""

fragmentShader = """
varying vec4 v_color;
void main()
{
  gl_FragColor = v_color;
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


data = np.zeros(3, [("position", np.float32, 2)])
data["position"] = (-0.5, +0.5), (+0.5, +0.5), (-0.5, -0.5)


# Build data

tempData = (
    (0.5, 0.5, -0.5),
    (0.5, 0.5, 0.5),
    (0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, 0.5, 0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (0.5, 0.5, -0.5),
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, 0.5, 0.5),
    (0.5, -0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, -0.5, -0.5),
    (-0.5, 0.5, 0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (0.5, -0.5, -0.5),
)

tempColor = (
    (0.714, 0.0, 0.0, 1.0),
    (0.714, 0.0, 0.0, 1.0),
    (0.783, 0.290, 0.734, 1.0),
    (0.714, 0.0, 0.0, 1.0),
    (0.997, 0.0, 0.064, 1.0),
    (0.945, 0.0, 0.592, 1.0),
    (0.543, 0.021, 0.542, 1.0),
    (0.673, 0.211, 0.457, 1.0),
    (0.722, 0.0, 0.174, 1.0),
    (0.302, 0.455, 0.848, 1.0),
    (0.225, 0.0, 0.040, 1.0),
    (0.517, 0.0, 0.338, 1.0),
    (0.997, 0.513, 0.064, 1.0),
    (0.945, 0.719, 0.592, 1.0),
    (0.543, 0.021, 0.542, 1.0),
    (0.997, 0.0, 0.064, 1.0),
    (0.583, 0.0, 0.014, 1.0),
    (0.609, 0.115, 0.436, 1.0),
    (0.327, 0.0, 0.844, 1.0),
    (0.014, 0.184, 0.576, 1.0),
    (0.559, 0.0, 0.639, 1.0),
    (0.559, 0.0, 0.639, 1.0),
    (0.195, 0.548, 0.859, 1.0),
    (0.559, 0.0, 0.639, 1.0),
)

vertex_data = np.zeros(
    int(len(tempData)), [("position", np.float32, 3), ("colors", np.float32, 4)]
)
vertex_data["position"] = tempData
vertex_data["colors"] = tempColor

indicesData = np.array(
    [
        0,
        1,
        2,
        1,
        2,
        3,
        4,
        5,
        6,
        5,
        6,
        7,
        8,
        9,
        10,
        9,
        10,
        11,
        12,
        13,
        14,
        13,
        14,
        15,
        16,
        17,
        18,
        17,
        18,
        19,
        20,
        21,
        22,
        21,
        22,
        23,
    ],
    dtype=np.int32,
)


def compileShader(source, type):
    shader = glCreateShader(type)
    glShaderSource(shader, source)

    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError("{source} shader compilation error")
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

###########################################

def main():
    running = True
    while running:
        width, height = 800, 800
        pg.init()
        pg.display.set_mode((width, height), DOUBLEBUF | OPENGL | GL_RGBA)
        pg.display.set_caption("Rotation - Lab 5 | Aayush Pokharel")
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

        transformY = np.matrix(
        f"""{np.cos((np.pi / 180) * 70)},
            0.0,
            {np.sin(-(np.pi / 180) * 70)},
            0.0;
            0.0,
            1.0,
            0.0,
            0.0;
            {np.sin((np.pi / 180) * 70)},
            0.0,
            {np.cos((np.pi / 180) * 70)},
            0.0;
            0.0,
            0.0,
            0.0,
            1.0"""
        )

        transformX = np.matrix(
            f""" 1.0,
                0.0,
                0.0,
                0.0;
                0.0,
                {np.cos((np.pi / 180) * -60)},
                {np.sin(-(np.pi / 180) * -60)},
                0.0;
                0.0,
                {np.sin((np.pi / 180) * -60)},
                {np.cos((np.pi / 180) * -60)},
                0.0;
                0.0,
                0.0,
                0.0,
                1.0"""
        )

        newTransform = np.matrix(
            f""" 1.0,
                0.0,
                0.0,
                0.0;
                0.0,
                {np.cos((np.pi / 180) * 60)},
                {np.sin((np.pi / 180) * 60)},
                0.0;
                0.0,
                {np.sin(-(np.pi / 180) * 60)},
                {np.cos((np.pi / 180) * 60)},
                0.0;
                0.0,
                0.0,
                0.0,
                1.0"""
        )
        transform = np.dot(newTransform, np.dot(transformX, transformY))
        loc = glGetUniformLocation(program, "transform")
        glUniformMatrix4fv(loc, 1, GL_FALSE, transform)

        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
        glDrawElements(GL_TRIANGLES, len(indicesData), GL_UNSIGNED_INT, None)
        glFlush()
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


if __name__ == "__main__":
    main()