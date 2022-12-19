import glfw
from OpenGL.GL import *
import numpy as np
from math import sin, cos


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(800, 600, "Lab 1 | Aayush Pokharel", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# make the context current
glfw.make_context_current(window)


# fmt: off
vertices = [
    -0.55, 0.55, 0.0,
    -0.55,-0.55, 0.0,
    0.55,-0.55, 0.0,
    0.05, -0.05, 0.0,
    0.55, -0.05, 0.0,
]

colors = [
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    1.0, 0.0, 1.0
    ]
# fmt: off

vertices = np.array(vertices, dtype=np.float32)
colors = np.array(colors, dtype=np.float32)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3, GL_FLOAT, 0, vertices)

glEnableClientState(GL_COLOR_ARRAY)
glColorPointer(3, GL_FLOAT, 0, colors)

glClearColor(0, 0.1, 0.1, 1)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    ct = glfw.get_time()  # returns the elapsed time, since init was called
    """
    glLoadIdentity()
    glScale(abs(sin(ct)), abs(sin(ct)), 1)
    glRotatef(sin(ct) * 45, 0, 0, 1)
    glTranslatef(sin(ct), cos(ct), 0)
    """
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 5)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
