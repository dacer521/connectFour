import random
import os

class Board:
    def __init__(self, cols, rows, AI):
        self.board = []
        self.cols = cols
        self.rows = rows
        self.AI = AI
        self.PLAYER1 = '\033[31mR\033[0m'
        self.PLAYER2 = '\033[33mY\033[0m'

    def createBoard(self):
        self.board = [['0' for _ in range(self.cols)] for _ in range(self.rows)]

    def checkDiagonals(self, player):
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True
        return False

    def checkRows(self, player):
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
        return False

    def checkCols(self, player):
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
        return False

    def __str__(self):
        header = ' '.join(map(str, range(1, self.cols + 1))) + '\n'
        rows = [' '.join(self.board[r]) for r in range(self.rows)]
        return header + '\n'.join(rows)

    def checkWin(self, player):
        return self.checkDiagonals(player) or self.checkRows(player) or self.checkCols(player)

    def checkTie(self):
        return all(self.board[row][col] != '0' for row in range(self.rows) for col in range(self.cols))

    def checkLegalMoves(self):
        legalMoves = {}
        position = 1
        for col in range(self.cols):
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] == '0':
                    legalMoves[position] = (row, col)
                    position += 1
                    break
        return legalMoves

    def AIPlay(self):
        legalMoves = self.checkLegalMoves()
        if not legalMoves:
            return False
        row, col = random.choice(list(legalMoves.values())) 
        self.play(col, self.PLAYER2)
        return True

    def play(self, col, player):
        if 0 <= col < self.cols:
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] == '0':
                    self.board[row][col] = player
                    return True
        return False

def main():
    playing = input("Would you like to play with a friend or against the computer? (F/C): ").upper()
    gameBoard = Board(7, 6, playing != 'F')
    gameBoard.createBoard()

    if gameBoard.AI:
        print("You are playing against the computer.")
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(gameBoard)
            while True:
                try:
                    moveCol = int(input("Enter a move (1-7): ")) - 1
                    if gameBoard.play(moveCol, gameBoard.PLAYER1):
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 1 and 7.")
            if gameBoard.checkWin(gameBoard.PLAYER1):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(gameBoard)
                print("You win!")
                break
            if gameBoard.checkTie():
                os.system('cls' if os.name == 'nt' else 'clear')
                print(gameBoard)
                print("It's a tie!")
                break
            if not gameBoard.AIPlay():
                os.system('cls' if os.name == 'nt' else 'clear')
                print(gameBoard)
                print("The computer wins!")
                break
            if gameBoard.checkWin(gameBoard.PLAYER2):
                print(gameBoard)
                print("Computer wins!")
                break
    else:
        print("You are playing against a friend.")
        current_player = gameBoard.PLAYER1
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(gameBoard)
            if gameBoard.checkWin(gameBoard.PLAYER1):
                print("Player 1 wins!")
                break
            if gameBoard.checkWin(gameBoard.PLAYER2):
                print("Player 2 wins!")
                break
            if gameBoard.checkTie():
                print("It's a tie!")
                break
            print(f"Player {'1' if current_player == gameBoard.PLAYER1 else '2'}'s turn.")
            while True:
                try:
                    moveCol = int(input("Enter a move (1-7): ")) - 1
                    if gameBoard.play(moveCol, current_player):
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 1 and 7.")
            current_player = gameBoard.PLAYER2 if current_player == gameBoard.PLAYER1 else gameBoard.PLAYER1

if __name__ == '__main__':
    main()