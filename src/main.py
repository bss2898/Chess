import argparse
import random
import sys

from src.AI import AI
from src.Board import Board
from src.InputParser import InputParser

WHITE = True
BLACK = False


def askForPlayerSide():
    playerChoiceInput = input(
        "What side would you like to play as [wB]? ").lower()
    if 'w' in playerChoiceInput:
        print("You will play as white")
        return WHITE
    else:
        print("You will play as black")
        return BLACK


def askForDepthOfAI():
    depthInput = 2
    try:
        depthInput = int(input("How deep should the AI look for moves?\n"
                               "Warning : values above 3 will be very slow."
                               " [2]? "))
        while depthInput<=0:
             depthInput = int(input("How deep should the AI look for moves?\n"
                               "Warning : values above 3 will be very slow. "
                               "Your input must be above 0."
                               " [2]? "))

    except KeyboardInterrupt:
        sys.exit()
    except:
        print("Invalid input, defaulting to 2")
    return depthInput


def printCommandOptions():
    undoOption = 'u : undo last move'
    printLegalMovesOption = 'l : show all legal moves'
    randomMoveOption = 'r : make a random move'
    printGameMoves = 'gm: moves of current game in PGN format'
    quitOption = 'quit : resign'
    moveOption = 'a3, Nc3, Qxa2, etc : make the move'
    options = [undoOption, printLegalMovesOption, randomMoveOption, printGameMoves,
               quitOption, moveOption, '', ]
    print('\n'.join(options))


def printAllLegalMoves(board, parser):
    for move in parser.getLegalMovesWithNotation(board.currentSide, short=True):
        print(move.notation)


def getRandomMove(board, parser):
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notationForMove(randomMove)
    return randomMove


def makeMove(move, board):
    print("Making move : " + move.notation)
    board.makeMove(move)


def printPointAdvantage(board):
    print("Currently, the point difference is : " +
          str(board.getPointAdvantageOfSide(board.currentSide)))


def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()

def printBoard(board):
    print()
    print(board)
    print()

def printGameMoves(history):
    counter = 0
    for num, mv in enumerate(history):
        if num % 2 == 0:
            if counter % 6 == 0:
                print()
            print(f'{counter + 1}.', end=" ")
            counter += 1

        print(mv[0].notation, end=" ")
    print()


def startGame(board, playerSide, ai):
    parser = InputParser(board, playerSide)
    while True:
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print("Checkmate, you lost")
            else:
                print("Checkmate! You won!")
            printGameMoves(board.history)
            return

        if board.isStalemate():
            print("Stalemate")
            printGameMoves(board.history)
            return

        if board.noMatingMaterial():
            print("Draw due to no mating material")
            printGameMoves(board.history)
            return

        if board.currentSide == playerSide:
            # printPointAdvantage(board)
            move = None
            command = input("It's your move."
                            " Type '?' for options. ? ")
            if command.lower() == 'u':
                undoLastTwoMoves(board)
                printBoard(board)
                continue
            elif command.lower() == '?':
                printCommandOptions()
                continue
            elif command.lower() == 'l':
                printAllLegalMoves(board, parser)
                continue
            elif command.lower() == 'gm':
                printGameMoves(board.history)
            elif command.lower() == 'r':
                move = getRandomMove(board, parser)
            elif command.lower() == 'exit' or command.lower() == 'quit':
                return
            try:
                if move is None:
                    move = parser.parse(command)
            except ValueError as error:
                print("%s" % error)
                continue
            makeMove(move, board)
            printBoard(board)

        else:
            print("AI thinking...")
            move = ai.getBestMove()
            move.notation = parser.notationForMove(move)
            makeMove(move, board)
            printBoard(board)

def twoPlayerGame(board):
    parserWhite = InputParser(board, WHITE)
    parserBlack = InputParser(board, BLACK)
    while True:
        printBoard(board)
        if board.isCheckmate():
            print("Checkmate")
            printGameMoves(board.history)
            return

        if board.isStalemate():
            print("Stalemate")
            printGameMoves(board.history)
            return

        if board.noMatingMaterial():
            print("Draw due to no mating material")
            printGameMoves(board.history)
            return

        # printPointAdvantage(board)
        if board.currentSide == WHITE:
            parser = parserWhite
        else:
            parser = parserBlack
        move = None
        command = input("It's your move, {}.".format(board.currentSideRep()) + \
                        " Type '?' for options. ? ")
        if command.lower() == 'u':
            undoLastTwoMoves(board)
            continue
        elif command.lower() == '?':
            printCommandOptions()
            continue
        elif command.lower() == 'l':
            printAllLegalMoves(board, parser)
            continue
        elif command.lower() == 'gm':
            printGameMoves(board.history)
        elif command.lower() == 'r':
            move = getRandomMove(board, parser)
        elif command.lower() == 'exit' or command.lower() == 'quit':
            return
        try:
            move = parser.parse(command)
        except ValueError as error:
            print("%s" % error)
            continue
        makeMove(move, board)


board = Board()

def main():
    parser = argparse.ArgumentParser(
        prog="chess",
        description="A python program to play chess "
                    "against an AI in the terminal.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Enjoy the game!"
    )
    parser.add_argument(
        '-t',
        '--two',
        action='store_true',
        default=False,
        help="to play a 2-player game"
    )
    parser.add_argument(
        '-u',
        '--unicode',
        action='store_true',
        default=False,
        help="display chess pieces using unicode characters"
    )
    parser.add_argument(
        '-w',
        '--white',
        action='store',
        default="blue",
        metavar='W',
        help="color for white player"
    )
    parser.add_argument(
        '-b',
        '--black',
        action='store',
        default="red",
        metavar='B',
        help="color for black player"
    )
    args = parser.parse_args()
    board.unicode = args.unicode
    board.whiteColor = args.white
    board.blackColor = args.black

    try:
        if args.two:
            twoPlayerGame(board)
        else:
            playerSide = askForPlayerSide()
            board.currentSide = playerSide
            print()
            aiDepth = askForDepthOfAI()
            opponentAI = AI(board, not playerSide, aiDepth)
            printBoard(board)
            startGame(board, WHITE, opponentAI)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
