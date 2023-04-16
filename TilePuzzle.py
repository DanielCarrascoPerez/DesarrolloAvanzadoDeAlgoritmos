#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import heapq
import random
import time
import sys

class TilePuzzle(object):
    """ Instances of this class represent states in the tile puzzle """
    
    def __init__(self, grid, n, hole, reference_grid):
        """ Private method, do not use it directly. Use the factory method instead
            Create a new puzzle with the parameter values """
        self.grid = grid
        self.n = n
        # Cached values for performance purposes
        self.reference_grid = reference_grid
        self.hole = hole
        self.distance_to_solve = self.compute_distance_to_solve()
        # Instances of this class serve to store a state-space tree
        self.travelled = 0 # Movements already performed to reach this state
        self.step = None # Step that leads to this state
        self.prev_state = None # Previous state in the state-space tree
        self.candidatos = []       
        self.allsteps = []
         
    def __str__(self):
        """ Friendly description of the object """
        return str(self.grid)
    
    def __lt__(self, other):
        """ Compare the cost of two puzzle states """
        return self.cost() < other.cost()
    
    def compute_distance_to_solve(self):
        """ Compute the distance to the solution 
            i.e., the number of non-hole misplaced tiles  """
        diff = self.grid != self.reference_grid
        diff[self.hole] = False
        return np.sum(diff)
    
    def cost(self):
        """ Compute the distance to the solution
            including the already travelled distance in self.travelled """
        return self.travelled + self.distance_to_solve

def create_puzzle(n, shuffle_steps=0, hole=None, reference_grid=None, grid=None):
    """ Factory method to create a new solvable puzzle of size n """
    if (reference_grid is None):    
       reference_grid = np.roll(np.arange(n*n),n**2-1).reshape((n, n))
    if (grid is None):
        grid = reference_grid.copy()
    if (hole is None):
        hole = (n-1,n-1)
    if (shuffle_steps>0):
        random.seed(4)
    while (shuffle_steps>0):
        candidates = candidate_movements(hole,n)
        hole = move_grid(grid,hole,n,random.choice(candidates))
        shuffle_steps -= 1
    puzzle = TilePuzzle(grid, n, hole, reference_grid)
    return puzzle

def move_grid(grid,hole,n,direction):
    """ Move the hole in the grid in the indicated direction """
    if (direction not in candidate_movements(hole,n)):
        raise ValueError("This movement is not valid")
    (hole_row,hole_col) = hole
    target_hole_row = hole_row-1 if (direction=='up') else hole_row+1 if (direction=='down') else hole_row
    target_hole_col = hole_col-1 if (direction=='left') else hole_col+1 if (direction=='right') else hole_col
    grid[hole_row,hole_col] = grid[target_hole_row,target_hole_col]
    grid[target_hole_row,target_hole_col] = 0
    return (target_hole_row,target_hole_col)

def candidate_movements(hole,n):
    """ Return valid movements in the current grid """
    (row,col) = hole
    candidates = []
    if (row>0):
        candidates.append('up')
    if (row+1<n):
        candidates.append('down')
    if (col>0):
        candidates.append('left')
    if (col+1<n):
        candidates.append('right')
    return candidates
    
def move(puzzle, direction):
        """ Create a new state moving three hole to the indicated direction registering:
            the direction in next_puzzle.step
            the previous state in puzzle.prev_state
            and incrementing next_puzzle.travelled """
        next_grid = puzzle.grid.copy()
        hole = move_grid(next_grid, puzzle.hole, puzzle.n, direction)
        next_puzzle = create_puzzle(puzzle.n, 0, hole, puzzle.reference_grid, next_grid)
        next_puzzle.step = direction
        next_puzzle.prev_state = puzzle
        next_puzzle.travelled = puzzle.travelled+1
        return next_puzzle

def bab_solve_puzzle(puzzle):
    heap = []
    while (puzzle.compute_distance_to_solve()>0):
        movements = candidate_movements(puzzle.hole, puzzle.n)
        #current_cost = puzzle.cost()
        for puzzle.direction in movements:
            puzzles = []
            next_puzzle = move(puzzle, puzzle.direction)
            #next_cost = next_puzzle.cost()
            heapq.heappush(heap, puzzles, next_puzzle)
        puzzle = heapq.heappop(puzzles)
        puzzle.candidatos.append(next_puzzle)
    return puzzle

def steps_to_solve(puzzle):
    """ puzzle - the solution state
        Return the list of steps from the initial puzzle state to the solution state """
    x = len(puzzle.steps)
    for i in range(x):
        print(puzzle.candidatos[i])
    #pass
 
p = create_puzzle(3, 25)
print(p)
start = time.time()
solved_puzzle = bab_solve_puzzle(p)
end = time.time()
print("BAB time: ", end - start)
if (solved_puzzle):
    print("Steps to solve:", steps_to_solve(solved_puzzle))
    print("Cost (steps):",solved_puzzle.cost())
else:
    print("No solution found")