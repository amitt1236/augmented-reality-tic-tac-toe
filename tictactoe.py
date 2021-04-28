"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
board = [[None, None, None], [None, None, None], [None, None, None]]
turn = X


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if turn == 'X':
        turn = 'O'
    else:
        turn = "X"   


def result(board, action):
    """
    updates board with new move
    """
    i = action[0]
    j = action[1]

    if board[i][j] != None:
        raise Exception

    board[i][j] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check colums
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != None:
            return board[i][0]
    # check rows
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != None:
            return board[0][i]
    # check diagonal
    if board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[1][1] == board[0][2] and board[1][1] != None:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    if sum(j.count(None) for j in board) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    if winner(board) == "O":
        return -1
    else:
        return 0


def player(board):
    if sum(j.count(None) for j in board) % 2 == 1:
        return "X"
    else:
        return "O"        