from mapManager import MapManager
from onePuzzleSolutions import OnePuzzleSolutions
from mapAbstract import MapAbstractMethods
from copy import deepcopy
import itertools

# this class if for multiple puzzles as it's name interprut
# MapManager class is inherited to easen it for the developers , so that
# they could pass the original map directly rather than passing the free-sloted map
class MultiplePuzzlesSolutions(MapManager,MapAbstractMethods):
    # the following parameters are essantial for the code to work properly
    # 1 - the original map parameter where 1s are obsticles and 0s are free slots
    # 2 - the puzzles parameter is a nested array with the puzzles
    def __init__(self,map,puzzles):
        super().__init__(map)
        self.freeSlotedMap = self.returnFreeSlotedMap()
        self.spairFreeSlotedMap = deepcopy(self.returnFreeSlotedMap())
        self.puzzles = puzzles

    # the following function's role is to return all possible solution with all possible sequences
    def returnPosibleSolutions(self):
        # as we have multiple puzzles , player could start with any puzzle and end with any puzzle
        # and countinue with any sequence , so we need to get all the possible permutaions.
        # example [puzzle0,puzzle1,puzzle2] , [puzzle2,puzzle0,puzzle1] , etc...
        puzzlesCombinations = self.__returnPermutaionsOfArray(list(range(len(self.puzzles))))
        result = {}
        # loops over each combination of puzzles
        for i in range(len(puzzlesCombinations)):
            thisCombination = puzzlesCombinations[i]
            # deepcoping the spair free-sloted map after each iteration
            self.freeSlotedMap = deepcopy(self.spairFreeSlotedMap)
            # this recursive function loops over each combination of solution for this 
            # combination of puzzles & checks if it is valid or not , if it's not valid it breaks
            # otherwise it will continue looping
            self.__recursivePuzzlesCombinationLoop(thisCombination,0,result)
        return result
    

    # this recursive function loops over each combination of puzzle indexes e.g ([0,1,2])
    # and tries every valid combination of solutions among the puzzles
    # this is because every self.puzzles[i] has multiple solutions so we need to make sure we tried all
    # possible combination of solutions
    # example : puzzle0 has [0,1] solutions and, puzzle1 has also [0,1] solution
    # so we need to try them all combined , and the result should look something like this:
    # [puzzle0[0],puzzle1[1]]
    def __recursivePuzzlesCombinationLoop(self,thisCombination,combinationIndex,result,
                          thisCombinationSubSolution=None,movments=None):
        
        # if it's the first loop
        if thisCombinationSubSolution == None:
            thisCombinationSubSolution = {}
        if movments == None:
            movments = {}

        #                    puzzles indexes 
        #                           \/
        # e.g (thisCombination = [1,0,2]) , combinationIndex is the index of current iteration
        # but thisPuzzleIndex is the thisCombination[combinationIndex] whitch is the element itself
        # not it's index & the element itself is an index of a puzzle in self.puzzles
        thisPuzzleIndex = thisCombination[combinationIndex]
        thisPuzzle = self.puzzles[thisCombination[combinationIndex]]

        sol = OnePuzzleSolutions(self.freeSlotedMap, thisPuzzle)
        i = 0
        while i < sol.returnNumberOfSolutions():
            # we need to store the index of solution and the index of puzzle to check after all
            # puzzles are put together if it's still valid
            # because every puzzle could be valid alone but when other puzzles are put
            # it might not still be a valid solution unless it's put in a certain sequence of 
            # solutions.

            movments[thisPuzzleIndex] = i
            formSolutions = self.returnFormulatedSolutionsData(sol.returnSolutions(), thisPuzzleIndex)
            thisMovePosition = list(formSolutions[i].values())[0]
            
            self.__placeBlock(thisMovePosition, thisPuzzle)
            self.freeSlotedMap = deepcopy(self.spairFreeSlotedMap)
            allowedCombination = True
            j = 0

            # now we will loop over past solutions and put them in this sequence and if they are not
            # valid then the loop will break otherwise it will continue with other combinations
            # of solution until it finishes this puzzle combination then it will jump to
            # another combination of puzzles
            while j <= combinationIndex:
                thisSubPuzzle = self.puzzles[thisCombination[j]]
                thisSubPuzzleSolutions = OnePuzzleSolutions(self.freeSlotedMap, thisSubPuzzle)

                thisSubPuzzleFormSolutions = self.returnFormulatedSolutionsData(thisSubPuzzleSolutions.returnSolutions(), thisCombination[j])
                if len(thisSubPuzzleFormSolutions)==0:
                    allowedCombination = False
                    break
                if movments[thisCombination[j]]>(len(thisSubPuzzleFormSolutions)-1):
                    allowedCombination = False
                    break
                thisSubMovePosition = list(thisSubPuzzleFormSolutions[movments[thisCombination[j]]].values())[0]

                self.__placeBlock(thisSubMovePosition, thisSubPuzzle)
                j+=1
            
            # check if it's not allowed combination of solutions so that it breaks the loop
            if allowedCombination == False:
                thisCombinationSubSolution = {}
                break

            # otherwise it will be added to thisCombinationSubSolution with thisPuzzleIndex as key
            # and thisMovePosition as value
            thisCombinationSubSolution[thisPuzzleIndex] = thisMovePosition

            # checks if it's last puzzle in this combination of puzzles so that this solution is added
            # to result other wise it will recur
            if combinationIndex == (len(thisCombination)-1):
                try:
                    result[self.returnNumberOfFreeSlots()].append(deepcopy(thisCombinationSubSolution))
                except:
                    result[self.returnNumberOfFreeSlots()] = [deepcopy(thisCombinationSubSolution)]
            else:
                self.__recursivePuzzlesCombinationLoop(thisCombination,combinationIndex=combinationIndex+1,result=result,thisCombinationSubSolution=thisCombinationSubSolution,movments=movments)

            i+=1

    # this function returns the solution with most number of vanished rows or/and columns.
    def returnSolutionsWithTheMostBlasts(self):
        return self.returnPosibleSolutions()[max(list(self.returnPosibleSolutions().keys()))]

    # *abstract function
    # this function returns the number of free slots in the map at the moment
    def returnNumberOfFreeSlots(self):
        result = 0
        for i in range(len(self.freeSlotedMap)):
            row = self.freeSlotedMap[i]
            for j in row:
                if j == 1:
                    result+=1
        return result

    # *abstract function
    # this function blasts the map or in other words in vanishes the completed rows & columns
    def blastMap(self):
        mapBlock = self.freeSlotedMap
        # row count is every row with the number of 0s in it or obsticles & the same goes with column count.
        rowCount = {}
        columnCount = {}
        # nested loop over map rows and each element in it 
        # (think of each element's index in row as the index of the column)
        for i in range(len(mapBlock)):
            rowCount[i] = mapBlock[i].count(0)
            for j in range(len(mapBlock[i])):
                # checking if element is an obsticle so that it's adde to column count[j]
                if mapBlock[i][j]==0:
                    try:
                        columnCount[j]+=1
                    except:
                        columnCount[j]=1
        # rowsCountsToDelete is the rows that is not completed yet and also the same goes with columnsCountsToDelete
        rowsCountsToDelete = []
        columnsCountsToDelete = []
        for r in rowCount:
            # note the length of any map row e.g (mapBlock[0],mapBlock[1],...) is the lenght needed
            # for any row to be complete and eraised , so if length of row 0 was not equal to 
            # rowCount[r] then it will be appended to rowsCountsToDelete array
            if rowCount[r]!=len(mapBlock[0]):
                rowsCountsToDelete.append(r)
        for c in columnCount:
            # as said with rows the same goes with columns but with some modifications, as the 
            # length of the map is the length needed for a column to be erasied, so if 
            # length of map was not equal to columnCount[c] then it will be appended to
            # columnsCountsToDelete array
            if columnCount[c]!=len(mapBlock):
                columnsCountsToDelete.append(c)
        # delete every index in rowsCountsToDelete & columnsCountsToDelete arraies
        for dr in rowsCountsToDelete:
            rowCount.pop(dr)
        for dc in columnsCountsToDelete:
            columnCount.pop(dc)
        # change every element in free-sloted map if the index of this element was found in rowCount keys
        # or column count keys
        for i1 in range(len(mapBlock)):
            for j1 in range(len(mapBlock[i1])):
                if i1 in rowCount.keys():
                    mapBlock[i1][j1] = 1
                if j1 in columnCount.keys():
                    mapBlock[i1][j1] = 1

    # passed position parameter should be in the following form [(rows),column] e.g [(0,1):1]
    def __placeBlock(self,position,puzzel):
        
        rows = list(position[0])
        cloumn = position[1]
        puzzleRowIndex = 0
        for i in range(len(self.freeSlotedMap)):
            # looping over every row then checks if this row is in rows of position parameter
            if i in rows:
                # subRow is part of the actual row whitch takes from the index of column to column + length 
                # of any row in puzzle , let that puzzle's row index be 0
                subRow = self.freeSlotedMap[i][cloumn:cloumn+len(puzzel[0])]
                # loop over each element in subRow & check if this element is 1 and puzzle[puzzleRowIndex][y]!=0
                # because if puzzle[puzzleRowIndex][y]==0 it doesn't mean any thing because
                # 0 in the puzzle is not a part of the puzzle , it's just a Supplement to the row
                for y in range(len(subRow)):
                    if subRow[y]==1 and puzzel[puzzleRowIndex][y]!=0:
                        subRow[y]=0
                # changing the actual row in the free-sloted map
                self.freeSlotedMap[i][cloumn:cloumn+len(puzzel[0])]=subRow
                # increment puzzle row index counter
                puzzleRowIndex+=1
        # blast the map , or vanish the completed rows and columns
        self.blastMap()

    # this function return an expanded form of solution for this puzzle in the combination of puzzles
    # for example solution for a certain puzzle would be like this {(0,1):[1,2,3],(1,2):[4,5,7]}
    # a formulated solution will transform this standered solution into something like this:
    # {(0,1):1,(0,1):2,(0,1):3,(1,2):4,(1,2):5,(1,2):7}
    def returnFormulatedSolutionsData(self,puzzleSolutions,index):
        result = []
        for i in puzzleSolutions:
            for j in puzzleSolutions[i]:
                result.append({index:[i,j]})
        return result

    # returns all permutaions among all arrays in nested array
    def __returnPermutaionsOfArray(self,arr):
        result = []
        for p in itertools.permutations(arr):
            result.append(list(p))
        return result
