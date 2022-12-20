# This is a class that is uncoupled from the rendering logic and purely handles the state of the Game and how it works.
class GameState:
    def __init__(self):

        # fmt:off
        # To represent blank space in board value 0 is taken.
        # X is value 1, O is value 2
        self.ValMap = [ # this initializes an empty board
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
            ]
        # fmt: on

        # self.player = ["playerX","playerO"]
        self.currentPlayer = "playerX"
        self.won = False
        self.winningPlayer = ""

    # function that returns the current player
    def getCurrentPlayer(self):
        return self.currentPlayer

    # function that controls the game. It takes a parameter called positionBox and checks if it's empty or not.
    # If it's empty, it checks for the current player and enter's their corresponding number at the given index in the board.
    # Finally it checks if the player's input has triggered a win condition.
    def putValue(self, positionBox):
        if self.ValMap[positionBox] == 0: # checking if board is empty
            # print("putValue triggered")
            if self.currentPlayer == "playerX": # when current player is X
                self.ValMap[positionBox] = 1 # it replaces 0 at the refrence location of the board with 1 ie. Player X's value.
                self.currentPlayer = "playerO" # This changes the turn from player X to player O
                self.checkWin() # checking if the player's input triggered a win condition
            elif self.currentPlayer == "playerO": # when current player is O
                self.ValMap[positionBox] = 2  # it replaces 0 at the refrence location of the board with 2 ie. Player O's value.
                self.currentPlayer = "playerX" # This changes the turn from player O to player X
                self.checkWin() # checking if the player's input triggered a win condition

    # function that takes three values and gives a string output if they are same and have value 1 or 2
    def checkIfSameValue(self, val1, val2, val3):
        values = [self.ValMap[val1], self.ValMap[val2], self.ValMap[val3]] # list having values of given position in Board
        if all(v == 1 for v in values): # 1 is the value for player X, checks if there are three 1s
            # print("1 win triggered")
            return "X Wins"
        if all(v == 2 for v in values): # 2 is the value for player O, checks if there are three 2s
            # print("2 win triggered")
            return "O Wins"

    def checkHorizontal(self):
        row1Status = self.checkIfSameValue(0, 1, 2) # check for top row
        row2Status = self.checkIfSameValue(3, 4, 5) # check for middle row
        row3Status = self.checkIfSameValue(6, 7, 8) # check for bottom row

        horizontalStatus = [row1Status, row2Status, row3Status] # list having status of all rows

        if any(status == "X Wins" for status in horizontalStatus):
            self.won = True
            self.winningPlayer = "playerX"

        if any(status == "O Wins" for status in horizontalStatus):
            self.won = True
            self.winningPlayer = "playerO"

    def checkVertical(self):
        column1Status = self.checkIfSameValue(0, 3, 6) # check for left column
        column2Status = self.checkIfSameValue(1, 4, 7) # check for middle column
        column3Status = self.checkIfSameValue(2, 5, 8) # check for right column

        verticalStatus = [column1Status, column2Status, column3Status] # list having status of all columns

        if any(status == "X Wins" for status in verticalStatus):
            self.won = True
            self.winningPlayer = "playerX"

        if any(status == "O Wins" for status in verticalStatus):
            self.won = True
            self.winningPlayer = "playerY"

    def checkDiagonal(self):
        diagonal1Status = self.checkIfSameValue(0, 4, 8) # check for \ diagonal
        diagonal2Status = self.checkIfSameValue(2, 4, 6) # check for / diagonal

        diagonalStatus = [diagonal1Status, diagonal2Status] # list having status of all diagonals

        if any(status == "X Wins" for status in diagonalStatus):
            self.won = True
            self.winningPlayer = "playerX"

        if any(status == "Y Wins" for status in diagonalStatus):
            self.won = True
            self.winningPlayer = "playerY"

    # Taking mouse input in pixels and checking where in which box the cursor is in
    def checkLoc(self, xLoc, yLoc):
        if xLoc >= 0 and xLoc <= 266 and yLoc >= 0 and yLoc <= 266: # Bounds of Top Left Box
            return 0
        elif xLoc >= 266 and xLoc <= 534 and yLoc >= 0 and yLoc <= 266: # Bounds of Top Middle Box
            return 1
        elif xLoc >= 534 and xLoc <= 800 and yLoc >= 0 and yLoc <= 266: # Bounds of Top Right Box
            return 2
        elif xLoc >= 0 and xLoc <= 266 and yLoc >= 266 and yLoc <= 534: # Bounds of Middle Left Box
            return 3
        elif xLoc >= 266 and xLoc <= 534 and yLoc >= 266 and yLoc <= 534: # Bounds of Middle Middle Box
            return 4
        elif xLoc >= 534 and xLoc <= 800 and yLoc >= 266 and yLoc <= 534: # Bounds of Middle Right Box
            return 5
        elif xLoc >= 0 and xLoc <= 266 and yLoc >= 534 and yLoc <= 800: # Bounds of Bottom Left Box
            return 6
        elif xLoc >= 266 and xLoc <= 534 and yLoc >= 534 and yLoc <= 800: # Bounds of Bottom Middle Box
            return 7
        elif xLoc >= 534 and xLoc <= 800 and yLoc >= 534 and yLoc <= 800: # Bounds of Bottom Right Box
            return 8

    def checkWin(self):
        # print("checkWin Triggered")
        self.checkDiagonal() # checks for if 3 value matches diagonally
        self.checkHorizontal()  # checks for if 3 value matches horizontally
        self.checkVertical()    # checks for if 3 value matches vertically

        return self.won # return the win condition variable

    # Takes a string and prints the board condition to console in 3x3 matrix order.
    # is Used during devlopment to keep track of the board's state
    def printBoardCondition(self, con):
        print(
            con,
            "\n",
            self.ValMap[0], #
            self.ValMap[1], # Top Row
            self.ValMap[2], #
            "\n",
            self.ValMap[3], #
            self.ValMap[4], # Middle Row
            self.ValMap[5], #
            "\n",
            self.ValMap[6], #
            self.ValMap[7], # Bottom Row
            self.ValMap[8], #
            "\n",
        )
