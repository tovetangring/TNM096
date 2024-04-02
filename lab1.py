import random

h1 = 0 # Hur många är på rätt ställe
h2 = 0 # Manhattan avstånd till rätt ställe

# Define the puzzle and its goal state (empty is represented by 0)
PUZZLE_START = [[5, 3, 2], [4, 1, 6], [0, 7, 8]]
PUZZLE_GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

class Node:
  def __init__(self, h1, puzzle, children, visited):
    self.h1 = h1
    self.puzzle = puzzle
    self.children = children
    self.visited = visited

# #Shuffles the puzzle
# flattened_puzzle = [item for sublist in puzzle for item in sublist]
# random.shuffle(flattened_puzzle)
# def to_2d_list(flat_list, row_length):
#     return [flat_list[i:i + row_length] for i in range(0, len(flat_list), row_length)]
# puzzle = to_2d_list(flattened_puzzle, len(puzzle[0]))

# Define a function that prints the puzzle in a readable format
def printPuzzle(puzzleToPrint):
  for i, row in enumerate(puzzleToPrint):
    for j, value in enumerate(row):
      if value == 0:
        print("[" + ' ' +  "]", end=" ")
      else:
        print([value], end=" ")
    print()
  print("-----------")

# Define a function the finds the 0 in the puzzle
def findZero(puzzleToFind):
  for i, row in enumerate(puzzleToFind):
      for j, value in enumerate(row):
          if value == 0:
              return (i, j)
  return None

# region Shift functions

# Define a function that shifts the puzzle in a given direction. Returns a node
def shift(direction,puzzleToChange):
  coord = findZero(puzzleToChange)
  shiftedPuzzle = puzzleToChange
  shiftedTile = None
  if coord == None:
    print("ERROR: No empty tile found")
    return None
  
  match direction:
    case "up":
      if coord[0] == 0:
        print("ERROR: Cannot shift up")
        return None
      
      shiftedTile = puzzleToChange[coord[0] - 1][coord[1]]
      shiftedPuzzle[coord[0] - 1][coord[1]] = 0
  
    case "down":
      if coord[0] == 2:
        print("ERROR: Cannot shift down")
        return None
      
      shiftedTile = puzzleToChange[coord[0] + 1][coord[1]]
      shiftedPuzzle[coord[0] + 1][coord[1]] = 0
    
    case "left":
      if coord[1] == 0:
        print("ERROR: Cannot shift left")
        return None
      
      shiftedTile = puzzleToChange[coord[0]][coord[1] - 1]
      shiftedPuzzle[coord[0]][coord[1] - 1] = 0
  
    case "right":
      if coord[1] == 2:
        print("ERROR: Cannot shift right")
        return None
      
      shiftedTile = puzzleToChange[coord[0]][coord[1] + 1]
      shiftedPuzzle[coord[0]][coord[1] + 1] = 0
  
  if shiftedTile == None:
    print("ERROR: Invalid direction")
    return None
  else:
    shiftedPuzzle[coord[0]][coord[1]] = shiftedTile
    printPuzzle(shiftedPuzzle)
    return Node(calculateH1(shiftedPuzzle), shiftedPuzzle, [], False)


# endregion

#####################     A* SEARCH      ############################
  
#update h1
def calculateH1(puzzleToCheck):
  h1 = 0
  for i, row in enumerate(puzzleToCheck):
      for j, value in enumerate(row):
          if value == PUZZLE_GOAL[i][j]:
              h1 += 1
  return h1

def generateChildren(activeNode):
  directions = ["up", "down", "left", "right"]

  for dir in directions:
    childNode = shift(dir, activeNode.puzzle)
    if childNode != None:
      activeNode.children.append(childNode)

 ###
def aStarSearch(startNode):

 #Make priority queue

  #Find children for first position in priority queue

  #Check if the solution is any of the children
  
  #Place children in priority queue (and it will automatically sort them) and remove parent

LIMIT = 1000
tries = 0
solved = False
startNode = Node(0, PUZZLE_START, [], True)
while not solved and tries < LIMIT:
  solved = aStarSearch(startNode)
  tries += 1