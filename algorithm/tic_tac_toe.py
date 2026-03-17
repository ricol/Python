#!/usr/bin/env python
#-*- coding: utf-8 -*-

class TicTacToe:

    PLAYER_A = 'X'
    PLAYER_B = 'O'
    EMPTY = ' '

    def __init__(self):
        self._board = [[self.EMPTY] * 3 for _ in range(3)]
        self._player = self.PLAYER_A

    def mark(self, i, j):
        if not (0 <= i <= 2 and 0 <= j <= 2):
            raise ValueError('Invalid board position')
        if self._board[i][j] != self.EMPTY:
            raise ValueError('Board position occupied')
        if self.winner() is not None:
            raise ValueError('Game is already complete')
        self._board[i][j] = self._player
        self._player = self.PLAYER_A if self._player == self.PLAYER_B else self.PLAYER_B
        print(self)

    def _is_win(self, mark):
        board = self._board
        return (mark == board[0][0] == board[0][1] == board[0][2] or
                mark == board[1][0] == board[1][1] == board[1][2] or
                mark == board[2][0] == board[2][1] == board[2][2] or
                mark == board[0][0] == board[1][0] == board[2][0] or
                mark == board[0][1] == board[1][1] == board[2][1] or
                mark == board[0][2] == board[1][2] == board[2][2] or
                mark == board[0][0] == board[1][1] == board[2][2] or
                mark == board[0][2] == board[1][1] == board[2][0])

    def winner(self):
        for mark in [self.PLAYER_A, self.PLAYER_B]:
            if self._is_win(mark):
                return mark
        return None

    def __str__(self):
        rows = ['|'.join(self._board[r]) for r in range(3)]
        return '*' * 5 + "\n" + '\n-----\n'.join(rows)

if __name__ == '__main__':
    try:
        game = TicTacToe()
        game.mark(1, 1); game.mark(0, 2)
        game.mark(2, 2); game.mark(0, 0)
        game.mark(0, 1); game.mark(2, 1)
        game.mark(1, 2); game.mark(1, 0)
        game.mark(2, 0)
    except:
        pass
    finally:
        winner = game.winner()
        if winner is None:
            print("Tie")
        else:
            print("Winner: %s" % winner)
