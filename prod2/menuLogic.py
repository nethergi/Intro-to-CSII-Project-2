from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
import player
import random as r


player1 = None
player2 = None
player3 = None
player4 = None


def playButtPressed(obj):
    '''Logic for when the play button is pressed.
    1st press: Prompts User to select player count and hides button
    2nd press: Selects 0 AI
    3rd press: Saves Log to txt file'''
    if obj.playPressed == 1:
        playerAmountPressed(obj, 0)
    elif obj.playPressed == 2:
        with open('log.txt', 'w') as log:
            log.write(obj.logBox.toPlainText())
            obj.playButton.setEnabled(False)
            obj.playButton.setText('Log Saved!')
            obj.playPressed = 3
    elif obj.playPressed == 0:
    
        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(0)
        obj.playButton.setGraphicsEffect(opEffect)
        obj.playButton.setEnabled(False)
        obj.playButton.setText('')

        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.inpOne.setGraphicsEffect(opEffect)
        obj.inpOne.setEnabled(True)

        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.inpThree.setGraphicsEffect(opEffect)
        obj.inpThree.setEnabled(True)

        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.inpTwo.setGraphicsEffect(opEffect)
        obj.inpTwo.setEnabled(True)

        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.inpFour.setGraphicsEffect(opEffect)
        obj.inpFour.setEnabled(True)

        obj.topLabel.setText('How many players?')

def hideAmtButts(obj):
    opEffect = QtWidgets.QGraphicsOpacityEffect()
    opEffect.setOpacity(0)
    obj.inpOne.setGraphicsEffect(opEffect)
    obj.inpOne.setText('')
    obj.inpOne.setEnabled(False)

    opEffect = QtWidgets.QGraphicsOpacityEffect()
    opEffect.setOpacity(0)
    obj.inpThree.setGraphicsEffect(opEffect)
    obj.inpThree.setText('')
    obj.inpThree.setEnabled(False)

    opEffect = QtWidgets.QGraphicsOpacityEffect()
    opEffect.setOpacity(0)
    obj.inpTwo.setGraphicsEffect(opEffect)
    obj.inpTwo.setText('')
    obj.inpTwo.setEnabled(False)

    opEffect = QtWidgets.QGraphicsOpacityEffect()
    opEffect.setOpacity(0)
    obj.inpFour.setGraphicsEffect(opEffect)
    obj.inpFour.setText('')
    obj.inpFour.setEnabled(False)

    opEffect = QtWidgets.QGraphicsOpacityEffect()
    opEffect.setOpacity(0)
    obj.playButton.setGraphicsEffect(opEffect)
    obj.playButton.setEnabled(False)
    obj.playButton.setText('')


def clearPlayerPieces(obj, player):
    '''Part 1 of rendering, clears board of player pieces'''
    for key in player.coords:
        item = QtWidgets.QTableWidgetItem('')
        obj.boardGrid.setItem(player.coords.get(key)[0], player.coords.get(key)[1], item)

def renderPlayer(obj, player):
    '''Part 2 of rendering, displays each player's pieces individually'''
    if player == None:
        return
    

    #renders pieces
    for key in player.coords:
        itemtxt = ''
        try:
            itemtxt = obj.boardGrid.item(player.coords.get(key)[0], player.coords.get(key)[1]).text()
        except AttributeError:
            pass

        
        item = QtWidgets.QTableWidgetItem(itemtxt + player.getPiece())
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        brush = None
        match player.team:
            case 1:
                brush = QtGui.QBrush(QtGui.QColor(111, 59, 0))
            case 2:
                brush = QtGui.QBrush(QtGui.QColor(0, 67, 10))
            case 3:
                brush = QtGui.QBrush(QtGui.QColor(163, 0, 2))
            case 4:
                brush = QtGui.QBrush(QtGui.QColor(21, 0, 255))

        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        item.setForeground(brush)
        obj.boardGrid.setItem(player.coords.get(key)[0], player.coords.get(key)[1], item)
        #obj .boardGrid.setColumnWidth(player.coords.get(key)[1], 32)
            


def attackCheck(obj, player):
    '''Checks whether anyone gets attacked, should be ran before rendering'''
    itemtxt = ''
    victim = None
    
    
    #If space is empty or populated by allies, all good
    if itemtxt == '' or player.getPiece().find(itemtxt):
        return
    #Else, murder
    else:
        itemtxt = itemtxt[0]
        if itemtxt == '♥':     #team 1
            global player1
            victim = player1
        elif itemtxt == '⚑':   #team 2
            global player2
            victim = player2
        elif itemtxt == '☻':   #team 3
            global player3
            victim = player3
        elif itemtxt == '♠':   #team 4
            global player4
            victim = player4

        for key in player.coords:
            if player.coords.get(key) == victim.coords.get(key):
                print('OOF')
                obj.logBox.append(f'Player {player.team} knocked out Player {victim.team}\'s piece(s) from coords {victim.coords.get(key)}!!')
                victim.coords.get[key][0] = victim.homeCoords
                victim.positions[victim.pieceToPos(key)] = -1

        

roll = None
rollPressed = 0
def rollButt(obj):
    '''Determines roll button actions
    1st press: generate a random number (randint(1, 12)) and tells the player of the roll
    2nd press: attempts to move the selected piece, if failed, tells the player to select another piece and repeats
    AI automatically does these steps'''
    player = None
    global player1
    global player2
    global player3
    global player4

    match player1.getTurn():
        case 1:
            player = player1
        case 2:
            player = player2
        case 3:
            player = player3
        case 4:
            player = player4

    global rollPressed
    if rollPressed == 0:
        global roll
        roll = r.randint(1, 12)

        obj.topLabel.setText(f'A {roll}! What pawn to move Player {player.getTurn()}?')
        obj.logBox.append(f'Player {player.getTurn()} rolled a {roll}')
        obj.rollButton.setText('Submit')
        rollPressed = 1

        if player.ai:
            for key in player.coords:
                if 64 - (player.pieceToPos(key) + roll) >= 0:
                    match int(key[-1]):
                        case 1:
                            obj.pieceOneRadio.click()
                        case 2:
                            obj.pieceTwoRadio.click()
                        case 3:
                            obj.pieceThreeRadio.click()
                        case 4:
                            obj.pieceFourRadio.click()
                    break
            obj.rollButton.click()

    elif rollPressed == 1:
        piece = ''
        if obj.pieceOneRadio.isChecked():
            piece = 'p1'
        elif obj.pieceTwoRadio.isChecked():
            piece = 'p2'
        elif obj.pieceThreeRadio.isChecked():
            piece = 'p3'
        elif obj.pieceFourRadio.isChecked():
            piece = 'p4'
        else:
            obj.topLabel.setText('Select a piece with the radio buttons bellow')
            return
        


        item = QtWidgets.QTableWidgetItem('')
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        obj.boardGrid.setItem(player.coords.get(piece)[0], player.coords.get(piece)[1], item)
        

        if not player.move(roll, piece):
            obj.topLabel.setText('Piece overshot, select another piece')
            
            if player.ai:
                match r.randint(1, 4):
                    case 1:
                        obj.pieceOneRadio.click()
                    case 2:
                        obj.pieceTwoRadio.click()
                    case 3:
                        obj.pieceThreeRadio.click()
                    case 4:
                        obj.pieceFourRadio.click()
                obj.topLabel.setText('AI error, please submit again')

            return
        attackCheck(obj, player)
        clearPlayerPieces(obj, player)
        obj.logBox.append(f'Player {player.getTurn()} moved piece_{piece[-1]} {roll} spaces')
        player.updateTurn()
        obj.topLabel.setText(f'Player {player.getTurn()}\'s turn')
        obj.rollButton.setText('Roll!')
        rollPressed = 0


        renderPlayer(obj, player)

        if player.calculateWinPoints() == 4:
            endGame(obj, False, player)
            return

        nextPlayer = None
        match player1.getTurn():
            case 1:
                nextPlayer = player1
            case 2:
                nextPlayer = player2
            case 3:
                nextPlayer = player3
            case 4:
                nextPlayer = player4

        if nextPlayer.ai:
            obj.rollButton.click()



def updateBoard(obj):
    #clearBoard(obj)
    renderPlayer(obj, player1)
    renderPlayer(obj, player2)
    renderPlayer(obj, player3)
    renderPlayer(obj, player4)


def playerAmountPressed(obj, amt):
    '''Determines amount button actions
    1st press: selects 1 - 4 total players
    2nd press: selects 0 - 4 AI, then hides the buttons and displays the log and roll button'''
    global player1
    global player2
    global player3
    global player4
    
    if obj.playPressed == 0:
        match amt:
            case 1:
                player1 = player.Player()

                obj.inpTwo.setEnabled(False)
                obj.inpThree.setEnabled(False)
                obj.inpFour.setEnabled(False)
            case 2:
                player1 = player.Player()
                player2 = player.Player()

                obj.inpThree.setEnabled(False)
                obj.inpFour.setEnabled(False)
            case 3:
                player1 = player.Player()
                player2 = player.Player()
                player3 = player.Player()

                obj.inpFour.setEnabled(False)
            case 4:
                player1 = player.Player()
                player2 = player.Player()
                player3 = player.Player()
                player4 = player.Player()
        obj.playPressed = 1
        obj.topLabel.setText('How many are AI?')
        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.playButton.setGraphicsEffect(opEffect)
        obj.playButton.setEnabled(True)
        obj.playButton.setText('0')

    elif obj.playPressed == 1:
        match amt:
            case 0:
                pass
            case 1:
                player1.setAI()
            case 2:
                player1.setAI()
                player2.setAI()
            case 3:
                player1.setAI()
                player2.setAI()
                player3.setAI()
            case 4:
                player1.setAI()
                player2.setAI()
                player3.setAI()
                player4.setAI()
        
        hideAmtButts(obj)

        obj.logBox.setEnabled(True)
        

        obj.logBox.setGeometry(QtCore.QRect(10, 570, 211, 151))
        opEffect1 = QGraphicsOpacityEffect()
        opEffect1.setOpacity(100)
        opEffect2 = QGraphicsOpacityEffect()
        opEffect2.setOpacity(100)
        opEffect3 = QGraphicsOpacityEffect()
        opEffect3.setOpacity(100)
        opEffect4 = QGraphicsOpacityEffect()
        opEffect4.setOpacity(100)

        obj.logBox.setGraphicsEffect(opEffect1)
        obj.pieceOneRadio.setGraphicsEffect(opEffect1)
        obj.pieceTwoRadio.setGraphicsEffect(opEffect2)
        obj.pieceThreeRadio.setGraphicsEffect(opEffect3)
        obj.pieceFourRadio.setGraphicsEffect(opEffect4)

        obj.pieceOneRadio.setEnabled(True)
        obj.pieceTwoRadio.setEnabled(True)
        obj.pieceThreeRadio.setEnabled(True)
        obj.pieceFourRadio.setEnabled(True)

        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.rollButton.setGraphicsEffect(opEffect)
        obj.rollButton.setText('Roll!')
        obj.rollButton.setEnabled(True)

        obj.topLabel.setText('Player 1\'s Turn')

        opEffect = QtWidgets.QGraphicsOpacityEffect()
        opEffect.setOpacity(100)
        obj.endButton.setGraphicsEffect(opEffect)
        obj.endButton.setEnabled(True)

        updateBoard(obj)

        if player1.ai:
            obj.pieceOneRadio.click()
            obj.rollButton.click()

def endGame(obj, premature=True, player=None):
    '''End game logic, says whether the game was ended early or not and allows user to save Log as a txt'''
    opEffect1 = QGraphicsOpacityEffect()
    opEffect1.setOpacity(0)
    opEffect2 = QGraphicsOpacityEffect()
    opEffect2.setOpacity(0)
    opEffect3 = QGraphicsOpacityEffect()
    opEffect3.setOpacity(0)
    opEffect4 = QGraphicsOpacityEffect()
    opEffect4.setOpacity(0)
    opEffect5 = QGraphicsOpacityEffect()
    opEffect5.setOpacity(0)
    opEffect6 = QGraphicsOpacityEffect()
    opEffect6.setOpacity(0)

    obj.pieceOneRadio.setGraphicsEffect(opEffect1)
    obj.pieceTwoRadio.setGraphicsEffect(opEffect2)
    obj.pieceThreeRadio.setGraphicsEffect(opEffect3)
    obj.pieceFourRadio.setGraphicsEffect(opEffect4)

    obj.rollButton.setEnabled(False)
    obj.rollButton.setGraphicsEffect(opEffect5)

    obj.pieceOneRadio.setEnabled(False)
    obj.pieceTwoRadio.setEnabled(False)
    obj.pieceThreeRadio.setEnabled(False)
    obj.pieceFourRadio.setEnabled(False)

    opEffect = QtWidgets.QGraphicsOpacityEffect()
    opEffect.setOpacity(100)
    obj.playButton.setGraphicsEffect(opEffect)
    obj.playButton.setEnabled(True)
    obj.playButton.setText('Save Log?')

    obj.endButton.setGraphicsEffect(opEffect6)
    obj.endButton.setEnabled(False)
    
    if not premature:
        obj.topLabel.setText(f'{player.getPiece()}-PLAYER {player.team} WINS-{player.getPiece()}')
        obj.logBox.append(f'\n{player.getPiece()} -! PLAYER {player.team} WINS !- {player.getPiece()}')
    else:
        obj.logBox.append('\n-~-GAME ENDED EARLY-~-\n')
        winner = -1
        maxp = -1
        if player1 != None and player1.winPoints > maxp:
            winner = 1
            maxp = player1.winPoints
        if player2 != None and player2.winPoints > maxp:
            winner = 2
            maxp = player2.winPoints
        if player3 != None and player3.winPoints > maxp:
            winner = 3
            maxp = player3.winPoints
        if player4 != None and player4.winPoints > maxp:
            winner = 4
            maxp = player4.winPoints
        
        if maxp == 0:
            winner = -1

        if winner == -1:
            obj.topLabel.setText(f'Game ended too early...')
            obj.logBox.append('Game ended to early to call...')
        else:
            obj.topLabel.setText(f'Player {winner} Wins!')
            obj.logBox.append(f'Player {winner} Wins!')

    obj.playPressed = 2

    