import numpy as np
import pandas as pd
import copy
from colorama import Fore, Back, Style
import itertools
import threading
import time
import random

print("Welcome to Sudoku")
board = []

locker = threading.Lock()

originalIndex = []

def main():

    global board
    while True:
        choice = input("Menu\n[1]: Enter your Puzzel for Validation\n[2]: Enter your Puzzel for Solving\n[3]: Exit: ")
        if choice == '1':
            board = []
            print("Validation\n")
            for row in range(0, 9):
                board.append(input().replace(" ", ""))
            for index, line in enumerate(board):
                board[index] = list(line)
            if isCorrect() == True:
                estT = time.time()
                t1 = threading.Thread(target=RowChecker)
                t2 = threading.Thread(target=ColumnChecker)
                t1.start()
                t2.start()
                gno = 0
                for i in [0, 3, 6]:
                    for j in [0, 3, 6]:
                        gno += 1
                        t3 = threading.Thread(target=SquaresChecker, args=(i, j, gno,))
                        t3.start()
                        print("\n\nActive Thread", threading.activeCount())
                        print("\n\nActive Thread", threading.enumerate())
                t1.join()
                t2.join()
                t3.join()
                print("Done in ", time.time() - estT, "Seconds")
            else:
                print("Board is incorrect")

        elif choice == '2':
            board = []
            print("Solving ...\n")

            for row in range(0, 9):
                board.append(input().replace(" ", ""))

            if isCorrect() == True:
                global originalIndex
                for index, line in enumerate(board):
                    board[index] = list(line)

                for index, x in enumerate(board):
                    for i, y in enumerate(x):
                        if board[index][i] != "_":
                            originalIndex.append((index, i))
                HardSolve()
                print("Solved Puzzel\n")
                printBoard()
                estT = time.time()
                t1 = threading.Thread(target=RowChecker)
                t2 = threading.Thread(target=ColumnChecker)
                t1.start()
                t2.start()
                gno = 0
                for i in [0, 3, 6]:
                    for j in [0, 3, 6]:
                        gno += 1
                        t3 = threading.Thread(target=SquaresChecker, args=(i, j, gno,))
                        t3.start()
                        # print("\n\nActive Thread", threading.activeCount())
                        # print("\n\nActive Thread", threading.enumerate())
                t1.join()
                t2.join()
                t3.join()
                print("Done in ", time.time() - estT, "Seconds")

            else:
                print("Board is incorrect")

        elif choice == '3':
            print("\nThanks for using our Game\n")
            break

#********************SOLVING SECTION********************

# Simply we try to look for a cell that has only one number to put and start over again
def EasySolve():
    global board
    newEdit = False
    while True:
        newEdit = False
        for i in range(0, 9):
            for j in range(0, 9):
                possibilities = getPossibilities(i, j)
                if possibilities == False:
                    continue

                if len(possibilities) == 0:
                    raise RuntimeError("ERROR! No Solution")

                if len(possibilities) == 1:
                    board[i][j] = possibilities[0]
                    newEdit = True

        if newEdit == False:
            return

# In this function: Fisrt, we try to solve the puzzle with EasySolve() fun. but if it couldn't solve it we then use a recursive solution to solve it called backtrack algorithm.
def HardSolve():
    global board
    try:
        EasySolve()
    except:
        return False

    if isComplete() == True:
        return True

    i, j = 0, 0
    for index, row in enumerate(board):
        for colIndex, col in enumerate(row):
            if col == '_':
                i,j = index, colIndex


    possibilities = getPossibilities(i, j)
    for value in possibilities:
        lastCopy = copy.deepcopy(board)
        board[i][j] = value
        result = HardSolve()
        if result == True:
            return True
        else:
            board = copy.deepcopy(lastCopy)

    return False

# Get all possible numbers that can be inserted in each empty cell
def getPossibilities(i, j):
    global board
    if board[i][j] != '_':
        return False

    possibilities = {str(n) for n in range(1, 10)}

    for val in board[i]:
        possibilities -= set(val)

    for index in range(0, 9):
        possibilities -= set(board[index][j])

    iStart = (i // 3) * 3
    jStart = (j // 3) * 3

    subboard = board[iStart:iStart+3]
    for index, row in enumerate(subboard):
        subboard[index] = row[jStart:jStart+3]

    for row in subboard:
        for col in row:
            possibilities -= set(col)
    return list(possibilities)



#********************CHECKER SECTION********************
# This function is used to check the each row contains the numbers from 1-9 and no duplicated numbers
def RowChecker():
    global board
    #time.sleep(random.randint(1, 5))
    #print(threading.current_thread().name)
    rowValid = {str(n) for n in range(1, 10)}
    ErrorRow = []
    rowNo = 1

    for row in board:
        rowNo += 1
        rowValid -= set(row)

        if len(rowValid) == 0:
            rowValid = {str(n) for n in range(1, 10)}
        else:
            ErrorRow.append(rowNo-1)
            rowValid = {str(n) for n in range(1, 10)}

    if len(ErrorRow) == 0:
        print("Rows are correct")
    else:
        for e in ErrorRow:
            print("Row No. ", e, " is not valid")
        #return False

# This function is used to check the each column contains the numbers from 1-9 and no duplicated numbers
def ColumnChecker():
    global board
    #time.sleep(random.randint(1, 5))
    #print(threading.current_thread().name)
    colValid = {str(n) for n in range(1, 10)}
    ErrorColumn = []

    for col in range(0, 9):

        for row in range(0, 9):
            colValid -= set(board[row][col])

        if len(colValid) == 0:
            colValid = {str(n) for n in range(1, 10)}
        else:
            ErrorColumn.append(col + 1)
            colValid = {str(n) for n in range(1, 10)}

    if len(ErrorColumn) == 0:
        print("Columns are correct")
    else:
        for e in ErrorColumn:
            print("Column No. ", e, " is not valid")
        #return False

# This function is used to check the each subsquare contains the numbers from 1-9 and no duplicated numbers
def SquaresChecker(i, j, n):
    global board
    time.sleep(1)
    #print("Thread ", n, "stops")
    #print(threading.current_thread().name)
    subboard = []
    iStart = (i // 3) * 3
    jStart = (j // 3) * 3

    SquareValid = {str(n) for n in range(1, 10)}

    subboard = board[iStart:iStart + 3]
    for index, row in enumerate(subboard):
        subboard[index] = row[jStart:jStart + 3]

    for row in subboard:
        for col in row:
            SquareValid -= set(col)

    if len(SquareValid) != 0:
        print("Sub grid No.: ", n, "is incorrect.")
    else:
        print("Sub-Grid No.: ", n, "is correct")

# Check there is no missing cells
def isComplete():
    global board
    for row in board:
        for col in row:
            if col == '_':
                return False
    return True

# Check that the structure of the board is correct
def isCorrect():
    global board
    for row in board:
        if len(row) != 9:
            return False
    return True

# Print the board in the console
def printBoard():
    global board
    global originalIndex
    for index, row in enumerate(board):
        for i, column in enumerate(row):
            if (index, i) in originalIndex:
                print(Fore.BLUE + board[index][i] + " " + Style.RESET_ALL, end="")
            else:
                print(board[index][i] + " ", end="")
        print("")

main()
