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
        self.white_king_loc = (4, 7)
        self.black_king_loc = (4, 0)
        self.checkmate = False
        self.stalemate = False
    
    def makeMove(self, move):
        self.Board[move.startY][move.startX] = '++'
        self.Board[move.endY][move.endX] = move.piezaMovio
        self.gameLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piezaMovio == 'wK':
            self.white_king_loc = (move.endX, move.endY)
        elif move.piezaMovio == 'bK':
            self.black_king_loc = (move.endX, move.endY)

    def undoMove(self, move):
        self.Board[move.startY][move.startX] = move.piezaMovio
        self.Board[move.endY][move.endX] = move.piezaCaptura
        self.gameLog.pop()
        self.whiteToMove = not self.whiteToMove
        if move.piezaMovio == 'wK':
            self.white_king_loc = (move.startX, move.startY)
        elif move.piezaMovio == 'bK':
            self.black_king_loc = (move.startX, move.startY)

    def pawn_moves(self, x, y, moves):
        if self.whiteToMove:
            if y == 0:
                pass

            else:
                if self.Board[y-1][x] == '++':
                    moves.append(Move((x,y), (x,y-1), self.Board))
                if y == 6 and self.Board[y-2][x] == '++':
                    moves.append(Move((x,y), (x,y-2), self.Board))
                if x > 0 and self.Board[y-1][x-1][0] == 'b':
                    moves.append(Move((x,y), (x-1,y-1), self.Board))
                if x < 7 and self.Board[y-1][x+1][0] == 'b':
                    moves.append(Move((x,y), (x+1,y-1), self.Board))
                                
        if not self.whiteToMove:
            if y == 7:
                pass

            else:
                if self.Board[y+1][x] == '++':
                    moves.append(Move((x,y), (x,y+1), self.Board))
                if y == 1 and self.Board[y+2][x] == '++':
                    moves.append(Move((x,y), (x,y+2), self.Board))
                if x > 0 and self.Board[y+1][x-1][0] == 'w':
                     moves.append(Move((x,y), (x+1,y+1), self.Board))
                if x < 7 and self.Board[y+1][x+1][0] == 'w':
                    moves.append(Move((x,y), (x+1,y+1), self.Board))

    def rook_moves(self, x, y, moves, color):
        directions = ((1,0), (0,-1), (-1,0), (0,1))

        for direction in directions:
            mov_x = x
            mov_y = y
            
            diferencia_x = x + 1 if direction[0] == -1 else col-x 
            diferencia_y = y + 1 if direction[1] == -1 else fil-y

            diferencia = abs(diferencia_x * direction[0] + diferencia_y *direction[1]) 

            for i in range(diferencia-1):
                mov_x += direction[0]
                mov_y += direction[1]

                if self.Board[mov_y][mov_x] != '++':
                    if self.Board[mov_y][mov_x][0] != color:
                        moves.append(Move((x,y), (mov_x, mov_y), self.Board))
                        break
                    else:
                        break
                                
                moves.append(Move((x,y), (mov_x, mov_y), self.Board))

    def knight_moves(self, x, y, moves, color):
        for i in range(col):
            for j in range(fil):
                if ((x-i)**2 + (y-j)**2) == 5:
                    move = Move((x,y), (i,j), self.Board)
                    if self.Board[j][i][0] != color:
                        moves.append(move)

    def bishop_moves(self, x, y, moves, color):
        directions = ((1,1), (1,-1), (-1,-1), (-1,1))

        for direction in directions:
            mov_x = x
            mov_y = y
            
            diferencia_x = x + 1 if direction[0] == -1 else col-x 
            diferencia_y = y + 1 if direction[1] == -1 else fil-y

            min_dif = min(diferencia_x, diferencia_y)
                            
            for i in range(min_dif-1):
                mov_x += direction[0]
                mov_y += direction[1]

                if self.Board[mov_y][mov_x] != '++':
                    if self.Board[mov_y][mov_x][0] != color:
                        moves.append(Move((x,y), (mov_x, mov_y), self.Board))
                        break
                    else:
                        break
                moves.append(Move((x,y), (mov_x, mov_y), self.Board))

    def queen_moves(self, x, y, moves, color):
        directions = ((1,0), (0,-1), (-1,0), (0,1), (1,1), (1,-1), (-1,-1), (-1,1))

        for direction in directions:
            mov_x = x
            mov_y = y
                            
            diferencia = 0
            if(abs(direction[0] + direction[1]) == 1):
                diferencia_x = x + 1 if direction[0] == -1 else col-x 
                diferencia_y = y + 1 if direction[1] == -1 else fil-y
                diferencia = abs(diferencia_x * direction[0] + diferencia_y *direction[1]) 
            else:
                diferencia_x = x + 1 if direction[0] == -1 else col-x 
                diferencia_y = y + 1 if direction[1] == -1 else fil-y
                diferencia = min(diferencia_x, diferencia_y)


            for i in range(diferencia-1):
                mov_x += direction[0]
                mov_y += direction[1]

                if self.Board[mov_y][mov_x] != '++':
                    if self.Board[mov_y][mov_x][0] != color:
                        moves.append(Move((x,y), (mov_x, mov_y), self.Board))
                        break
                    else:
                        break
                                
                moves.append(Move((x,y), (mov_x, mov_y), self.Board))

    def king_moves(self, x, y, moves, color):
        for i in range(col):
            for j in range(fil):
                if ((x-i)**2 + (y-j)**2) <= 2:
                    move = Move((x,y), (i,j), self.Board)
                    if self.Board[j][i][0] != color:
                        moves.append(move)
                        

    def getAllMoves(self):
        movimientos = []
        for y in range(fil):
            for x in range(col):
                color = self.Board[y][x][0]
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    pieza = self.Board[y][x][1]
                    if pieza == 'p':
                        self.pawn_moves(x, y, movimientos)

                    elif pieza == 'R':
                        self.rook_moves(x, y, movimientos, color)
                        
                    elif pieza == 'N':   
                        self.knight_moves(x, y, movimientos, color)

                    elif pieza == 'B':
                       self.bishop_moves(x, y, movimientos, color)
                    
                    elif pieza == 'Q':
                        self.queen_moves(x, y, movimientos, color)
                    
                    elif pieza == 'K':
                        self.king_moves(x, y, movimientos, color)
        return movimientos
# estas checando tus movimientos
# para cada movimiento lo haces
# checas si estas en jaque
# para checar si estas en jaque tienes que generar todos los movimientos del oponente

    def in_attack(self, x, y):
        moves = self.getAllMoves()
        for move in moves:
            if move.endX == x and move.endY == y:
                return True
        return False

    def in_check(self):
        if not self.whiteToMove: k_loc = self.white_king_loc 
        else: k_loc = self.black_king_loc
        return self.in_attack(k_loc[0], k_loc[1])


    def getValidMoves(self):
        movimientos = self.getAllMoves()
        for i in range(len(movimientos)-1, -1, -1):
            self.makeMove(movimientos[i])
            if self.in_check():
                print(movimientos[i].piezaMovio)
                self.undoMove(movimientos[i])
                movimientos.remove(movimientos[i])
            else:
                self.undoMove(movimientos[i])
        return movimientos

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

class Button():
    def __init__(self, x, y, image_path):
        # self.__OnLeftClickHandlers = []
        # self.__OnRightClickHandlers = [] #para futuro

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        pos = pygame.mouse.get_pos()

        mouseClick = False

        #event handler
        if self.rect.collidepoint(pos):
            print("hover")
            if pygame.mouse.get_pressed()[0]:
                # self.__handleEvent(self.__OnLeftClickHandlers);
                # for handler in self.__OnLeftClickHandlers:
                #     handler(self)
                mouseClick = True

        vent.blit(self.image, (self.rect.x, self.rect.y))

        return mouseClick

    # def __handleEvent(self, *handlers):
    #     for handler in handlers:
    #         handler();        


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
    showStartMenu = True
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
                        print(board.whiteToMove)
                        cdSele = ()
                        playerClicks = []
                        moveMade = True
                    else:
                        playerClicks = [cdSele]
            if key[pygame.K_LEFT]:
                move = board.gameLog[-1]
                board.undoMove(move)
                moveMade = True
                print('yay')
        
        if moveMade:
            validMoves = board.getValidMoves()
            moveMade = False
                    
        if showStartMenu:
            showStartMenu = not(drawStartMenu(vent))
        else:
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

def drawStartMenu(vent):
    vent.fill(pygame.Color('steelblue4'))
    btn_clasico = Button(156, 100, "Assets/Image/btn-clasico.png") 
    # btn_clasico._Button__OnLeftClickHandlers.append(On_btn_clsico_click)
    return btn_clasico.draw()

# def On_btn_clsico_click(sender):
#     showStartMenu = False

main()
