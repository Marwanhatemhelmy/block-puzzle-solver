from multiplePuzzlesSolutions import MultiplePuzzlesSolutions
gamePlayMap = [
    [1,1,1,0,0,1,1,0],
    [0,1,1,0,0,1,0,0],
    [0,0,0,0,1,1,1,0],
    [0,0,0,0,1,1,1,1],
    [0,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0],
    [1,1,1,0,1,1,1,0]
]

puzzle0 = [
    [0,1,0],
    [1,1,1]
]
puzzle1 = [
    [1,1,1]
]
puzzle2 = [
    [1,1,1],
    [1,1,1],
    [1,1,1]
]

solutions = MultiplePuzzlesSolutions(gamePlayMap,[puzzle0,puzzle1,puzzle2])
###########################################################################
# return all possible solutions :
print(solutions.returnPosibleSolutions())

###########################################################################
# returns the solutions that vanishes the most rows and/or columns :
print(solutions.returnSolutionWithTheMostBlasts())