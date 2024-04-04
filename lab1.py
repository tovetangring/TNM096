# import random
from queue import PriorityQueue 

h1 = 0 # Hur många är på rätt ställe
h2 = 0 # Manhattan avstånd till rätt ställe 

# Define the puzzle and its goal state (empty is represented by 0)
PUZZLE_START = "532416078"
PUZZLE_GOAL  = "012345678"

MAX_ITERATIONS = 1000  # Set the maximum number of unique children

class Node:
  def __init__(self, h1, puzzle, parent):
    self.h1 = h1
    self.puzzle = puzzle
    self.parent = parent

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
 
        # If the bucket does not contain a similar key:
        # Append the new key-value pair to the bucket
        if not found_key:
            bucket.append((key, val))

        # Return if the operation was successful
        return not found_key

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
    for i, tile in enumerate(puzzleToPrint):
        if i % 3 == 0:
            print()
        if tile == "0":
            print("[" + ' ' +  "]", end=" ")
        else:
          print("[" + tile +  "]", end=" ")
    print()
    print("-----------")

def replaceChar(s, i, ch):
  return s[:i] + ch + s[i + 1:]

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
    print("ERROR:1 No empty tile found")
    return None
  
  match direction:
    case "up":
      if coord < 3:
        return None
      
      shiftedTile = puzzleToChange[coord - 3]
      shiftedPuzzle = replaceChar(shiftedPuzzle, coord-3, "0")
  
    case "down":
      if coord > 5:
        return None
      
      shiftedTile = puzzleToChange[coord + 3]
      shiftedPuzzle = replaceChar(shiftedPuzzle, coord + 3, "0")
    
    case "left":
      if coord % 3 == 0:
        return None
      
      shiftedTile = puzzleToChange[coord - 1]
      shiftedPuzzle = replaceChar(shiftedPuzzle, coord - 1, "0")
  
    case "right":
      if coord % 3 == 2:
        return None
      
      shiftedTile = puzzleToChange[coord + 1]
      shiftedPuzzle = replaceChar(shiftedPuzzle, coord + 1, "0")

    case _:
      print("ERROR:2 Invalid direction")
      return None
     
  shiftedPuzzle = replaceChar(shiftedPuzzle, coord, shiftedTile)
  printPuzzle(shiftedPuzzle)
  return Node(calculateH1(shiftedPuzzle), shiftedPuzzle, None)


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

def generateChildren(activeNode, visited):
  directions = ["up", "down", "left", "right"]
  children = []

  # Generate possible moves from the current node
  for dir in directions:
    childNode = shift(dir, activeNode.puzzle)
    childNode.parent = activeNode
    if childNode != None:
      puzzle = childNode.puzzle
      # Check if the child has already been visited,
      # if not, add it to the list of children
      if visited.set_val(puzzle, calculateH1(puzzle)):
        children.append(childNode)

  return children

 ###
def aStarSearch(startNode):
  #Make already checked list
  visited = HashTable()
  visited.set_val(startNode.puzzle, startNode.h1)

  #Make priority queue
  q = PriorityQueue()
  q.put(startNode.h1, startNode)

  tries = 0
  while tries < MAX_ITERATIONS and not q.empty():
  #Find children for first position in priority queue
    activeNode = q.get()
    if activeNode.puzzle == PUZZLE_GOAL:
      return
    
    children = generateChildren(activeNode, visited)
    for node in children:
      q.put(node.h1, node)

    tries += 1
  

startNode = Node(0, PUZZLE_START, None)
aStarSearch(startNode)