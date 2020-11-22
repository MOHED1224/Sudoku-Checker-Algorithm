import time
import pandas
print("Welcome to Sudoku")
print("Plese Enter Each Row in Puzzel then Press Enter")

board = []

def main():
    for row in range(0, 9):
        board.append(input().replace(" ", "")) #Removes any spaces in rows

    for index, line in enumerate(board):
        board[index] = list(line) #convert each row into list of 9 numbers

    if isCorrect() == True:
        estT = time.time()

        RowChecker()
        ColumnChecker()

        GridNumber = 0

        #Two for loops to loop the 9 sub grids
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                GridNumber += 1
                SquaresChecker(i, j, GridNumber)

        print("Done in ", time.time()-estT, "Seconds")
    else:
        print("Board is incorrect")

def RowChecker():
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

def ColumnChecker():
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


def SquaresChecker(i, j, n):
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


def isCorrect():
    global board
    for row in board:
        if len(row) != 9:
            return False
    return True

main()
