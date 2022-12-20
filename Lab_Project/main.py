import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
from GameState import *

# This is the main class of the application.
class App:
    def __init__(self):

        # initialize python window from pygame
        pg.init()
        # set the text of in the title bar of the applicatin
        pg.display.set_caption("Tick Tack Toe | Lab Mini-Project")
        # this sets the initalized pygame window to use OpenGL in a double buffer system instead of it's own abstracted SDL2 Library.
        self.scrn = pg.display.set_mode((800, 800), pg.OPENGL | pg.DOUBLEBUF)
        # this gets and instances a clock for the application which will be used in calulating fps, and rendering
        self.clock = pg.time.Clock()
        # initialize Game State and bind an instance to the main application class.
        self.gs = GameState()
        # This makes OpenGl to render a background having specific color
        glClearColor(0.1, 0.2, 0.2, 1)
        # the shader instance of the class is assigned via a custom function that compiles
        # and returns the necessary shaders from the shader files.
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        # making sure that our application uses the compiled shader(aka Program)
        glUseProgram(self.shader)
        # instantiate a class of Background Line that contain all the vertex information
        self.BackgroundLines = BackgroundLines()
        # command to run the infite Game Loop of the Application
        self.mainLoop()

    # custom function that takes file path for GLSL source files for vertex and fragment shader.
    # It does file handling and read their content to a variable as a string.
    # It takes the strings and compiles the shader(program).
    def createShader(self, vertexFilePath, fragmentFilePath):
         # using with open automatically closed the file once it's out of scope.
        with open(vertexFilePath, "r") as f: # opening file for read
            vertex_src = f.readlines() # reading the content of the Vertex shader's source file

        with open(fragmentFilePath, "r") as f: # opening file for read
            fragment_src = f.readlines()  # reading the content of the Vertex shader's source file

        # compiling all the shaders and making a Program
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER), # compiling individual shaders
            compileShader(fragment_src, GL_FRAGMENT_SHADER), # compiling individual shaders
        )

        return shader

    # This is the function having the infinity loop that handles all the application.
    # It has certain conditons under which the loop can be terminated and the termination of the loop results in
    # closing of the application.
    def mainLoop(self):
        running = True # This is the variable which is used to keep the loop running
        # this is instantiated as an empty list and we append vertices to this list to later dynamically bind the 
        # buffer on user input.
        newLine = [] 
        printingWinner = False # this is used to make sure that the printing of Winner is only done once during the infinite loop.
        # all the events and logic runs under this loop. This is the main loop.
        while running:
            # check all events that are occuring
            for event in pg.event.get():
                # creating a quit conditon to close the application
                if event.type == pg.QUIT: # pg.QUIT can be accessed when clicking the quit button.
                    running = False # sets the running to false and breaks the infinite loop.

                # this checks for mouse input. Especially the clicking of left mouse button.
                if event.type == pg.MOUSEBUTTONDOWN:
                    # getting the positon of the mouse cursor in pixel of the PyGame window.
                    # top left is 0,0 and bottom right is the width and height of the PyGame window.
                    # for this application it's 800px by 800 px
                    mouseX, mouseY = pg.mouse.get_pos()
                    print("\nMouse Position Pixel :", mouseX, mouseY, "\n")
                    # print(self.gs.checkLoc(int(mouseX),int(mouseY)))

                    # this is a custom function that takes the pixel position of the mouse cursor in the
                    # PyGame window and returns the refrence to the box in the Game Board.
                    # for example: It returns 0 the refrence for top left box if the mouse cursor is within it's bounding area.
                    tileLocation = self.gs.checkLoc(int(mouseX), int(mouseY))
                    print("value to be added in tile:", tileLocation)
                    # function that was used in devlopment to log the state of the board before user's input in a turn.
                    self.gs.printBoardCondition("before")
                    prevVal = self.gs.ValMap[tileLocation] # temporarily storing the board's state before player's input
                    self.gs.putValue(tileLocation)  # the function that handles the player's turn
                    curVal = self.gs.ValMap[tileLocation] # temporarily storing the board's state after player's input
                     # function that was used in devlopment to log the state of the board after user's input in a turn.
                    self.gs.printBoardCondition("after")
                    # condition that checks if there was any changes to the board after player's input
                    if prevVal != curVal:
                        # custom function that takes the refrence loctaion and the current players turn to calculate the
                        # vertices that need to be passed to the newLine list to add the vertics to the Buffer.
                        toPrint = self.BackgroundLines.getNewLine(tileLocation,self.gs.currentPlayer)
                        newLine.extend(toPrint) # appending the new vertices to the newLine list
                        self.BackgroundLines.addNew(newLine) # passing the updated newLine list to the OpenGl pipline to render
                        glBindVertexArray(self.BackgroundLines.vao) # refrencing and rebinding the VertexArray with new Values
                        #print("changed Background vertex count is:",self.BackgroundLines.vertex_count)
                        glDrawArrays(GL_LINES, 0, self.BackgroundLines.vertex_count) # Drawing the required lines as per the updated buffer.


            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            # using the compiled shader
            glUseProgram(self.shader)
            # binding the Vertex array according to the initial vertices
            glBindVertexArray(self.BackgroundLines.vao)
            if self.gs.won != True: # condition to render as long as the game is not won
                glDrawArrays(GL_LINES, 0, self.BackgroundLines.vertex_count) # drawing the requred lines as per the vertices.
            if self.gs.won == True:
                if printingWinner == False: # This if conditon makes sure that the winner is only printed once during the infinite loop.
                    print("\nThe winner is: ",self.gs.winningPlayer)
                    printingWinner = True
                # changing the color of the screen to white to denote a game being won.
                glClearColor(1, 1, 1, 1)
                

             # This function flips the buffers and changes the screen.
             # It exchanges the buffer on screen with the one in GPU's memory.
            pg.display.flip()

            # timing signal. It helps in maintaining a 60 FPS.
            self.clock.tick(60)

        # function to call destructor
        self.quit()

    # this the destructor the deletes and clear all the memory used during execution of program
    def quit(self):

        # Destroying the instance of Background Lines
        self.BackgroundLines.destroy()
        # Destroying the compiled shders
        glDeleteProgram(self.shader)
        # calling the quit function to close the PyGame Application.
        pg.quit()

# This is the class that handles all the rendering and vertices for the application
class BackgroundLines:
    # constructor
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
        # The logic of this program depends up manipluation of this list. It initially contains the vertices to draw
        # the 4 straight lines that will make up the board.
        # Later on, as per use input vertices will be appended to it to help in dynamically changing the Buffer.
        # fmt: on
        # OpenGL is written in C language and it can't support the python List therefore we use the numpy library
        # to create a array of 32bit float form the list so the wrapper function can properly pass the vertices to the
        # API calls written in C language.
        self.vertices = np.array(self.raw_vertices, dtype=np.float32)

        # this gives the number of vertices. A vertex is made up of 6 elements (x,y,z,r,g,b) so we divide the length of 
        # the vertices with 6 to get the vertex count.
        self.vertex_count = int(len(self.vertices)/6)
        # We generate the VAO for location 1 in memory.
        # The exact logic of this command is still unknown but it somehow binds the VOA and is necessary.
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao) # This binds the Vertices from the Vertex Array Object (VAO)
        self.vbo = glGenBuffers(1) # The VBO is refrenced from VAO
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) # The Buffer which is sent to the GPU is binded with th VBO
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW
        ) # This functions gives information on the buffer, It takes the Buffer Type, the size of the buffer, the vertices and
          # the type of rendering it requires.

        glEnableVertexAttribArray(0) # This defines the data for location 0 in our GLSL shader which is for location coordinates.
        
        # This function defines how the content in the buffer is actually made.
        # It has location 0, takes 3 elements, is a float, the vertices are not normalized and the one vertex is 6*4 bis = 24 bits long.
        # and the pointer for this array starts at position 0 i,e at the front,
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)  # This defines the data for location 1 in our GLSL shader which is for texture coordinates.
        
        # This function defines how the content in the buffer is actually made.
        # It las location 1, takes 3 elements, is a float, the vertices are not normalized and the one vertex is 6*4 bis = 24 bits long.
        # and the pointer for this array starts at position 12 i,e at the start of the RBG value in the array
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # This is the function that takes the box location refrence from the board as well as the current player and return a list of vertices to
    # render X or 0 as per user input.
    def getNewLine(self,val,cPlayer):
        toAdd = []
        # this is for X
        if cPlayer == "playerO": # After putting value current player chagnes so taking alternate
            if val == 0:
                #fmt: off
                toAdd = [
                    # X Top Left
                    -0.9,0.9,0,1,1,1,
                    -0.4,0.4,0,1,1,1,
                    -0.9,0.4,0,1,1,1,
                    -0.4,0.9,0,1,1,1,
                ]
                #fmt: on
            if val == 1:
                #fmt: off
                toAdd = [
                    # X Top Middle
                    -0.2,0.9,0,1,1,1,
                    0.2,0.4,0,1,1,1,
                    0.2,0.9,0,1,1,1,
                    -0.2,0.4,0,1,1,1,
                ]
                #fmt: off
            if val == 2:
                #fmt: off
                toAdd = [
                    # X Top Right
                    0.9,0.9,0,1,1,1,
                    0.4,0.4,0,1,1,1,
                    0.9,0.4,0,1,1,1,
                    0.4,0.9,0,1,1,1,
                ]
                #fmt: off
            if val == 3:
                #fmt: off
                toAdd = [
                    # X Middle Left
                    -0.9,0.3,0,1,1,1,
                    -0.4,-0.3,0,1,1,1,
                    -0.4,0.3,0,1,1,1,
                    -0.9,-0.3,0,1,1,1,
                ]
                #fmt: off
            if val == 4:
                #fmt: off
                toAdd = [
                    # X Middle Middle
                    -0.2,0.3,0,1,1,1,
                    0.2,-0.3,0,1,1,1,
                    0.2,0.3,0,1,1,1,
                    -0.2,-0.3,0,1,1,1,
                ]
                #fmt: off
            if val == 5:
                #fmt: off
                toAdd = [
                    # X Middle Right
                    0.9,0.3,0,1,1,1,
                    0.4,-0.3,0,1,1,1,
                    0.9,-0.3,0,1,1,1,
                    0.4,0.3,0,1,1,1,
                ]
                #fmt: off
            if val == 6:
                #fmt: off
                toAdd = [
                    # X Bottom Left
                    -0.9,-0.9,0,1,1,1,
                    -0.4,-0.4,0,1,1,1,
                    -0.4,-0.9,0,1,1,1,
                    -0.9,-0.4,0,1,1,1,
                ]
                #fmt: off
            if val == 7:
                #fmt: off
                toAdd = [
                    # X Bottom Middle
                    -0.2,-0.9,0,1,1,1,
                    0.2,-0.4,0,1,1,1,
                    0.2,-0.9,0,1,1,1,
                    -0.2,-0.4,0,1,1,1,
                ]
                #fmt: off
            if val == 8:
                #fmt: off
                toAdd = [
                    # X Bottom Right
                    0.9,-0.9,0,1,1,1,
                    0.4,-0.4,0,1,1,1,
                    0.9,-0.4,0,1,1,1,
                    0.4,-0.9,0,1,1,1,
                ]
                #fmt: off
        # This is for O
        if cPlayer == "playerX": # After putting value current player chagnes so taking alternate
            if val == 0:
                #fmt: off
                toAdd = [
                    # O Top Left
                    -0.5,0.9,0,1,1,1,
                    -0.9,0.7,0,1,1,1,
                    -0.9,0.7,0,1,1,1,
                    -0.5,0.4,0,1,1,1,
                    -0.5,0.4,0,1,1,1,
                    -0.4,0.7,0,1,1,1,
                    -0.4,0.7,0,1,1,1,
                    -0.5,0.9,0,1,1,1,
                ]
                #fmt: on
            if val == 1:
                #fmt: off
                toAdd = [
                    # O Top Middle
                    0.0,0.9,0,1,1,1,
                    -0.2,0.7,0,1,1,1,
                    -0.2,0.7,0,1,1,1,
                    0.0,0.4,0,1,1,1,
                    0.0,0.4,0,1,1,1,
                    0.2,0.7,0,1,1,1,
                    0.2,0.7,0,1,1,1,
                    0.0,0.9,0,1,1,1,
                ]
                #fmt: off
            if val == 2:
                #fmt: off
                # O Top Right
                toAdd = [
                    0.5,0.9,0,1,1,1,
                    0.9,0.7,0,1,1,1,
                    0.9,0.7,0,1,1,1,
                    0.5,0.4,0,1,1,1,
                    0.5,0.4,0,1,1,1,
                    0.4,0.7,0,1,1,1,
                    0.4,0.7,0,1,1,1,
                    0.5,0.9,0,1,1,1,
                ]
                #fmt: off
            if val == 3:
                #fmt: off
                toAdd = [
                    # O Middle Left
                    -0.5,0.3,0,1,1,1,
                    -0.9,0.0,0,1,1,1,
                    -0.9,0.0,0,1,1,1,
                    -0.5,-0.3,0,1,1,1,
                    -0.5,-0.3,0,1,1,1,
                    -0.4,0.0,0,1,1,1,
                    -0.4,0.0,0,1,1,1,
                    -0.5,0.3,0,1,1,1,
                ]
                #fmt: off
            if val == 4:
                #fmt: off
                toAdd = [
                    # O Middle Middle
                    0.0,0.3,0,1,1,1,
                    -0.2,0.0,0,1,1,1,
                    -0.2,0.0,0,1,1,1,
                    0.0,-0.3,0,1,1,1,
                    0.0,-0.3,0,1,1,1,
                    0.2,0.0,0,1,1,1,
                    0.2,0.0,0,1,1,1,
                    0.0,0.3,0,1,1,1,
                ]
                #fmt: off
            if val == 5:
                #fmt: off
                toAdd = [
                    # O Middle Right
                    0.5,0.3,0,1,1,1,
                    0.9,0.0,0,1,1,1,
                    0.9,0.0,0,1,1,1,
                    0.5,-0.3,0,1,1,1,
                    0.5,-0.3,0,1,1,1,
                    0.4,0.0,0,1,1,1,
                    0.4,0.0,0,1,1,1,
                    0.5,0.3,0,1,1,1,
                ]
                #fmt: off
            if val == 6:
                #fmt: off
                toAdd = [
                    # O Bottom Left
                    -0.5,-0.4,0,1,1,1,
                    -0.9,-0.7,0,1,1,1,
                    -0.9,-0.7,0,1,1,1,
                    -0.5,-0.9,0,1,1,1,
                    -0.5,-0.9,0,1,1,1,
                    -0.4,-0.7,0,1,1,1,
                    -0.4,-0.7,0,1,1,1,
                    -0.5,-0.4,0,1,1,1,
                ]
                #fmt: off
            if val == 7:
                #fmt: off
                toAdd = [
                    # O Bottom Middle
                    0.0,-0.4,0,1,1,1,
                    -0.2,-0.7,0,1,1,1,
                    -0.2,-0.7,0,1,1,1,
                    0.0,-0.9,0,1,1,1,
                    0.0,-0.9,0,1,1,1,
                    0.2,-0.7,0,1,1,1,
                    0.2,-0.7,0,1,1,1,
                    0.0,-0.4,0,1,1,1,
                ]
                #fmt: off
            if val == 8:
                #fmt: off
                toAdd = [
                    # O Bottom Right
                    0.5,-0.4,0,1,1,1,
                    0.9,-0.7,0,1,1,1,
                    0.9,-0.7,0,1,1,1,
                    0.5,-0.9,0,1,1,1,
                    0.5,-0.9,0,1,1,1,
                    0.4,-0.7,0,1,1,1,
                    0.4,-0.7,0,1,1,1,
                    0.5,-0.4,0,1,1,1,
                ]
                #fmt: off
        return toAdd


    
    def addNew(self,lis):
        #print("to be added",lis)
        lis = np.array(lis,dtype=np.float32)
        #print("old vertices", self.vertices)
        self.vertices = np.append(self.vertices,lis)
        #print("new vertices", self.vertices)
        self.vertex_count = int(len(self.vertices)/6)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW
        )
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))



if __name__ == "__main__":
    myApp = App()
