import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from GameState import *


class App:
    def __init__(self):

        # initialize python window
        pg.init()
        pg.display.set_caption("Tick Tack Toe | Lab Mini-Project")
        self.scrn = pg.display.set_mode((800, 800), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        # initialize Game State
        self.gs = GameState()
        # initialize opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        self.BackgroundLines = BackgroundLines()
        self.imgX = pg.image.load("Texture/X.png").convert()
        self.imgO = pg.image.load("Texture/O.png").convert()
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

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pg.mouse.get_pos()
                    print("\nMouse Position Pixel :", mouseX, mouseY, "\n")
                    # print(self.gs.checkLoc(int(mouseX),int(mouseY)))
                    tileLocation = self.gs.checkLoc(int(mouseX), int(mouseY))
                    print("value to be added in tile:", tileLocation)
                    # print("before:\n",self.gs.ValMap,"\n\n")
                    self.gs.printBoardCondition("before")
                    prevVal = self.gs.ValMap[tileLocation]
                    self.gs.putValue(tileLocation)
                    curVal = self.gs.ValMap[tileLocation]
                    # print("after:\n",self.gs.ValMap,"\n\n")
                    self.gs.printBoardCondition("after")
                    if prevVal != curVal:
                        print("change")
                        newLine = [-0.5,0.5,0,1,1,1]
                        self.BackgroundLines.addNew(newLine)
                        print(self.BackgroundLines.vertices)
                        glUseProgram(self.shader)
                        glBindVertexArray(self.BackgroundLines.vao)
                        glDrawArrays(GL_LINES, 0, self.BackgroundLines.vertex_count)


            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.BackgroundLines.vao)
            if self.gs.won != True:
                glDrawArrays(GL_LINES, 0, self.BackgroundLines.vertex_count)
            if self.gs.won == True:
                glClearColor(1, 1, 1, 1)
                #self.BackgroundLines.vertices.append()

            pg.display.flip()

            # timiing
            self.clock.tick(60)

        self.quit()

    def quit(self):

        # self.flag.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class BackgroundLines:
    def __init__(self):
        # fmt: off
        # x, y,z,r,g,b
        self.raw_vertices = [
            -(1/3),1.0,0,1,1,1, 
            -(1/3),-1.0,0,1,1,1,
            (1/3),1.0,0,1,1,1,
            (1/3),-1.0,0,1,1,1,
            -1.0, (1/3),0,1,1,1,
            1.0, (1/3),0,1,1,1,
            -1.0, -(1/3),0,1,1,1,
            1.0, -(1/3),0,1,1,1,
        ]
        # fmt: on
        self.vertices = np.array(self.raw_vertices, dtype=np.float32)

        #print("lenth of",len(self.vertices))
        self.vertex_count = int(len(self.vertices)/6)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW
        )
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def addNew(self,lis):
        print("to be added",lis)
        lis = np.array(lis,dtype=np.float32)
        self.vertices = np.append(self.vertices,lis)
        self.vertex_count = int(len(self.vertices)/6)
        #self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW
        )
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))



"""
class Material:
    def __init__(self, filepath):

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            image_width,
            image_height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data,
        )
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))

"""

if __name__ == "__main__":
    myApp = App()
