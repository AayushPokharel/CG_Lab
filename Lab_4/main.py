import ctypes
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame as pg
from pygame.locals import *

# Define Shaders
vertexShader = """
attribute vec2 position;
uniform mat4 transform;
void main()
{
  gl_Position = transform*vec4(position, 0.0, 1.0);
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


data = np.zeros(3, [("position", np.float32, 2)])
data["position"] = (-0.5, +0.5), (+0.5, +0.5), (-0.5, -0.5)


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


def getTransformationMatrix(Transformation):
    # fmt:off
    if Transformation == "xReflection":
        transformation_mat = np.array(
            [
            -1.0, 0.0,0.0,0.0,
            0.0,1.0,0.0,0.0,
            0.0,0.0,0.0,0.0,
            0.0,0.0,0.0,1.0,
            ],
            np.float32,
        )
    if Transformation == "yReflection":
        transformation_mat = np.array(
            [
             1.0,0.0,0.0,0.0,
            0.0,-1.0,0.0,0.0,
            0.0,0.0,0.0,0.0,
            0.0,0.0,0.0,1.0,   
            ],
            np.float32,
        )
    if Transformation == "Rotation":
        transformation_mat = np.array(
            [
            np.cos((np.pi / 180) * 60),
            np.sin((np.pi / 180) * 60),
            0.0,
            0.0,
            np.sin(-(np.pi / 180) * 60),
            np.cos((np.pi / 180) * 60),
            0.0,
            0.0,
            0.0,0.0,1.0,0.0,
            0.0,0.0,0.0,1.0,
        ],
        np.float32,
        )
    if Transformation == "Scaling":
        transformation_mat = np.array(
            [
             3.0,0.0,0.0,0.0,
            0.0,3.0,0.0,0.0,
            0.0,0.0,0.0,0.0,
            0.0,0.0,0.0,1.0,
        ],
        np.float32,
        )
    if Transformation == "Scaling":
        transformation_mat = np.array(
            [
             3.0,0.0,0.0,0.0,
            0.0,3.0,0.0,0.0,
            0.0,0.0,0.0,0.0,
            0.0,0.0,0.0,1.0,
        ],
        np.float32,
        )
    if Transformation == "Translation":
        transformation_mat = np.array(
            [
            1.0, 0.0, 0.0, 0.5,
            0.0, 1.0, 0.0, 0.5,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ],
        np.float32,
        )
    if Transformation == "xShear":
        transformation_mat = np.array(
            [
            1.0,2.0,0.0,0.0,
            0.0,1.0,0.0,0.0,
            0.0,0.0,0.0,0.0,
            0.0,0.0,0.0,1.0,
        ],
        np.float32,
        )
    if Transformation == "yShear":
        transformation_mat = np.array(
            [
            1.0,1.5,0.0,0.0,
            0.0,1.0,0.0,0.0,
            0.0,0.0,0.0,0.0,
            0.0,0.0,0.0,1.0,
        ],
        np.float32,
        )
    # fmt:on
    return transformation_mat


def main():
    print("\n\nWhat type of Transformation do you want?")
    print("Translation : (Translation)")
    print("Rotation : (Rotation)")
    print("Scaling : (Scaling)")
    print("Reflection on X : (xReflection)")
    print("Reflection on Y : (yReflection)")
    print("Shearing on X : (xShear)")
    print("Shearing on Y : (yShear)")
    inputMatrix = input("Type the string inside parenthesis to select \n")

    running = True
    while running:
        width, height = 800, 800
        pg.init()
        pg.display.set_mode((width, height), DOUBLEBUF | OPENGL | GL_RGBA)
        pg.display.set_caption(("{} - Lab 4 | Aayush Pokharel").format(inputMatrix))
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

        transformation_mat = getTransformationMatrix(inputMatrix)
        loc = glGetUniformLocation(program, "transform")
        glUniformMatrix4fv(loc, 1, GL_FALSE, transformation_mat)

        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
        glDrawArrays(GL_TRIANGLES, 0, len(data))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


if __name__ == "__main__":
    main()
