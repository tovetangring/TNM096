# import random
from queue import PriorityQueue 

h1 = 0 # Hur många är på rätt ställe
h2 = 0 # Manhattan avstånd till rätt ställe 

# Define the puzzle and its goal state (empty is represented by 0)
PUZZLE_START = "532416078"
PUZZLE_GOAL  = "012345678"

MAX_ITERATIONS = 1000  # Set the maximum number of unique children

class Node:
  def __init__(self, h1, puzzle):
    self.h1 = h1
    self.puzzle = puzzle

class HashTable:
    # Create empty bucket list of given size
    def __init__(self):
        self.size = MAX_ITERATIONS
        self.hash_table = self.create_buckets()
 
    def create_buckets(self):
        return [[] for _ in range(self.size)]
    
    # Insert values into hash map
    def set_val(self, key, val):
       
        # Get the index from the key
        # using hash function
        hashed_key = hash(key) % self.size
         
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
             
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break
 
        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key:
            print("Error: Key already exists")
        else:
            bucket.append((key, val))

    # Remove a value with specific key
    def delete_val(self, key):
       
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
         
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
             
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break
 
        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key: bucket.pop(index)
        return
    
    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)
    


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
  for index, tile in enumerate(puzzleToFind):
    if "0" in tile:
      return index

  return None

# region Shift functions

# Define a function that shifts the puzzle in a given direction. Returns a node
def shift(direction, puzzleToChange):
  coord = findZero(puzzleToChange)
  print(type(coord))
  shiftedPuzzle = puzzleToChange
  if coord == None:
    print("ERROR: No empty tile found")
    return None
  
  match direction:
    case "up":
      if coord < 3:
        print("ERROR: Cannot shift up")
        return None
      
      shiftedTile = puzzleToChange[coord - 3]
      shiftedPuzzle[coord - 3] = "0"
  
    case "down":
      if coord > 5:
        print("ERROR: Cannot shift down")
        return None
      
      shiftedTile = puzzleToChange[coord[0] + 3]
      shiftedPuzzle[coord[0] + 3] = "0"
    
    case "left":
      if coord % 3 == 0:
        print("ERROR: Cannot shift left")
        return None
      
      shiftedTile = puzzleToChange[coord[0] - 1]
      shiftedPuzzle[coord[0] - 1] = "0"
  
    case "right":
      if coord % 3 == 2:
        print("ERROR: Cannot shift right")
        return None
      
      shiftedTile = puzzleToChange[coord[0] + 1]
      shiftedPuzzle[coord[0] + 1] = "0"

    case _:
      print("ERROR: Invalid direction")
      return None
     
  shiftedPuzzle[coord] = shiftedTile
  printPuzzle(shiftedPuzzle)
  return Node(calculateH1(shiftedPuzzle), shiftedPuzzle)


# endregion

#####################     A* SEARCH      ############################
  
#Update h1
def calculateH1(puzzleToCheck):
  h1 = 0
  # Go through the puzzle and check how many tiles are on the correct position
  for tile in puzzleToCheck:
    if tile == PUZZLE_GOAL:
      h1 += 1
  return h1

def generateChildren(activeNode):
  directions = ["up", "down", "left", "right"]

  for dir in directions:
    childNode = shift(dir, activeNode.puzzle)
    if childNode != None:
      activeNode.children.append(childNode) # Byt?

 ###
def aStarSearch(startNode, puzzle):
  #Make aldready checked list
  #Make priority queue
  q = PriorityQueue()
  children = generateChildren(startNode)
  q.put((calculateH1(puzzle), startNode))

  #Find children for first position in priority queue

  #Check if the solution is any of the children
  
  #Place children in priority queue (and it will automatically sort them) and remove parent
  pass
  
visited = HashTable()
print(visited)
visited.set_val(PUZZLE_START, 0)
print(visited)
print()
visited.set_val(PUZZLE_GOAL, 9)
print(visited)
print()
visited.set_val(PUZZLE_START, 0)
print(visited)
print()
visited.delete_val(PUZZLE_START)
print(visited)
print()
visited.delete_val(PUZZLE_START)
print(visited)

# Try the shift functions
printPuzzle(PUZZLE_START)
shift("up", PUZZLE_START)
shift("down", PUZZLE_START)
shift("left", PUZZLE_START)
shift("right", PUZZLE_START)


tries = 0
solved = False
startNode = Node(0, PUZZLE_START)
# while not solved and tries < MAX_ITERATIONS:
#   solved = aStarSearch(startNode)
#   tries += 1