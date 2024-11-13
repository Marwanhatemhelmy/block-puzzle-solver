from puzzleAbstract import PuzzleAbstractMethods

# this clss is to get solution for one puzzle
class OnePuzzleSolutions(PuzzleAbstractMethods):
    # enter the free-sloted map wich you get from blockblast class, and the puzzle witch you make
    # the puzzle has some requirements to be valid puzzle
    # 1st requirement:
    #   each row and column need to be the same size
    # 2nd requirement:
    #   each slot witch is not a part from the puzzle need to be 0
    def __init__(self,freeSlotsMap,puzzel):
        self.freeSlotsMap = freeSlotsMap
        self.puzzel = puzzel
        self.avaliableRows = {}
        self.update()

    # update function is to loop over the puzzle's rows and free-sloted map rows
    # and checks if every row in puzzle is in witch row in the free-sloted
    # and the columns in the free-sloted map that matches the columns of puzzle
    # usually it's not needed to be called but in case it's needed it's there 
    def update(self):
        for i in range(len(self.puzzel)):
            for j in range(len(self.freeSlotsMap)):
                # avaliable indexes in this row of free-sloted map that are suitable for this puzzle row
                arrAvaliableIndexes = self.findPuzzleRowInMapRow(self.freeSlotsMap[j],self.puzzel[i])
                if len(arrAvaliableIndexes)!=0:
                    try:
                        self.avaliableRows[j][i]=arrAvaliableIndexes
                    except:
                        self.avaliableRows[j] = {i:arrAvaliableIndexes}
        
        self.avaliableRowsIndexes = []
        self.avaliableRowsKeys = sorted(list(self.avaliableRows.keys()))
        for i1 in range(len(self.avaliableRowsKeys)):
            subArr = self.avaliableRowsKeys[i1:(i1+(len(self.puzzel)))]
            checkToAppendSubArray = True
            for j1 in range(len(subArr)):
                if j1!=0:
                    if (subArr[j1]-1) not in subArr:
                        checkToAppendSubArray=False
                        break

            if checkToAppendSubArray and len(subArr)==len(self.puzzel):
                self.avaliableRowsIndexes.append(self.avaliableRowsKeys[i1:(i1+(len(self.puzzel)))])
        self.solutions = {}
        puzzelNotFoundExeption=False

        for e in self.avaliableRowsIndexes:
            puzzelNotFoundExeption=False
            subCommonColumns = []
            subRows = []
            for se in range(len(e)):
                subRows.append(e[se])
                try:
                    subCommonColumns.append(self.avaliableRows[e[se]][se])
                except:
                    puzzelNotFoundExeption=True
            # checks if it's a valid solution to be added as solution
            if not puzzelNotFoundExeption:
                try:
                    self.solutions[tuple(subRows)].append(self.commonElementsInArrays(subCommonColumns))
                except:
                    self.solutions[tuple(subRows)] = self.commonElementsInArrays(subCommonColumns)
        
        solutionsToDelete = []
        # loop over solutions and check if this solution is empty so that it gets deleted later
        for emptySolution in self.solutions:
            if len(self.solutions[emptySolution])==0:
                solutionsToDelete.append(emptySolution)
        
        # deleting empty solutions
        for d in solutionsToDelete:
            self.solutions.pop(d)
    
    
    # this function if a boolean function witch checks if this puzzle row, e.g (puzzle[i]), is in
    # this free-sloted map row, e.g (freeSlotedMap[j]) so then it returns true otherwise it will
    # return false
    def isPuzzleRowInMapRow(self,mapSubArr,Arr):
        for i in range(len(mapSubArr)):
            if Arr[i]==1:
                if mapSubArr[i]!=1:
                    return False
        return True

    # this function return the beging indexes in this free-sloted map row witch 
    # from this index to index+(len(puzzle row)-1) == puzzle row
    def findPuzzleRowInMapRow(self,mapArr,arr):
        begingIndexes = []
        for i in range(len(mapArr)):
            if len(mapArr[i:i+len(arr)])==len(arr):
                if self.isPuzzleRowInMapRow(mapArr[i:i+len(arr)],arr):
                    begingIndexes.append(i)
        return begingIndexes
        
    # returns valid solutions for this puzzle
    #                             rows  columns
    #                              \/     \/ 
    # result will be for example {{(0,1):[0,1,2]}, (1,2):[6,5]}
    #                             |first        | |second    |
    #                                  solutions|   solutions|
    def returnSolutions(self):
        return self.solutions

    # returns the number of valid solutions for this puzzle 
    def returnNumberOfSolutions(self):
        result = 0
        for i in self.solutions:
            result+=len(self.solutions[i])
        return result
    
    # returns common elements in nested array
    # examle [[1,2,3],[0,4,2],[1,2,4]] , result will be [2], because 2 is the only element in every array
    def commonElementsInArrays(self,arrs):
        commonElements = {}
        result = []
        for i in arrs:
            for j in i:
                try:
                    commonElements[j]+=1
                except:
                    commonElements[j]=1
        for e in commonElements:        
            if commonElements[e]>=len(arrs):
                result.append(e)
        return result
    
    # *abstract function
    # this function return an expanded form of solution for this puzzle in the combination of puzzles
    # for example solution for a certain puzzle would be like this {(0,1):[1,2,3],(1,2):[4,5,7]}
    # a formulated solution will transform this standered solution into something like this:
    # {(0,1):1,(0,1):2,(0,1):3,(1,2):4,(1,2):5,(1,2):7}
    def returnFormulatedSolutionsData(self,puzzleSolutions):
        result = []
        for i in puzzleSolutions:
            for j in puzzleSolutions[i]:
                result.append([i,j])
        return result