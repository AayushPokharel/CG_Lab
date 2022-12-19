class GameState:

    def __init__(self):

        self.ValMap = [
            0,0,0,
            0,0,0,
            0,0,0
        ]
        

        #self.player = ["playerX","playerO"]
        self.currentPlayer = "playerX"
        self.won = False
        self.winningPlayer = ""

    """
    def changePlayer(self):
        if self.currentPlayer == "playerX":
            self.currentPlayer = "playerO"
        if self.currentPlayer == "playerO":
            self.currentPlayer = "playerX"
    """
    
    def getCurrentPlayer(self):
        return self.currentPlayer

    def putValue(self,positionBox):
        if self.ValMap[positionBox] == 0:
            #print("putValue triggered")
            if self.currentPlayer == "playerX":
                self.ValMap[positionBox] = 1
                self.currentPlayer = "playerO"
                self.checkWin()
            elif self.currentPlayer == "playerO":
                self.ValMap[positionBox] = 2
                self.currentPlayer = "playerX"  
                self.checkWin()
               
        
    
    def checkIfSameValue(self,val1,val2,val3):
        values = [self.ValMap[val1],self.ValMap[val2],self.ValMap[val3]]
        if all(v==1 for v in values):
            #print("1 win triggered")
            return "X Wins"
        if all(v==2 for v in values):
            #print("2 win triggered")
            return "O Wins"

    
    def checkHorizontal(self):
        row1Status = self.checkIfSameValue(0,1,2)
        row2Status = self.checkIfSameValue(3,4,5)
        row3Status = self.checkIfSameValue(6,7,8)

        horizontalStatus = [row1Status,row2Status,row3Status]

        if any(status=="X Wins" for status in horizontalStatus):
            self.won = True
            self.winningPlayer = "playerX"

        if any(status=="O Wins" for status in horizontalStatus):
            self.won = True
            self.winningPlayer = "playerO"
    
    def checkVertical(self):
        column1Status = self.checkIfSameValue(0,3,6)
        column2Status = self.checkIfSameValue(1,4,7)
        column3Status = self.checkIfSameValue(2,5,8)

        verticalStatus = [column1Status,column2Status,column3Status]

        if any(status=="X Wins" for status in verticalStatus):
            self.won = True
            self.winningPlayer = "playerX"

        if any(status=="O Wins" for status in verticalStatus):
            self.won = True
            self.winningPlayer = "playerY"

    def checkDiagonal(self):
        diagonal1Status = self.checkIfSameValue(0,3,6)
        diagonal2Status = self.checkIfSameValue(1,4,7)

        diagonalStatus = [diagonal1Status,diagonal2Status]

        if any(status=="X Wins" for status in diagonalStatus):
            self.won = True
            self.winningPlayer = "playerX"

        if any(status=="Y Wins" for status in diagonalStatus):
            self.won = True
            self.winningPlayer = "playerY"


    def checkLoc(self,xLoc,yLoc):
        if xLoc >= 0 and xLoc <= 266 and yLoc >= 0 and yLoc <= 266:
            return 0
        elif xLoc >= 266 and xLoc <= 534 and yLoc >= 0 and yLoc <= 266:
            return 1
        elif xLoc >= 534 and xLoc <= 800 and yLoc >= 0 and yLoc <= 266:
            return 2
        elif xLoc >= 0 and xLoc <= 266 and yLoc >= 266 and yLoc <= 534:
            return 3
        elif xLoc >= 266 and xLoc <= 534 and yLoc >= 266 and yLoc <= 534:
            return 4
        elif xLoc >= 534 and xLoc <= 800 and yLoc >= 266 and yLoc <= 534:
            return 5
        elif xLoc >= 0 and xLoc <= 266 and yLoc >=534 and yLoc <= 800:
            return 6
        elif xLoc >= 266 and xLoc <= 534 and yLoc >= 534 and yLoc <= 800:
            return 7
        elif xLoc >= 534 and xLoc <= 800 and yLoc >= 534 and yLoc <= 800:
            return 8

    def checkWin(self):
        #print("checkWin Triggered")
        self.checkDiagonal()
        self.checkHorizontal()
        self.checkVertical()

        return self.won

    def printBoardCondition(self,con):
        print(
            con,"\n",
            self.ValMap[0],self.ValMap[1],self.ValMap[2],"\n",
            self.ValMap[3],self.ValMap[4],self.ValMap[5],"\n",
            self.ValMap[6],self.ValMap[7],self.ValMap[8],"\n"
        )

    
