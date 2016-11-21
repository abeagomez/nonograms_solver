import util
from pprint import pprint

def build_board(size):
	board = []
	for i in range(0,size):
			l = []
			for j in range(0,size):
				l.append(False)
			board.append(l)
	return board


class problem:
	def __init__(self, restrictions_columns, restrictions_rows, size, board):
		#Restricciones para las columnas
		self.restrictions_columns = restrictions_columns
		#Restricciones para las filas
		self.restrictions_rows = restrictions_rows
		#Tamano del tablero... so far es una matriz cuadrada
		self.size = size
		#Tablero sobre el que se va a trabajar
		self.board = board
	
	#Indice de la fila actual de tablero (comenzando por 0)
	def current_row_index(self, index):
		return index//self.size

	#Indice de la columna actual de tablero (comenzando por 0)
	def current_column_index(self, index):
		return index%self.size

	#Asigna un valor(value) a la casilla deseada del tablero(index)
	def set_value(self, index, value):
		self.board[self.current_row_index(index)][self.current_column_index(index)] = value

	#devuelve la fila correspondiente a la posicion index del tablero
	def current_row(self, index):
		index = self.current_row_index(index)
		row = []
		for i in range(0, self.size):
			row.append(self.board[index][i])
		return row

	#devuelce la columna correspondiente a la posicion index del tablero
	def current_column(self, index):
		index = self.current_column_index(index)
		column = []
		for i in range(0, self.size):
			column.append(self.board[i][index])
		return column

	#Dada una posicion del tablero, comprueba la factibilidad de la columna y la fila correspondientes.
	def check_current_line(self, index):
		if not self.check_previous_row(index): return False
		row = self.current_row(index)
		column = self.current_column(index)
		column_index = self.current_column_index(index)
		if row[column_index]:
			if self.check_row_when_set_true(row, index) and self.check_column_when_set_true(column, index):
				return True
		else:
			if  self.check_row_when_set_false(row, index) and self.check_column_when_set_false(column, index):
				return True
		return False

	def check_row_when_set_true(self, row, index):
		return self.checkline(row, self.restrictions_rows[self.current_row_index(index)], self.current_column_index(index))
	
	def check_row_when_set_false(self, row, index):
		return self.check_inFalse_line(row, self.restrictions_rows[self.current_row_index(index)], self.current_column_index(index))
	
	def check_column_when_set_true(self, column, index):
		return self.checkline(column, self.restrictions_columns[self.current_column_index(index)], self.current_row_index(index))
	
	def check_column_when_set_false(self, column, index):
		return self.check_inFalse_line(column, self.restrictions_columns[self.current_column_index(index)], self.current_row_index(index))

	#Si una posicion del tablero es la primera de una fila, comprueba que la fila anterior quedo en un estado factible
	def check_previous_row(self, index):
		previous_row_index = self.current_row_index(index) - 1
		if self.current_column_index(index) is 0 and previous_row_index >= 0:
			row = self.current_row(index - 1)
			if self.check_whole_line(row, self.restrictions_rows[previous_row_index]):
				return True
			return False
		return True

	def check_rest_of_line(self, line, restrictions, line_blocks, index, mark):
		if mark:
			n_res = restrictions[len(line_blocks)-1]
			if n_res < line_blocks[-1]: return False
			rest = n_res - line_blocks[-1]
			s = 0
			for i in range(len(line_blocks),len(restrictions)):
				s += restrictions[i] + 1
			rest = rest + s
			if len(line) - (index + 1) < rest: return False
			return True
		else:
			s = 0
			if line_blocks[-1] is not 0:
				for i in range(len(line_blocks),len(restrictions)):
					s += restrictions[i] + 1
			else:
				for i in range(0, len(restrictions)):
					s += restrictions[i] + 1

			s -= 1
			if len(line) - (index + 1) < s: return False
			return True

	def check_inFalse_line(self, line, restrictions, index):
		result = self.simple_split(line)
		line_blocks = result[0]
		if len(line_blocks) is 1 and result[1] > 0:
			if line_blocks[0] is not restrictions[0]: return False
		for i in range(0, len(line_blocks)-1):
			if restrictions[i] != line_blocks[i]: return False
		if not self.check_rest_of_line(line, restrictions, line_blocks, index, False): return False
		return True

	def checkline(self, line, restrictions, index):
		result = self.simple_split(line)
		line_blocks = result[0]
		if len(restrictions) < len(line_blocks): return False
		for i in range(0, len(line_blocks)-1):
			if restrictions[i] != line_blocks[i]: return False
		if not self.check_rest_of_line(line, restrictions, line_blocks, index, True): return False
		return True
	
	def check_board(self):
		for i in range(0, self.size):
			column = self.current_column(i)
			if not self.check_whole_line(column, self.restrictions_columns[i]): return False
			row = self.current_row(i*self.size)
			if not self.check_whole_line(row, self.restrictions_rows[i]): return False
		return True
		
	def simple_split(self, line):
		split_blocks = []
		current = 0
		n = 0
		index = 0
		while n<len(line):
			while n<len(line) and not line[n]:
				n += 1
			while n < len(line) and line[n]:
				current += 1
				n+=1
			if current > 0:
				index = n
				split_blocks.append(current)
			current = 0
		if len(split_blocks) is 0:
			split_blocks.append(0)
		return (split_blocks, index)

	def check_whole_line(self, line, restrictions):
		line_blocks = self.simple_split(line)[0]
		if len(line_blocks) != len(restrictions): return False
		for i in range(0, len(restrictions)):
			if line_blocks[i] != restrictions[i]:
				return False
		return True 

	def copy_board(self):
		board = []
		for i in self.board:
			l = []
			for j in range(0, len(i)):
				l.append(i[j])
			board.append(l)
		return board

def dfs(size, restrictions_columns, restrictions_rows):
	board = build_board(size)
	p = problem(restrictions_columns, restrictions_rows, size, board)
	s = util.Stack()
	s.push((p, 0))
	while not s.isEmpty():
		current_element = s.pop()
		current_problem = current_element[0]
		current_index = current_element[1]
		if current_problem.check_board():
			pprint(current_problem.board)
			for row in current_problem.board:
				print("".join(("#" if x else ".") for x in row))
			return current_problem.board
		if current_index > size*size:
			continue
		p_right = problem(current_problem.restrictions_columns, 
							current_problem.restrictions_rows, 
							current_problem.size, 
							current_problem.copy_board())
		p_right.set_value(current_index, False)
		p_left = problem(current_problem.restrictions_columns, 
							current_problem.restrictions_rows, 
							current_problem.size, 
							current_problem.copy_board())
		p_left.set_value(current_index, True)
		new_index = current_index + 1
		if p_right.check_current_line(current_index):
			s.push((p_right,new_index))
		if p_left.check_current_line(current_index):
			s.push((p_left, new_index))
	return []


p = problem([[1,1],
			[3,1],
			[3],
			[3,1],
			[1,1]],
			[[1,1],
			[3],
			[5],
			[1],
			[2,2]],5, [[False, False, False, False, False],
						[False, False, False, False, False],
						[False, False, False, False, False],												
						[False, False, False, False, False],
						[False, False, False, False, False]] )

b = build_board(4)
p2 = problem([[4],[3],[3],[1]],[[2,1],[3],[3],[1,1]],4, [[True,True,False,True],[False,True,True,True],[False,False,False,False],[False,False,False,False]])

s = [[False, True, False, True, False],
	[False, True, True, True, False],
	[True, True, True, True, True],
	[False, False, True, False, False],
	[True, True, False, True, True]]

#print p2.check_current_line(4)

#dfs(3, [[1],[1],[2]], [[1],[1,1],[1]])
#dfs(4,[[4],[2,1],[2,1],[1,2]],[[4],[3],[1,1],[4]])

dfs(15,[[1, 1, 1, 1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 2], [1, 1, 1, 1], [1, 1, 1], [1, 1, 1], [3, 1], [1, 1], [1, 2, 6, 1], [2, 1], [2, 3, 1], [1, 1], [1, 1, 3, 1], [2, 1, 1]], [[1, 2], [1, 1, 2], [2, 1, 1, 1, 1], [3, 1], [1, 1, 1, 1], [1, 2, 1], [1], [1, 1, 1, 2], [2, 2, 1, 1], [1, 1, 1, 1, 1], [1, 2, 2], [2, 2], [1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1]])
"""
dfs(10, [[5],
[5,1],
[1,3],
[1,2,1],
[2,1,1],
[2,4],
[1,2],
[6],
[5],
[7]], [[3,1],
[6,2],
[2,3],
[2,3],
[3,3],
[4,3],
[4,1,1],
[1,1],
[4],
[1,2]])

dfs(15, [[1,1,1],
[1,1,2],
[3,6],
[5,3,1],
[6,5],
[3,7,1],
[2,7,1],
[1,4,2,1],
[4,1,1],
[2,2,3,1],
[2,4,1,1],
[9,1,1],
[2,1,1],
[2,1,1,3],
[1,4,5]],[[4,2,2],
[5,5],
[3,2,2],
[2,2,1],
[9],
[1,8,1],
[3,3,2,2],
[2,2,3,1],
[7,1,2],
[7,1,1],
[1,1,3,2,1],
[1,1,3,1],
[1,3,2],
[2,3],
[4,2,2]])
"""
#board = build_board(3)
#p = problem([[1,1],[1],[0]], [[2],[0],[1]], 3, board)
#print p.board
#p2 = problem(p.restrictions_columns, p.restrictions_rows, p.size, p.copy_board())
#p3 = problem(p.restrictions_columns, p.restrictions_rows, p.size, p.copy_board())
#print p2.board
#print p3.board

#p2.set_value(1, True)
#print ""
#print p2.board
#print ""
#print p3.

#p = problem([[2],[0],[1]],[[1,1],[1],[0]], 3, [[True, False, True], [True, False, False], [False, False, False]])
#print p.check_board()
