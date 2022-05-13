from contextlib import nullcontext
from math import fabs
import field as Field
import tile
import numpy as np

class Solver:

    def __init__(self,
                    field):
        
        self.field = field
        self.rows = self.field.getRows()
        self.columns = self.field.getColumns()
        self.blocks = self.field.getBlocks()
        self.tileList = self.field.getTileList()
        self.structureTypes = np.array([self.columns, self.rows, self.blocks])
        self.lastField = self.field

    # Scans every structure of a field until it can eliminate more possibilities
    # or until no further improvements can be made.
    # TODO: Consider changing rows, columns and blocks into a separate class.
    def solveField(self):
        iterationCount = 0
        iterationCap = 1000
        solvingIsComplete = False
        solvingIsPossible = True
        while (solvingIsPossible and not solvingIsComplete) and iterationCount < iterationCap:
            for structureType in self.structureTypes:
                for structure in structureType:
                    self.updateStructure(structure)
                    iterationCount += 1
            solvingIsComplete = self.solvingIsComplete()
            if self.changeOccured() or self.informationChangeOccured():
                solvingIsPossible = True
            else:
                solvingIsPossible = False
            print()
            self.field.printField()
            print(solvingIsPossible)
            print(not solvingIsComplete)
            print('xxxxxxxxxxxxxxxxxxxxx')
        print(iterationCount)
            
    # Checks whether all tiles of a field have been assigned a non-zero value
    def solvingIsComplete(self):
        isComplete = True
        for tile in self.tileList:
            if tile.getAssignedValue() == 0:
                isComplete = False
                return isComplete
        return isComplete

    # Returns whether any tiles has recieved a value update.
    # TODO: Code this more efficient.
    def changeOccured(self):
        changeOccured = False
        for identification in self.tileList:
            newTile = self.field.getTile(identification).getAssignedValue()
            oldTile = self.lastField.getTile(identification).getAssignedValue()
            if not newTile == oldTile:
                changeOccured = True
                return changeOccured
        self.lastField = self.field
        return changeOccured

    # Returns whether any tiles recieved any information update.
    def informationChangeOccured(self):
        changeOccured = False
        for identification in range(1, 82):
            newTile = self.field.getTile(identification).getAssignableValues()
            oldTile = self.lastField.getTile(identification).getAssignableValues()
            if not newTile == oldTile:
                changeOccured = True
                return changeOccured
        self.lastField = self.field
        return changeOccured

    # Takes a structure and updates all the information in it.
    def updateStructure2(self,
                            structure):
            for tile in structure:
                assignedValue = tile.getAssignedValue()
                assignableValues = tile.getAssignableValues()
                if assignedValue == 0:
                    continue
                else: 
                    for secondTile in structure:
                        secondAssignedValue = secondTile.getAssignedValue()
                        if not secondAssignedValue == 0:
                            continue
                        else:
                            secondAssignableValues = secondTile.getAssignableValues()
                            if assignedValue in secondAssignableValues:
                                index = np.where(secondAssignableValues == assignedValue)
                                newAssignableValues = np.delete(secondAssignableValues, index)
                                secondTile.updateAssignableValues(newAssignableValues)
            

    # Takes a structure and matches each tile against one another to update them.   
    def updateStructure(self,
                        structure):
        
        for referenceTile in structure:
            for updatedTile in structure:
                self.updateTile(referenceTile, updatedTile)
    
    # Takes a reference tile and a assignableValues list to check against one another.
    def updateTile(self,
                    referenceTile,
                    updatedTile):
        
        if updatedTile.getAssignedValue() == 0:
            referenceValue = referenceTile.getAssignedValue()
            updatedValues = updatedTile.getAssignableValues()
            if referenceValue in updatedValues:
                index = np.where(updatedValues == referenceValue)
                updatedValues = np.delete(updatedValues, index)
                updatedTile.updateAssignableValues(updatedValues)

""" v Salvagable Stuff v

    # Checks if assignable values can be updated.
    def checkConstraints(self,
                            assignableValues):
        # TODO: Implement updating here.
        assignableValues = 0
        return assignableValue
"""