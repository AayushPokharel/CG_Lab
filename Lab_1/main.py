import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader


class App:
    def __init__(self):

        # initialize python window
        pg.init()
        # getting system's resolution
        width, height = pg.display.Info().current_w, pg.display.Info().current_h
        # printing the resolution to console
        print("Display Width : ", width, "\nDisplay Height : ", height)
        pg.display.set_caption("Lab 1 | Aayush Pokharel")
        pg.display.set_mode((800, 800), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        # initialize opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        self.flag = Flag()
        self.mainLoop()

    def createShader(self, vertexFilePath, fragmentFilePath):

        with open(vertexFilePath, "r") as f:
            vertex_src = f.readlines()

        with open(fragmentFilePath, "r") as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER),
        )

        return shader

    def mainLoop(self):
        running = True
        while running:
            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.flag.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.flag.vertex_count)

            pg.display.flip()

            # timiing
            self.clock.tick(60)

        self.quit()

    def quit(self):

        self.flag.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Flag:
    def __init__(self):

        # fmt: off
        # x,y,z,r,g,b
        self.vertices = (
            # Triangle1-Outer
            -1.0,  -1.0,  0.5,	0.0, 0.21, 0.58,		#bottom left
		    0.68, -1.0,  0.5,	0.0, 0.21, 0.58,		#bottom right
		    -1.0,   0.7,  0.5,	0.0, 0.21, 0.58,		#mid-top left
								
		    -1.0,   0.0,   0.5,	0.0, 0.21, 0.58,		#mid left
		    0.72,  0.0,  0.5,	0.0, 0.21, 0.58,		#mid right 
		    -1.0,   1.0,  0.5,	0.0, 0.21, 0.58,		#top left

		    # Triangle2-Inner	
		    -0.95,	-0.95,	0.5,	0.87, 0.04, 0.2,		#bottom left
		    0.55, -0.95,	0.5,	0.87, 0.04, 0.2,		#bottom right
		    -0.95,	 0.6,	0.5,	0.87, 0.04, 0.2,		#mid top left
							
		    -0.95,	 0.05,  0.5,	0.87, 0.04, 0.2,		#mid left
		    0.52,  0.05,  0.5,	0.87, 0.04, 0.2,		#mid right 
		    -0.95,  0.9,  0.5,	0.87, 0.04, 0.2,		#top left
        )
        # fmt: on

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 12

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW
        )
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    myApp = App()
