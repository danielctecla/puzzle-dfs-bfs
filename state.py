class State():

    def __init__(self, state=None, movement= None):
        if state is not None:
            self.state(state, movement)

    def state(self, state, movement=None):
        if movement is None:
            n = 0
            self.movement = None
        else:
            self.movement = movement
        self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for i in range(4):
            for j in range(4):
                if movement is None:
                    value = int(state[n])
                    self.board[i][j] = value
                    if self.board[i][j] == 0:
                        self.posI = i
                        self.posJ = j
                    n += 1
                else:
                    self.board[i][j] = state[i][j]
                    if self.board[i][j] == 0:
                        self.posI = i
                        self.posJ = j

    # def state(self, state):
    #     n = 0
    #     self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #     for i in range(4):
    #         for j in range(4):
    #             value = int(state[n])
    #             self.board[i][j] = value
    #             if self.board[i][j] == 0:
    #                 self.posI = i
    #                 self.posJ = j
    #             n += 1
        
    # def state(self, board, movement):
    #     self.movement = movement
    #     self.board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #     for i in range(4):
    #         for j in range(4):
    #             self.board[i][j] = board[i][j]
    #             if self.board[i][j] == 0:
    #                 self.posI = i
    #                 self.posJ = j

    def show(self):
        if self.movement != None:
            print(self.movement)
        print("+-+-+-+")
        for i in range(4):
            for j in range(4):
                print(self.board[i][j], end="|")
            print("\n+-+-+-+")
        

    def swap(self, i, j):
        aux = self.board[i][j]
        self.board[i][j] = 0
        self.board[self.posI][self.posJ] = aux
        self.posI = i
        self.posJ = j
        self.show()

    def nextStates(self):
        next = []
        newBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

        for i in range(4):
            for j in range(4):
                newBoard[i][j] = self.board[i][j]
        
        if self.posI > 0:
            newI = self.posI - 1
            newState = State(newBoard, "u")
            newState.swap(newI, self.posJ)
            next.append(newState)
        if self.posI < 3:
            newI = self.posI + 1
            newState = State(newBoard, "d")
            newState.swap(newI, self.posJ)
            next.append(newState)
        if self.posJ > 0:
            newJ = self.posJ - 1
            newState = State(newBoard, "l")
            newState.swap(self.posI, newJ)
            next.append(newState)
        if self.posJ < 3:
            newJ = self.posJ + 1
            newState = State(newBoard, "r")
            newState.swap(self.posI, newJ)
            next.append(newState)
        return next
    
    def getBoard(self):
        return self.board
    
    def getI(self):
        return self.posI
    
    def getJ(self):
        return self.posJ
    
    def getMovement(self):
        return self.movement

    def goalFunction(self, goal):
        goalBoard = goal.getBoard()
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != goalBoard[i][j]:
                    return False
        
        return True
            
    def isEquals(self, s):
        board = s.getBoard()
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != board[i][j]:
                    return False
        return True