

class Player(object):
    TotalPlayers = 0
    Turn = 1

    def __init__(self, ai=False):
        '''Creates a Player object
        Team = total players + 1
        Position is the distance from Home, starting at -1 for start
        AI is a bool to determine if the player is AI (defaults to False)
        Coords are the coordinates on the grid (Dictionary with keys "p{piece#}")'''
        self.team = Player.TotalPlayers + 1
        self.positions = [-1,-1,-1,-1]
        self.ai = ai
        self.winPoints = 0
        self.homeCoords = -1

        match self.team:
            case 1:
                self.coords = {'p1':[13,11], 'p2':[13,11], 'p3':[13,11], 'p4':[13,11]} #[row,col]
                self.homeCoords = [13,11]
            case 2:
                self.coords = {'p1':[11,2], 'p2':[11,2], 'p3':[11,2], 'p4':[11,2]}
                self.homeCoords = [11,2]
            case 3:
                self.coords = {'p1':[2,4], 'p2':[2,4], 'p3':[2,4], 'p4':[2,4]}
                self.homeCoords = [2,4]
            case 4:
                self.coords = {'p1':[4,13], 'p2':[4,13], 'p3':[4,13], 'p4':[4,13]}
                self.homeCoords = [4,13]

        Player.TotalPlayers += 1

    def setAI(self, ai=True):
        self.ai = ai

    def getPiece(self):
        '''Returns the symbol accociated with the piece'''
        match self.team:
            case 1:
                return '♥'
            case 2:
                return '⚑'
            case 3:
                return '☻'
            case 4:
                return '♠'
            
    def getTurn(self):
        return Player.Turn
    
    def updateTurn(self):
        if self.getTurn() < Player.TotalPlayers:
            Player.Turn += 1
        else:
            Player.Turn = 1

    def pieceToPos(self, piece):
        '''Returns a piece's position with the piece's coordinate key'''
        return self.positions[int(piece[-1]) - 1]
    
    def calculateWinPoints(self):
        winList = []
        for i in self.positions:
            if i - 64 == 0:
                winList.append(1)
        return sum(winList)
            
    #Max moves == 64
    #58 til home
    def move(self, amt, piece):
        '''Moves the piece according to amount, won't move if it overshoots home'''

        print('pos:', self.pieceToPos(piece))
        if 64 - (self.pieceToPos(piece) + amt) >= 0: #Sees whether the move overshoots
            for i in range(amt):
                #Gets piece position to see if any special charactaristics apply
                #For home movement
                if 58 - (self.pieceToPos(piece) + 1) < 0:
                    match self.team:
                        case 1:
                            print('up')
                            self.coords[piece][0] = self.coords.get(piece)[0] - 1          
                        case 2:
                            print('right')
                            self.coords[piece][1] = self.coords.get(piece)[1] + 1
                        case 3:
                            print('down')
                            self.coords[piece][0] = self.coords.get(piece)[0] + 1
                        case 4:                           
                            print('left')
                            self.coords[piece][1] = self.coords.get(piece)[1] - 1
                #Default Movement
                elif self.pieceToPos(piece) != -1: 
                    if list(self.coords.get(piece))[0] == 15 and list(self.coords.get(piece))[1] > 0 and list(self.coords.get(piece)) != [13,12]: #move left
                        print('left')
                        self.coords[piece][1] = self.coords.get(piece)[1] - 1
                    elif self.coords.get(piece)[1] == 0 and self.coords.get(piece)[0] > 0: #move up
                        print('up')
                        self.coords[piece][0] = self.coords.get(piece)[0] - 1
                    elif self.coords.get(piece)[0] == 0 and self.coords.get(piece)[1] < 15: #move right
                        print('right')
                        self.coords[piece][1] = self.coords.get(piece)[1] + 1
                    elif self.coords.get(piece)[1] == 15 and self.coords.get(piece)[0] < 15: #move down
                        print('down')
                        self.coords[piece][0] = self.coords.get(piece)[0] + 1

                #For start movement
                elif self.pieceToPos(piece) == -1:
                    match self.team:
                        case 1:
                            print('down')
                            self.coords[piece][0] = self.coords.get(piece)[0] + 2
                        case 2:
                            print('left')
                            self.coords[piece][1] = self.coords.get(piece)[1] - 2
                        case 3:
                            print('up')
                            self.coords[piece][0] = self.coords.get(piece)[0] - 2
                        case 4:
                            print('right')
                            self.coords[piece][1] = self.coords.get(piece)[1] + 2

                

                self.positions[int(piece[-1]) - 1] += 1
            return True
        else:
            return False

