from mapAbstract import MapAbstractMethods

class MapManager(MapAbstractMethods):
    # enter the raw map where every 1 is an obsticle, and every 0 is a free slot
    def __init__(self, map):
        self.map = map
        self.freeSlotedMap = None
        self.returnFreeSlotedMap()

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
        

        self.freeSlotedMap = result
        self.blastMap()
        # returns free-sloted map array 
        return self.freeSlotedMap
    
    # *abstract function
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