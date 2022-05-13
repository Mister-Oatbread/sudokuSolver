from tile import Tile
import math
import numpy as np

"""
This class represents a field compiled of 81 tiles that form a sudoku board.
"""

class Field():

    """
    This method is used as the default constructor for a field.
    Parameters:
        knownBlocks: A list containing all the numbers that are known from the sudoku.
    """

    def __init__(self,
                    knownTiles):

        self.blocks = []
        self.columns = []
        self.rows = []

        self.tileList = np.array([])
        self.fieldMatrix = np.zeros(shape = (9, 9))
        self.assignableValues = np.array([])
        self.fillingArray = np.array([])

        self.identificationsOfKnownTiles = np.array([], dtype = np.integer)
        self.valuesOfKnownTiles = np.array([], dtype = np.integer)

        self.initiateArrays()
        self.assignKnownTiles(knownTiles)
        self.initiateTiles()
        self.assignTiles()
        
    # Fill all possible assignable values into the corresponding array.
    def initiateArrays(self):
        for value in range(1, 10):
            value = math.floor(value)
            self.assignableValues = np.append(self.assignableValues, value)
            self.columns.append(self.fillingArray)
            self.rows.append(self.fillingArray)
            self.blocks.append(self.fillingArray)
    
    # Filter information given in knownTiles by splitting into values and positions.
    def assignKnownTiles(self,
                            knownTiles):

        xCoordinateInformation = "xCoordinateInformation"
        yCoordinateInformation = "yCoordinateInformation"
        valueInformation = "valueInformation"
        nextInformation = xCoordinateInformation
        for information in knownTiles:
            if nextInformation == xCoordinateInformation:
                xCoordinate = information
                nextInformation = yCoordinateInformation
            elif nextInformation == yCoordinateInformation:
                yCoordinate = information
                nextInformation = valueInformation
            elif nextInformation == valueInformation:
                if information > 9 or information < 1:
                    raise TypeError("Information is out of bounds")
                else:
                    identification = 10*xCoordinate + yCoordinate
                    self.identificationsOfKnownTiles = np.append(self.identificationsOfKnownTiles, identification)
                    self.valuesOfKnownTiles = np.append(self.valuesOfKnownTiles, information)
                nextInformation = xCoordinateInformation
        self.identificationsOfKnownTiles = self.identificationsOfKnownTiles.astype(np.int64)
        self.valuesOfKnownTiles = self.valuesOfKnownTiles.astype(np.int64)

    # Initiate all tiles with all available information and put them into a list.
    def initiateTiles(self):
        for yCoordinate in range (1, 10):
            for xCoordinate in range (1, 10):
                identification = xCoordinate*10 + yCoordinate
            # TODO: The identification range has been changed starting from 0 instead of 1. Check if this interferes with anything.
                if identification in self.identificationsOfKnownTiles:
                    index = np.where(self.identificationsOfKnownTiles == identification)
                    assignedValueAsArray = self.valuesOfKnownTiles[index]
                    assignedValue = np.asscalar(assignedValueAsArray)
                    assignableValues = np.empty([])
                else:
                    assignedValue = 0
                    assignableValues = self.assignableValues

                newTile = Tile(assignedValue, xCoordinate, yCoordinate, assignableValues, identification)
                self.tileList = np.append(self.tileList, newTile)

    # Assign each tile to a block, row and column
    def assignTiles(self):
        for tile in self.tileList:
            xCoordinate = tile.getXCoordinate()
            yCoordinate = tile.getYCoordinate()

            self.columns[xCoordinate-1] = np.append(self.columns[xCoordinate-1], tile)
            self.rows[yCoordinate-1] = np.append(self.rows[yCoordinate-1], tile)

            transformedXCoordinate = math.ceil(xCoordinate / 3)
            transformedYCoordinate = math.ceil(yCoordinate / 3)
            # TODO: Plug this into a separate method.
            positionInList = (transformedXCoordinate-1) + 3*(transformedYCoordinate-1)
            self.blocks[positionInList] = np.append(self.blocks[positionInList], tile)
        
        self.columns = np.asarray(self.columns, dtype = object)
        self.rows = np.asarray(self.rows, dtype = object)
        self.blocks = np.asarray(self.blocks, dtype = object)


    # Print the matrix that represents the field at a given state.
    def printField(self):
        currentYCoordinate = 1
        print()
        for tile in self.tileList:
            assignedValue = tile.getAssignedValue()
            xCoordinate = tile.getXCoordinate()
            yCoordinate = tile.getYCoordinate()
            if not (yCoordinate == currentYCoordinate):
                print()
                currentYCoordinate = yCoordinate
                if yCoordinate == 4 or yCoordinate == 7:
                    print(" ")
                
            if xCoordinate == 4 or xCoordinate == 7:
                    print(" ", end = ' ')

            print(assignedValue, end = ' ')
        print()
    # TODO: The solution with 'firstIteration' is pretty ugly, solve this in another way.

    # Prints all assignable values for each tile of a field.
    def printAssignableValues(self):
        print()
        for tile in self.tileList:
            assignableValues = tile.getAssignableValues()
            print(tile.getIdentification(), end = ' ')
            print(tile.getXCoordinate(), end = ' ')
            print(tile.getYCoordinate(), end = ' ')
            index = np.where(self.blocks == tile)
            index = np.asscalar(index[0] + 1)
            print(index, end =': ')

            if tile.isAssignable():
                for value in assignableValues:
                    value = np.asscalar(value)
                    print(value, end = ' ')
            print()
        print()
    
    # Prints all tiles wih their x and y coordinates.
    def printCoordinates(self):
        for tile in self.tileList:
            return None

    # Returns the line in which the requested tile is located.
    def getLine(self,
                tile):
        
        line = np.where(tile.getIdentification)
    
    # Returns the tile that corresponds to the specified x and y coordinate.
    def getTile(self,
                xCoordinate,
                yCoordinate):
        identification = self.transformCoordinates(xCoordinate, yCoordinate)
        tile = self.tileList[identification]
        return tile

    # Returns all tiles in an array of a field.
    def getTileList(self):
        return self.tileList

    # Returns the column which contains a given tile.
    # TODO: Change this to be able to process every structure type using structureType.
    def getStructure(self,
                    requestedTile,
                    structureType):
        
        if structureType == 'column':
            structures = self.columns
        elif structureType == 'row':
            structures = self.rows
        elif structureType == 'block':
            structures = self.blocks

        requestedStructure = -1
        for structure in structures:
            for tile in structure:
                if tile == requestedTile:
                    requestedStructure = structure
                    return requestedStructure

    # TODO: Check if this works properly, then extend it to rows and blocks.
    # TODO: Consider if it makes sense to implement this somewhere else, namely tile.

    # Returns all columns of a field.
    def getColumns(self):
        return self.columns
        
    # Returns all rows of a field.
    def getRows(self):
        return self.rows

    # Returns all blocks of a field.
    def getBlocks(self):
        return self.blocks

    # v Salvagable stuffs v
"""
    # This method transforms an identification into a coordinate tuple.
    def transformIdentification(self,
                                identification):

        identification = identification - 1
        xCoordinate = identification % 9
        yCoordinate = math.ceil(identification / 9)
        adjustedXCoordinate = xCoordinate + 1
        adjustedYCoordinate = yCoordinate
        if identification == 1:
            adjustedXCoordinate = 1
            adjustedYCoordinate = 1
        coordinateTuple = np.array([adjustedXCoordinate, adjustedYCoordinate])
        return coordinateTuple

    # This method transforms two coordinates into a identification.
    def transformCoordinates(self,
                                xCoordinate,
                                yCoordinate):
        adjustedXCoordinate = xCoordinate
        adjustedYCoordinate = yCoordinate - 1
        identification = (adjustedXCoordinate + adjustedYCoordinate * 9)
        return identification
    # TODO: The whole identification transformation thing is still a bit weird. Think this through again.

        # Initialize test matrix for temporary testing purposes.
        for i in range(1, 9):
            for j in range(1, 9): 
                fieldMatrix[i][j] = tile(0, i, j, assignableValues)
        
        # Takes a structure array and converts it so that it can be printed cleanly.
        def createPrintableStructure(self,
                                    structure):
            printableArray = np.array([])
            for tile in structure:
                newEntry = tile.getAssignedValue()
                printableArray = np.append(printableArray, newEntry)
            return printableArray


        # Print the matrix that represents the field at a given state. Test version 2.0.
        def printField2(self):
            firstIteration = True
            row = np.array([])
            for tile in self.tileList:
                if firstIteration or tile.getYCoordinate() == lastTile.getYCoordinate():
                    row = np.append(row, tile)
                    lastTile = tile
                else:
                    print(np.array2string(row, separator=', '))
                    #print(' '.join(map(str, row)))
                    row = np.array([])
                        
                firstIteration = False
            

        for rowIndex in range(1, 9):
            for columnIndex in range(1, 9):
                if information in identificationsOfKnownTiles:
                    specificAssignableValues = valuesOfKnownTiles[identificationsOfKnownTiles.index(information)]
                else:
                    specificAssignableValues = assignableValues

                newTile = tile.Tile(0, rowIndex, columnIndex, specificAssignableValues, identification)
                tileList.append(newTile)
                identification+=1
                fieldMatrix.append()
        
        assignBlocksInField()


    This method outsources the assignment from tiles to different blocks that is used in the constructor.
    The blocks are arranged the following way:
        6 7 8
        3 4 5
        0 1 2
    In this implementation however they are arranged in a list.
    
    def assignBlocksInField(self):
        for i in range(1, 9):
            self.blocks[i] = i

        for tile in self.fieldMatrix:
            xCoordinate = math.floor(tile.getXCoordinate/3)
            yCoordinate = tile.getYCoordinate%3
            if xCoordinate>8 or xCoordinate<0 or yCoordinate>8 or yCoordinate<0:
                # Implement normal throws here.
                print('value is out of bounds')
                break
            self.blocks[xCoordinate + 3*yCoordinate].append(tile)



        # Find a way to assign each tile to row, column and block automatically.
        # Not quite sure if this works as intended for now, find that out by testing or something.
        for tile in self.tileList:
            columnIndex = tileList.index(tile) % 9
            columns.index(columnIndex).append(tile)

            rowIndex = math.floor(tileList.index(tile)/9)
            rows.index(rowIndex).append(tile)

            # Block still needs to be done.
"""


"""
This class represents a tile in a sudoku game.
It stores all the information regarding assignability etc. for this
"""