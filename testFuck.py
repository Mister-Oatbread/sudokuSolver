from field import Field
from solver import Solver
from tile import Tile
import numpy as np

testList = np.array([7, 1, 25, 4, 64, 7, 19, 5, 71, 6, 4, 5])
testList2 = np.array([5, 5, 3, 1, 9, 5, 3, 7, 1])
testList3 = np.array([2, 1, 3,
                        4, 2, 1,
                        5, 2, 9,
                        6, 2, 5,
                        3, 3, 8,
                        8, 3, 6,
                        1, 4, 8,
                        5, 4, 6,
                        1, 5, 4,
                        4, 5, 8,
                        9, 5, 1,
                        5, 6, 2,
                        2, 7, 6,
                        7, 7, 2,
                        8, 7, 8,
                        4, 8, 4,
                        5, 8, 1,
                        6, 8, 9,
                        9, 8, 5,
                        8, 9, 7])

testField = Field(testList3)
testField.printField()
print()

testSolver = Solver(testField)

testSolver.solveField()
testField.printField()
testField.printAssignableValues()
testField.printField()

# TODO: Change the entries for assignableValues from floats to integers.
# TODO: The stopping method that measures changes in the field doesn't work properly. Fix it.
# TODO: Add tile method to get tile by identification.