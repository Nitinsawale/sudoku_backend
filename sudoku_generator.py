import math
import random
import copy
PUZZLE_SIZE = 9
EMPTY_VALUE = ""
PUZZLE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class sudokuGenerator():


	def __init__(self):
		self.puzzle = [[EMPTY_VALUE for _ in range(9)] for x in range(9)]
		self.generate_solution()


	def is_valid_puzzle(self, row, col, value, puzzle_size):

		for col_ in range(puzzle_size):
			if self.puzzle[row][col_] == value:
				return False
		
		for row_ in range(puzzle_size):
			if self.puzzle[row_][col] == value:
				return False
		
		startRow = math.floor(row / 3) * 3
		startCol = math.floor(col / 3) * 3

		for i in range(startRow, startRow + 3):
			for j in range(startCol, startCol + 3):
				if self.puzzle[i][j] == value:
					return False
				
		return True

	def has_empty_cell(self, puzzle_size):
		
		for i in range(puzzle_size):
			for j in range(puzzle_size):
				if self.puzzle[i][j] == EMPTY_VALUE:
					return True
		return False

	def generate_solution(self):
		"""generates a full solution with backtracking"""
		number_list = [1,2,3,4,5,6,7,8,9]
		for i in range(0,81):
			row=i//9
			col=i%9
			if self.puzzle[row][col]==EMPTY_VALUE:
				random.shuffle(number_list)      
				for number in number_list:
					if self.is_valid_puzzle(row,col,number, PUZZLE_SIZE):
						self.puzzle[row][col]=number
						if not self.has_empty_cell( PUZZLE_SIZE):
							
							return True
						else:
							if self.generate_solution():
								return True
				break
		self.puzzle[row][col]= EMPTY_VALUE
		return False

	def get_non_empty_squares(self, grid):
		"""returns a shuffled list of non-empty squares in the puzzle"""
		non_empty_squares = []
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != EMPTY_VALUE:
					non_empty_squares.append((i,j))
		random.shuffle(non_empty_squares)
		return non_empty_squares
	
	def remove_numbers_from_grid(self):
		"""remove numbers from the grid to create the puzzle"""
		#get all non-empty squares from the grid
		non_empty_squares = self.get_non_empty_squares(self.puzzle)
		non_empty_squares_count = len(non_empty_squares)
		rounds = 3
		while rounds > 0 and non_empty_squares_count >= 17:
			#there should be at least 17 clues
			row,col = non_empty_squares.pop()
			non_empty_squares_count -= 1
			#might need to put the square value back if there is more than one solution
			removed_square = self.puzzle[row][col]
			self.puzzle[row][col]= EMPTY_VALUE
			#make a copy of the grid to solve
			grid_copy = copy.deepcopy(self.puzzle)
			#initialize solutions counter to zero
			self.counter=0      
			self.solve_puzzle(grid_copy)   
			#if there is more than one solution, put the last removed cell back into the grid
			if self.counter!=1:
				self.puzzle[row][col]=removed_square
				non_empty_squares_count += 1
				rounds -=1
		return


	def solve_puzzle(self, grid):
		"""solve the sudoku puzzle with backtracking"""
		for i in range(0,81):
			row=i//9
			col=i%9
			#find next empty cell
			if grid[row][col]== EMPTY_VALUE:
				for number in range(1,10):
					#check that the number hasn't been used in the row/col/subgrid
					if self.valid_location(grid,row,col,number):
						grid[row][col]=number
						if not self.find_empty_square(grid):
							self.counter+=1
							break
						else:
							if self.solve_puzzle(grid):
								return True
				break
		grid[row][col]=EMPTY_VALUE
		return False
	
	def valid_location(self,grid,row,col,number):
		"""return False if the number has been used in the row, column or subgrid"""
		if self.num_used_in_row(grid, row,number):
			return False
		elif self.num_used_in_column(grid,col,number):
			return False
		elif self.num_used_in_subgrid(grid,row,col,number):
			return False
		return True

	def find_empty_square(self,grid):
		"""return the next empty square coordinates in the grid"""
		for i in range(9):
			for j in range(9):
				if grid[i][j] == EMPTY_VALUE:
					return (i,j)
		return

	def num_used_in_row(self,grid,row,number):
		"""returns True if the number has been used in that row"""
		if number in grid[row]:
			return True
		return False

	def num_used_in_column(self,grid,col,number):
		"""returns True if the number has been used in that column"""
		for i in range(9):
			if grid[i][col] == number:
				return True
		return False

	def num_used_in_subgrid(self,grid,row,col,number):
		"""returns True if the number has been used in that subgrid/box"""
		sub_row = (row // 3) * 3
		sub_col = (col // 3)  * 3
		for i in range(sub_row, (sub_row + 3)): 
			for j in range(sub_col, (sub_col + 3)): 
				if grid[i][j] == number: 
					return True
		return False

# def generate_puzzle(grid):

#     values = [1,2,3,4,5,6,7,8,9]
#     for i in range(0,81):
#         row = i // 9
#         col = (i % 9) 
#         if grid[row][col] == EMPTY_VALUE:            
#             random.shuffle(values)
#             for val in values:
#                 if is_valid_puzzle(grid, row, col, val, puzzle_size=9):
#                     grid[row][col] = val
#                     if not has_empty_cell(grid, 9):
						
#                         return True
#                     else:
#                         if generate_puzzle(grid):
#                             return True   
#             break
#     return False


def generate_new_puzzle():
	new_puzzle = sudokuGenerator()
	solution = copy.deepcopy(new_puzzle.puzzle)
	new_puzzle.remove_numbers_from_grid()
	return new_puzzle.puzzle, solution

if __name__ == "__main__":
  generate_new_puzzle()