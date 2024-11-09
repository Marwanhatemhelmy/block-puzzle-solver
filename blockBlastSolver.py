from iso import BlockBlast,Solution
import itertools
from copy import deepcopy


# this class if for multiple puzzles as it's name interprut
class solutionForMultiplePuzzles:
    # like solution class this class has the same essential parameters like the free-sloted map
    # the diffrence is that there is a nested array parameter with multiple puzzles
    def __init__(self,freeSlotedMap,puzzles):
        self.freeSlotedMap = freeSlotedMap
        self.spairFreeSlotedMap = deepcopy(freeSlotedMap)
        self.puzzles = puzzles

    def returnPosibleSolutions(self):
        puzzleCombination = self.returnPermutaionsOfArray(list(range(len(self.puzzles))))
        result = {}
        for i in range(len(puzzleCombination)):
            thisCombination = puzzleCombination[i]
            self.freeSlotedMap = deepcopy(self.spairFreeSlotedMap)
            self.recursiveApproach(thisCombination,0,result)
        return result

    def recursiveApproach(self,thisComb,combId,result,position=None,movments=None):
        if position == None:
            position = {}
        if movments == None:
            movments = {}

        thisPuzzleIndex = thisComb[combId]
        thisPuzzle = self.puzzles[thisComb[combId]]

        sol = Solution(self.freeSlotedMap, thisPuzzle)
        si = 0
        while si < sol.returnNumberOfSolutions():
            movments[thisPuzzleIndex] = si
            formSolutions = self.returnFormulatedSolutionsData(sol.returnSolutions(), thisPuzzleIndex)
            thisMovePosition = list(formSolutions[si].values())[0]
            
            self.placeBlock(thisMovePosition, thisPuzzle)
            self.freeSlotedMap = deepcopy(self.spairFreeSlotedMap)
            allowedCombination = True
            j = 0
            while j <= combId:
                thisPuzzleSpair = self.puzzles[thisComb[j]]
                solSpair = Solution(self.freeSlotedMap, thisPuzzleSpair)

                formSolutionsSpair = self.returnFormulatedSolutionsData(solSpair.returnSolutions(), thisComb[j])
                if len(formSolutionsSpair)==0:
                    allowedCombination = False
                    break
                if movments[thisComb[j]]>(len(formSolutionsSpair)-1):
                    allowedCombination = False
                    break
                thisMovePositionSpair = list(formSolutionsSpair[movments[thisComb[j]]].values())[0]
                thisMovePuzzleKey = list(formSolutionsSpair[movments[thisComb[j]]].keys())[0]

                self.placeBlock(thisMovePositionSpair, thisPuzzleSpair)
                j+=1
            if allowedCombination == False:
                position = {}
                break
            position[thisPuzzleIndex] = thisMovePosition
            if combId == (len(thisComb)-1):
                try:
                    result[self.returnNumberOfFreeSlots()].append(deepcopy(position))
                except:
                    result[self.returnNumberOfFreeSlots()] = [deepcopy(position)]
                pass
            else:
                self.recursiveApproach(thisComb,combId=combId+1,result=result,position=position,movments=movments)

            si+=1


    def returnSolutionWithTheMostBlasts(self):
        return self.bestSolutions()[max(list(self.bestSolutions().keys()))]

    def returnNumberOfFreeSlots(self):
        result = 0
        for i in range(len(self.freeSlotedMap)):
            row = self.freeSlotedMap[i]
            for j in row:
                if j == 1:
                    result+=1
        return result

    def blastMap(self):
        mapBlock = self.freeSlotedMap
        rowCount = {}
        columnCount = {}
        for i in range(len(mapBlock)):
            rowCount[i] = mapBlock[i].count(0)
            for j in range(len(mapBlock[i])):
                if mapBlock[i][j]==0:
                    try:
                        columnCount[j]+=1
                    except:
                        columnCount[j]=1
        rowsCountsToDelete = []
        columnsCountsToDelete = []
        for r in rowCount:
            if rowCount[r]!=len(mapBlock[0]):
                rowsCountsToDelete.append(r)
        for c in columnCount:
            if columnCount[c]!=len(mapBlock):
                columnsCountsToDelete.append(c)
        for dr in rowsCountsToDelete:
            rowCount.pop(dr)
        for dc in columnsCountsToDelete:
            columnCount.pop(dc)
        for i1 in range(len(mapBlock)):
            for j1 in range(len(mapBlock[i1])):
                if i1 in rowCount.keys():
                    mapBlock[i1][j1] = 1
                if j1 in columnCount.keys():
                    mapBlock[i1][j1] = 1

    def placeBlock(self,position,puzzel):
        
        rows = list(position[0])
        cloumns = position[1]
        puzzelIndex = 0
        for i in range(len(self.freeSlotedMap)):
            if i in rows:
                row = self.freeSlotedMap[i][cloumns:cloumns+len(puzzel[0])]
                for y in range(len(row)):
                    if row[y]==1 and puzzel[puzzelIndex][y]!=0:
                        row[y]=0
                #print(self.freeSlotedMap[i][cloumns:len(puzzel[0])],row)
                self.freeSlotedMap[i][cloumns:cloumns+len(puzzel[0])]=row
                puzzelIndex+=1
        self.blastMap()

    def returnFormulatedSolutionsData(self,puzzleSolutions,index):
        result = []
        for i in puzzleSolutions:
            for j in puzzleSolutions[i]:
                result.append({index:[i,j]})
        return result

    def returnCombinations(self,formulatedSolutionsData):
        results = []
        combinations = list(itertools.product(*formulatedSolutionsData))

        for comb in combinations:
            l = list(itertools.permutations(comb))
            for i in range(len(l)):
                l[i] = list(l[i])
            results += l
        return results
    # this function returns all permutaions of an array
    def returnPermutaionsOfArray(self,arr):
        result = []
        for p in itertools.permutations(arr):
            result.append(list(p))
        return result
