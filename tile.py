import numpy as np

"""
This class represents a tile in a sudoku game.
It stores all the information regarding assignability etc. for this
"""

class Tile():

    """
    This method serves as a default constructor for a tile.
    """
    def __init__(self,
                    assignedValue,
                    locationX,
                    locationY,
                    assignableValues,
                    identification):

        self.assignedValue = assignedValue
        self.location = [locationX, locationY]
        self.assignableValues = assignableValues
        self.identification = identification
        if self.assignedValue == 0:
            self.canBeAssigned = True
        else:
            self.canBeAssigned = False

    """
    This method returns the x coordinate of a tile in its field matrix.
    Admissible values range from 0 to 8.
    """
    def getXCoordinate(self):
        return self.location[0]
    
    """
    This method returns the y coordinate of a tile in its field matrix.
    Admissible values range from 0 to 8.
    """
    def getYCoordinate(self):
        return self.location[1]

    # Returns the value that is currently assigned to the tile or 0 if there isn't any value assigned yet.
    def getAssignedValue(self):
        return self.assignedValue
    
    # Allows to assign a value to a tile. Can only be performed once per tile.
    def setAssignedValue(self,
                            value):
        if self.canBeAssigned:
            self.assignedValue = value
            self.canBeAssigned = False
        else:
            print('This tile has already been assigned another value!!!')
            # TODO: Implement a proper exception throw here.


    # Returns the values that can be assigned to a given tile.
    def getAssignableValues(self):
        return self.assignableValues
    
    # Takes a new array to update assignableValues
    def updateAssignableValues(self,
                                updatedValues):

        if self.assignedValue == 0:
            self.assignableValues = updatedValues
            if np.size(updatedValues) == 1:
                updatedValuesAsArray = updatedValues[0]
                valueToAssign = np.asscalar(updatedValuesAsArray)
                self.setAssignedValue(valueToAssign)
        else:
            print('This tile has already been assigned a value!!!')

    # Returns the indentification according to the enumeration of all tiles.
    def getIdentification(self):
        return self.identification

    # Returns whether a tile is already defined or still has to be assigned.
    def isAssignable(self):
        return self.canBeAssigned