import pygame
import time



col, fil = 8, 8
cafe = (155, 103, 60)
blanco = (200, 200, 200)
negro = (0, 0, 0)
ancho = 512
largo = ancho
sqrs = ancho // col
vent = pygame.display.set_mode((largo, ancho))
clock = pygame.time.Clock()
pygame.display.set_caption('Ajedrez Musical')


class GameState:
    def __init__(self):
        self.Board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['++', '++', '++', '++', '++', '++', '++', '++'],
                      ['++', '++', '++', '++', '++', '++', '++', '++'],
                      ['++', '++', '++', '++', '++', '++', '++', '++'],
                      ['++', '++', '++', '++', '++', '++', '++', '++'],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteToMove = True
        self.gameLog = []
    
    def makeMove(self, move):
        self.Board[move.startY][move.startX] = '++'
        self.Board[move.endY][move.endX] = move.piezaMovio
        self.gameLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self, move):
        self.Board[move.startY][move.startX] = move.piezaMovio
        self.Board[move.endY][move.endX] = move.piezaCaptura
        self.gameLog.pop()
        self.whiteToMove = not self.whiteToMove

    def getAllMoves(self):
        movimientos = []
        for y in range(fil):
            for x in range(col):
                color = self.Board[y][x][0]
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    pieza = self.Board[y][x][1]
                    if pieza == 'p':
                        if color == 'w':
                            if y == 0:
                                pass

                            else:
                                if self.Board[y-1][x] == '++':
                                    movimientos.append(Move((x,y), (x,y-1), self.Board))
                                if y == 6 and self.Board[y-2][x] == '++':
                                    movimientos.append(Move((x,y), (x,y-2), self.Board))
                                if x > 0 and self.Board[y-1][x-1][0] == 'b':
                                    movimientos.append(Move((x,y), (x-1,y-1), self.Board))
                                if x < 7 and self.Board[y-1][x+1][0] == 'b':
                                    movimientos.append(Move((x,y), (x+1,y-1), self.Board))
                                

                    elif pieza == 'R':
                        for i in range(col - x):
                            movimientos.append(Move((x,y), (x+i,y), self.Board))
                        for i in range(x):
                            movimientos.append(Move((x,y), (x-i,y), self.Board))
                        for i in range(fil - y):
                            movimientos.append(Move((x,y), (x,y+i), self.Board))
                        for i in range(y):
                            movimientos.append(Move((x,y), (x,y-i), self.Board))
                        
                    elif pieza == 'N':
                        movimientos.append(Move((x,y), (x+2, y+1), self.Board))
                        movimientos.append(Move((x,y), (x+2, y-1), self.Board))
                        movimientos.append(Move((x,y), (x-2, y+1), self.Board))
                        movimientos.append(Move((x,y), (x-2, y-1), self.Board))
                        movimientos.append(Move((x,y), (x+1, y+2), self.Board))
                        movimientos.append(Move((x,y), (x+1, y-2), self.Board))
                        movimientos.append(Move((x,y), (x-1, y+2), self.Board))
                        movimientos.append(Move((x,y), (x-1, y-2), self.Board))

                        if x<2:
                            if y==0:
                                movimientos.pop()
                            if y==7:
                                movimientos.pop()
                        if x>5:
                            if(y==0):
                                movimientos.pop()
                            if(y==7):
                                movimientos.pop()
                        if y<2:
                            
                            movimientos.pop()
                            movimientos.pop()
                        if y>5:
                            movimientos.pop()
                            movimientos.pop()

                    elif pieza == 'B':
                        pass
                    elif pieza == 'Q':
                        pass
                    elif pieza == 'K':
                        pass
        return movimientos

    def getValidMoves(self):
        return self.getAllMoves()

class Move:

    rowsToRanks = {7:'1', 6:'2', 5:'3', 4:'4', 3:'5', 2:'6', 1:'7', 0:'8'}
    ranksToRows = {v: k for k, v in rowsToRanks.items()}
    colsToFiles = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    filesToCols = {v: k for k, v in colsToFiles.items()}

    def __init__(self, start, end, board):
        self.startX = start[0]
        self.startY = start[1]
        self.endX = end[0]
        self.endY = end[1]
        self.piezaMovio = board[self.startY][self.startX]
        self.piezaCaptura = board[self.endY][self.endX]
        self.moveID = 1000*self.startX + 100*self.startY + 10*self.endX + self.endY

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False 
    
    def getChessNotation(self):
        return self.getRankFile(self.startY, self.startX) + self.getRankFile(self.endY, self.endX)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # def getNotes(self, start, end):
    #     return self.colsToNotes[]

        

imagenes = {}
def cargarImagenes():
    piezas = ['bp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for i in piezas:
        imagenes[i] = pygame.transform.scale(pygame.image.load(i + '.png'), (sqrs, sqrs))

sonidos = {}
def cargarSonidos():
    columnas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C3', 
                'C#3', 'D3', 'E3', 'F3', 'Cpiano', 'C#piano', 'Dpiano', 'D#piano', 
                'Epiano', 'Fpiano', 'F#piano', 'Gpiano', 'G#piano', 'Apiano', 'A#piano', 'Bpiano', 'C1piano',
                'Cchello','Dchello', 'Echello', 'Fchello', 'Gchello', 'Achello', 'Bchello', 'C2chello']
    for i in columnas:
        sonidos[i] = pygame.mixer.Sound(i + '.wav')

# desicion = input('¿Qué sonidos?\n')

# if desicion == '1':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F', 4:'G', 5:'A', 6:'B', 7:'C3'}
#     rowsToNotes = {7:'C', 6:'D', 5:'E', 4:'F', 3:'G', 2:'A', 1:'B', 0:'C3'}
# elif desicion == '1r':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F', 4:'G', 5:'A', 6:'B', 7:'C3'}
#     rowsToNotes = {7:'C3', 6:'B', 5:'A', 4:'G', 3:'F', 2:'E', 1:'D', 0:'C'}
# elif desicion == '1c':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F', 4:'G', 5:'A', 6:'B', 7:'C3'}
#     rowsToNotes = {7:'Cchello', 6:'Dchello', 5:'Echello', 4:'Fchello', 3:'Gchello', 
#                   2:'Achello', 1:'Bchello', 0:'C2chello'}
# elif desicion == '8':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F', 4:'G', 5:'A', 6:'B', 7:'C3'}
#     rowsToNotes = {7:'Cpiano', 6:'Dpiano', 5:'Epiano', 4:'Fpiano', 3:'Gpiano', 2:'Apiano', 1:'Bpiano', 0:'C1piano'}
# elif desicion == '2':
#     colsToNotes = {0:'C', 1:'D', 2:'D#', 3:'F', 4:'G', 5:'G#', 6:'A#', 7:'C3'}
#     rowsToNotes = {7:'C', 6:'D', 5:'D#', 4:'F', 3:'G', 2:'G#', 1:'A#', 0:'C3'}
# elif desicion == '3':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'G', 4:'A', 5:'C3', 6:'D3', 7:'E3'}
#     rowsToNotes = {7:'C', 6:'D', 5:'E', 4:'G', 3:'A', 2:'C3', 1:'D3', 0:'E3'}
# elif desicion == '4':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F#', 4:'G', 5:'A', 6:'B', 7:'C3'}
#     rowsToNotes = {7:'C', 6:'D', 5:'E', 4:'F#', 3:'G', 2:'A', 1:'B', 0:'C3'}
# elif desicion == '5':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F', 4:'G', 5:'G#', 6:'A#', 7:'C3'}
#     rowsToNotes = {7:'C', 6:'D', 5:'E', 4:'F', 3:'G', 2:'G#', 1:'A#', 0:'C3'}
# elif desicion == '6':
#     colsToNotes = {0:'C', 1:'D', 2:'E', 3:'F#', 4:'G#', 5:'A#', 6:'C3', 7:'D3'}
#     rowsToNotes = {7:'C', 6:'D', 5:'E', 4:'F#', 3:'G#', 2:'A#', 1:'C3', 0:'D3'}
# else:
#     colsToNotes = {0:'C', 1:'C#', 2:'E', 3:'F', 4:'G', 5:'G#', 6:'A#', 7:'C3'}
#     rowsToNotes = {7:'C', 6:'C#', 5:'E', 4:'F', 3:'G', 2:'G#', 1:'A#', 0:'C3'}

######################################################################################################################
######################################################################################################################

def main():
    done = False
    board = GameState()
    pygame.init()
    moveMade = False
    validMoves = board.getValidMoves()
    cargarImagenes()
    cargarSonidos()
    cdSele = ()
    playerClicks = []
    while not done:

        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(posX // sqrs), int(posY // sqrs)
                # cifX = colsToNotes[celX]
                # cifY = rowsToNotes[celY]
                # sonidos[cifX].play()
                # sonidos[cifY].play()
                if cdSele == (celX, celY):
                    cdSele = ()
                    playerClicks = []
                else:
                    cdSele = (celX, celY)
                    playerClicks.append(cdSele)

                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], board.Board)
                    if move in validMoves:
                        board.makeMove(move)
                        cdSele = ()
                        playerClicks = []
                        moveMade = True
                    else:
                        print('invalido')
                        cdSele = ()
                        playerClicks = []
            if key[pygame.K_LEFT]:
                move = board.gameLog[-1]
                board.undoMove(move)
                moveMade = True
                print('yay')
        
        if moveMade:
            validMoves = board.getValidMoves()
            moveMade = False
                    


        drawBoard(vent)
        drawPieces(vent, board.Board)
        clock.tick(15)
        pygame.display.flip()

# pygame.Color('steelblue4')
def drawBoard(vent):
    colores = [pygame.Color('white'), pygame.Color('steelblue4')]
    for c in range(col):
        for f in range(fil):
            color = colores[(c + f) % 2]
            celda = (c*sqrs, f*sqrs, sqrs, sqrs)
            pygame.draw.rect(vent, color, celda)

def drawPieces(vent, board):
    for c in range(col):
        for f in range(fil):
            pieza = board[f][c]
            if pieza != '++':
                vent.blit(imagenes[pieza], pygame.Rect(c*sqrs, f*sqrs, sqrs, sqrs))



main()
