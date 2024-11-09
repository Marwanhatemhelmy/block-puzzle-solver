import itertools
class BlockBlast:
    # enter the raw map where every 1 is an obsticle, and every 0 is a free slot
    def __init__(self, map):
        self.map = map
    # as the name of the function clarifies , this fucntion returns an inverted
    # free-sloted map where every 1 is a free slot and every 0 is an obsticle
    def returnFreeSlotedMap(self,returnFreeRawIndexes=False):
        # result map array
        result = []
        
        resultIndexes = []
        for i in range(len(self.map)):
            # row array is every row inverted into free slots row
            row = []
            # rawFreeSlotsIndexes array is every free slot index in this row
            rawFreeSlotsIndexes = []
            # loop over every slot in the row and check if it's 1 so it gets appended to row array as 0
            # or if it's 0 then it gets appended to row array as 1, and gets appended also to 
            # rawFreeSlotsIndexes array
            for j in range(len(self.map[i])):
                if self.map[i][j]==1:
                    row.append(0)
                else:
                    row.append(1)
                    rawFreeSlotsIndexes.append(j)
            result.append(row)
            if (len(rawFreeSlotsIndexes)==0):
                resultIndexes.append([])
            else:
                resultIndexes.append(rawFreeSlotsIndexes)
        if returnFreeRawIndexes == True:
            return resultIndexes
        # returns free-sloted map array 
        return result


# this clss is to get solution for one puzzle
class Solution:
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
            if not puzzelNotFoundExeption:
                try:
                    self.solutions[tuple(subRows)].append(self.commonElementsInArrays(subCommonColumns))
                except:
                    self.solutions[tuple(subRows)] = self.commonElementsInArrays(subCommonColumns)
        solutionsToDelete = []
        for emptySolution in self.solutions:
            if len(self.solutions[emptySolution])==0:
                solutionsToDelete.append(emptySolution)
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