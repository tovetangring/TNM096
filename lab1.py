# import random
from queue import PriorityQueue
import datetime

class Node:
  def __init__(self, puzzle, parent):
    if USE_MANHATTAN:
      self.h1 = -(calculate_manhattan(puzzle) - 9)
    else:
      self.h1 = -(calculate_h1(puzzle) - 9)
    self.puzzle = puzzle
    self.parent = parent
    self.depth = 0
    self.cost = self.h1 + self.depth

  def calculate_cost(self):
    self.cost = self.h1 + self.depth

  # To compare nodes
  def __lt__(self, other):
    return self.cost < other.cost
  
  # To print the node
  def __str__(self):
    return "Puzzle: " + self.puzzle + " H1: " + str(-(self.h1-9)) + "(" + str(self.h1) + ")"

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
def print_puzzle(puzzle_to_print):
    for i, tile in enumerate(puzzle_to_print):
        if i % 3 == 0:
            print()
        if tile == "0":
            print("[" + ' ' +  "]", end=" ")
        else:
          print("[" + tile +  "]", end=" ")
    print()

def replace_char(s, i, ch):
  return s[:i] + ch + s[i + 1:]

# Define a function the finds the 0 in the puzzle
def find_zero(puzzle_to_find):
  for index, tile in enumerate(puzzle_to_find):
    if "0" in tile:
      return index

  return None

# region Shift functions

# Define a function that shifts the puzzle in a given direction. Returns a node
def shift(direction, puzzle_to_change):
  coord = find_zero(puzzle_to_change)
  shifted_puzzle = puzzle_to_change
  if coord == None:
    print("ERROR:1 No empty tile found")
    return None
  
  match direction:
    case "up":
      if coord < 3:
        return None
      
      shifted_tile = puzzle_to_change[coord - 3]
      shifted_puzzle = replace_char(shifted_puzzle, coord-3, "0")
  
    case "down":
      if coord > 5:
        return None
      
      shifted_tile = puzzle_to_change[coord + 3]
      shifted_puzzle = replace_char(shifted_puzzle, coord + 3, "0")
    
    case "left":
      if coord % 3 == 0:
        return None
      
      shifted_tile = puzzle_to_change[coord - 1]
      shifted_puzzle = replace_char(shifted_puzzle, coord - 1, "0")
  
    case "right":
      if coord % 3 == 2:
        return None
      
      shifted_tile = puzzle_to_change[coord + 1]
      shifted_puzzle = replace_char(shifted_puzzle, coord + 1, "0")

    case _:
      print("ERROR:2 Invalid direction")
      return None
     
  shifted_puzzle = replace_char(shifted_puzzle, coord, shifted_tile)
  return Node(shifted_puzzle, None)


# endregion
  
#Update h1
def calculate_h1(puzzle_to_check):
  h1 = 0
  # Go through the puzzle and check how many tiles are on the correct position
  for i, tile in enumerate(puzzle_to_check):
    if tile == PUZZLE_GOAL[i]:
      h1 += 1
  return h1

# Calculate Manhattan distance
def calculate_manhattan(puzzle_to_check):
  # Turn the puzzle into a 2D list 
  positions = [[1,1], [2,1], [3,1], [1,2], [2,2], [3,2], [1,3], [2,3], [3,3]]
  h = 0
  # Go through the puzzle and calculate the Manhattan distance for each tile
  for n in puzzle_to_check:
    # Get the index of the current tile in the 2D grid
    index_of_current = puzzle_to_check.index(n)
    state_pos = positions[index_of_current]

    # Get the goal position of the current tile
    if n == "0":
      goal_pos = positions[8]
    else:
      goal_pos = positions[int(n)-1]
    
    # Calculate the Manhattan distance
    y_dist = abs(state_pos[1] - goal_pos[1])
    x_dist = abs(state_pos[0] - goal_pos[0])
    h = h + y_dist + x_dist
  return h

def generate_children(active_node, visited):
  directions = ["up", "down", "left", "right"]
  children = []

  # Generate possible moves from the current node
  for dir in directions:
    child_node = shift(dir, active_node.puzzle)
    if child_node != None:
      child_node.parent = active_node
      child_node.depth = active_node.depth + 1
      child_node.calculate_cost()
      puzzle = child_node.puzzle
      # Check if the child has already been visited,
      # if not, add it to the list of children
      if visited.set_val(puzzle, calculate_h1(puzzle)):
        children.append(child_node)
       
  return children

def a_star_search(start_node, visited):

  print("Starting A* search")
  print("Start node", start_node)
  print_puzzle(start_node.puzzle)

  visited.set_val(start_node.puzzle, start_node.h1)

  #Make priority queue
  q = PriorityQueue()
  q.put(start_node)

  tries = 0
  while tries < MAX_ITERATIONS and not q.empty():
  #Find children for first position in priority queue
    active_node = q.get()

    if active_node.puzzle == PUZZLE_GOAL:
      print("Solution found!")
      return active_node
  
    children = generate_children(active_node, visited)
    for node in children:
      q.put(node)

    tries += 1

    # Progress bar
    if tries % 10000 == 0:
      print("Tries:", tries, "Queue size:", q.qsize())
  print()
  print("No solution found")

# Generate an array with all the nodes in the tree
def generate_tree(node):
  tree = []
  while node != None:
    tree.append(node)
    node = node.parent
  return tree[::-1] 
  

# Define the puzzle and its goal state (empty is represented by 0)
PUZZLE_START = "867254301"
PUZZLE_GOAL  = "123456780"
MAX_ITERATIONS = 1000000  # Set the maximum number of unique children
USE_MANHATTAN = True

#Make already checked list
visited = HashTable()

startTime = datetime.datetime.now()
startNode = Node(PUZZLE_START, None)
endNode = a_star_search(startNode, visited)
endTime = datetime.datetime.now()

tree = generate_tree(endNode)
for node in tree:
  print_puzzle(node.puzzle)

print()
print("Depth:", len(tree) - 1)
print("Time:", (endTime - startTime).total_seconds() * 1000, "ms")