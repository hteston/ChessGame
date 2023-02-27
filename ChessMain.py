"""
Responsible for handling the current state of the chess game. Also responsible for determining the valid moves
also it will have the move log in here.
"""

import pygame as p
from Chess import ChessEngine, ChessAI

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chessimages/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False


    loadImages()
    running = True
    sqSelected = () #keep track of last click of user
    playerClicks = [] #keep track of player clicks
    gameOver = False
    playerOne = False #if human white then true, if ai then false
    playerTwo = False #set to AI
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r: #undo when 'r' is pressed
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_z: #reset the board with 'z'
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False

        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'StALeMaTe')
        clock.tick(MAX_FPS)
        p.display.flip()

'''highlight square selected'''

def highlightSquare(screen, gs, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))



'''
Responsible for all graphics within current game state
'''
def drawGameState(screen, gs, sqSelected):
    drawBoard(screen) #draw squares onto board
    highlightSquare(screen, gs, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on square

'''
draw squares on board
'''
def drawBoard(screen):
    colors = [p.Color("lightyellow"), p.Color("lightgreen")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
''''
draw pieces onto current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, r*SQ_SIZE, r*SQ_SIZE))

def drawText(screen,text):
    font = p.font.SysFont('Helvitca', 100, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Gray"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()


