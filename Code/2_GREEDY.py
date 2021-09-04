import FitnessFunction as fit
import Scramble 
import math
import random
from scrambleGenerator import makeMove
import matplotlib.pyplot as plt
from os import system, name 
import time
import numpy as np


# This global variable is used to count the number of times,
# Kociemba algorithm was called throughout the program
numberOfEvaluations = 0


def evaluationFunction(cube_orientation, n):
	"""
	This fucntion will return the fitness of the cube. 
	It will run the Kociemba's algorithm on the cube state n times and take the average of n values.
	cube_orientation - orientation or the state of the cube.
	n - number of times Kociemba needs to be called on the cube state
	"""

	# Refer to the global variable numberOfEvaluations
	global numberOfEvaluations

	# To hold the sum of the fitness values
	fitnessSum = 0

	# Call the Kociemba n times on the cube state and sum them
	for i in range(n):
		fitnessSum = fitnessSum + fit.fitness(cube_orientation)
	
	# And increament the number of evaluations by n
	numberOfEvaluations = numberOfEvaluations + n	

	# Return the rounded average value
	return round(fitnessSum/n)


def bubbleSort(possibleMoves): 
	"""
	This is a bubble sort function.
	This function takes all the moves applied to the cube and the fitness obtained 
	when applying those moves and sorts them in ascending order.
	I wrote this function as the inbuilt function like sort(), sorted() didn't give proper outputs.
	possibleMoves - Input in the form of a 2D array which has the 18 move applied and the fitness.
	[[R, 18],[R', 18],[R2, 17], ... ]
	"""

	# Find the length of the array
	arrlen = len(possibleMoves) 

	# Traverse through all array elements 
	for i in range(arrlen): 

		# Last i elements are already in place 
		for j in range(0, arrlen-i-1): 

			# traverse the array from 0 to n-i-1 
			# Swap if the element found is greater, than the next element 
			# We will have to compare the values i.e. the fitness values
			if possibleMoves[j][1] > possibleMoves[j+1][1] : 
				possibleMoves[j], possibleMoves[j+1] = possibleMoves[j+1], possibleMoves[j] 


def convert2Scramble(scramble):
	"""
	This will take a string "F F' F2"and will convert it into the form [['F',''],['F',"'"],['F','2']].
	We need to give it in the above format for the scrambling to work
	"""
	# Create an empty array to store the moves
	properScramble = []

	# Split based on the space between characters
	moves = scramble.split(" ")
	
	# Delete the last element as it is a space
	del moves[-1]	

	# Take every moves
	for m in moves:
		subMoves = ["", ""]
		if m == "F'" or m == "B'" or m == "R'" or m == "L'" or m == "U'" or m == "D'" or m == "F2" or m == "B2" or m == "R2" or m == "L2" or m == "U2" or m == "D2":
			subMoves[0] = m[0]
			subMoves[1] = m[1]
		else:
			subMoves[0] = m
			subMoves[1] = ""

		properScramble.append(subMoves)

	# Return the proper scramble format
	return properScramble


def FindAllPossibleMoves(legal_moves, AllAppliedMoves, possibleMoveTree,n):
	"""
	This function will return all the possible moves that can be applied to the cube,
	along with the fitness value for each moves.
	The output will be in the format [[U, 18], [U', 18], ..].
	This will be appended to an array called the possibleMoveTree which 
	will hold the possible moves at each depth.
	legal_moves - Moves that can be applied to the cube - [R, R', R2, ...]
	AllAppliedMoves - Moves applied to the cube till now.
	possibleMoveTree - the moves applied to the cube in every depth
	n - Number of times the Kociemba has to be called for a state.
	"""
	
	# This will hold all the possible moves from the current state along with its fitness values
	# This will be an array with a list [moves, fitness]
	possibleMoves = []
		
	# Take each possible move from the list of legal moves
	for i in range(len(legal_moves)):
		
		# Apply that move to the cube
		properScramble = convert2Scramble(AllAppliedMoves + legal_moves[i] + " ")
		
		# Find the length of the scramble
		scrambleLength = len(properScramble)	
		
		# Make that scramble and get the orientation
		scramble, cube_orientation = Scramble.scramble(True, properScramble, scrambleLength)
		
		# Now find the fitness value for the cube orientation
		fitnessValue = evaluationFunction(cube_orientation,n)
		
		# Now add the move and its fitnessValue to the dictionary
		possibleMoves.append([legal_moves[i], fitnessValue])
	
	# Now we are going to sort the list of moves and its fitness function.
	# Now I am going to sort this using bubble sort as the pre defined sort function in python can't sort it properly.		
	bubbleSort(possibleMoves)
		
	# Now we are going to append it to the list that holds the possible moves at each depth
	possibleMoveTree.append(possibleMoves)	
	
	# Return the possible move tree
	return possibleMoveTree


def GREEDY(iterations, manualflag, scramble,n):
	"""
	This function uses a greedy approach with backtracking to find the shortest path to the solved state.
	It works as follows:
	1. Find the fitness function of the current state of the cube.
	2. Apply all the 18 legal moves to the cube and find the fitness value of the next possible legal states.
	3. Sort the state and the moves in ascending order of fitness value.
	4. Apply the move that gives minimum fitness value.
	5. If the fitness value of all 18 moves is greater than previous state undo the move applied to the previous state
	6. Repeat steps 1 - 5 till the state is solved state.	

	iteration - number of iterations to run the PSO
	particles - number of particles
	manualflag - to check if the scramble is random or manual scramble
	scrambe - scramble. 
	It is a NULL string ("") if manualflag is "R" i.e. random scramble
	Or it is a string if manualflag is "M" i.e. user given scramble
	n - number of times the Kociemba needs to be called on a cube state
	"""
	
	# Problem definition for the greedy tree search
	# This returns the scramble and the orientation of the stickers in the cube		
	# If it is a random scramble
	if manualflag == False:
		# Problem definition
		scramble, cube_orientation = Scramble.scramble(manualflag,scramble,0)	# This returns the scramble and the orientation of the stickers in the cube
	
	# Else if it is a manual scramble
	else:
		# Now apply the move to the cube
		properScramble = convert2Scramble(scramble)
		
		# Find the length of the scramble
		scrambleLength = len(properScramble)	
		
		# Make that scramble and get the orientation
		scramble, cube_orientation = Scramble.scramble(manualflag, properScramble, scrambleLength)
	
	# Save the scramble used
	originalScramble = scramble
	
	# Save the initial cube orientation
	initialOrientation = cube_orientation
	
	# Original Fitnees score
	originalFitness = evaluationFunction(cube_orientation,n)

	# Refer to the global variable numberOfEvaluations
	global numberOfEvaluations

	# We will decrease number of evaluations by n, since 
	# we just want to find the fitness of the scrambled cube for comparing
	# how the algorithm did with Kociemba.
	# This fitness evaluation is not part of the program, so we will decrease it by n
	numberOfEvaluations = numberOfEvaluations - n
	
	# Print the initial orientation
	print("Scramble : ",originalScramble)
	print("Initial cube orientation: ", initialOrientation)
	print("Initial fitness : ",originalFitness)
	print("\n")
	
	# We are going to create a few data structures to hold a set of ingormations
	
	# A data structure to hold the legal moves available  i.e. U,U',U2,...,R,R',R2.
	# Since Kociemba works on half turn metric where two turns of the side are counted as one move we will use half turn metric.
	legal_moves = ["U", "U'", "U2", "D", "D'","D2", 
				   "L","L'", "L2", "R", "R'", "R2",
				   "F","F'", "F2", "B", "B'", "B2",				   
				  ]	
	
	# For each state we will evalaute its fitness three times using Kociemba's algorithm and average them
	# To save time we use this data structure to hold the evaluated scores,
	# and we take the fitness value from it instead of evalauting the positions again to save time.
	# This list will hold the orientation of the cube.
	orientations = []
	orientations.append(initialOrientation)	# This is the scrambled position
	
	# This will hold the fitness value at each depth for each orientation
	fitnessValues = []
	fitnessValues.append(originalFitness)	# This is the fitness of the scrambled position
	
	# This list will hold the moves applied to the cube and the fitness values
	movesApplied = []
	
	# This will hold the possible moves at each depth
	possibleMoveTree = []
	
	# This variable will hold the moves that are applied to the cube including the scramble
	# Initially only the scramble has been applied to the cube
	AllAppliedMoves = originalScramble
	
	# This variable is used to hold the maximum depth that the algorithm went to find the solution
	maxDepth = 0
	
	# This variable will hold the iteration and also fitness at each iteration
	xIter = []
	yFitnessIter = []	# This is used to hold the fitness reached at each iteration
	yGlobalIter = []	# This is used to hold the global minimum value at each iteration
	globalMinimum = originalFitness	# This variable is used to hold the global minimum fitness value.
		
	# This variable is used to check if the solution has been found
	# This will be set to true if it could not be found.
	flag = False
	
	# We will set an iteration limit. 
	# If the program execution exceded the limit, we will break out of the loop.
	iteration_limit = iterations
	iter = 0	# Iteration starts from 0
	
	start_time = time.time()	# This is were the execution begins
	while(True):
		
		print("\n")
		print("Iteration : ",iter)
		
		# Continue the while loop till the cube is solved
		if orientations[-1] == "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":
			break
		
		# Call the possible move function.
		# This is used to find all the possible moves that can be applied from the given state.
		possibleMoveTree = FindAllPossibleMoves(legal_moves, AllAppliedMoves, possibleMoveTree,n)
		
		# We need to do backtracking till we get a condition where we dont need to backtrack
		while(True):
			
			print("\n")
			print("Total Depth : ", len(possibleMoveTree))
			
			# We need to check a condition that can happen sometime. 
			# The scrambled cube has a fitness value of lets say 8.
			# And all the possible 18 moves give fitness value greater than 8. 
			# This means that we cannot apply a move to the cube. 
			# In this case we will just select the first move available and see where it goes. 
			
			# This should only be done in depth 1. 
			if len(possibleMoveTree) == 1:
				count = 0
				for i in range(len(possibleMoveTree[-1])):
					if possibleMoveTree[-1][i][1] > fitnessValues[-1]:
						count +=1
				
				# If all the possible moves have fitness greater than the scrambled state at depth 1.
				# Just apply the first minimum move and see where it leads.
				if count == len(possibleMoveTree[-1]):
					print("No possible moves give fitness less than previous level.")
					print("So we take the ones we have now.")
				
					# Now we will select the move from the last depth
					move = possibleMoveTree[-1].pop(0) # This will be an array [move, fitness]
					
					# Now we have got the move, now apply the move to the cube
					properScramble = convert2Scramble(AllAppliedMoves + move[0] + " ")
			
					# Find the length of the scramble
					scrambleLength = len(properScramble)	
					
					# Make that scramble and get the orientation when the move is applied
					scramble, new_orientation = Scramble.scramble(True, properScramble, scrambleLength)
					
					newFitness = move[1]	# We have already applied the move and found the fitness value. So we just have to take that from [move, fitness]
					oldFitness = fitnessValues[-1]	# To prevent save time we take the stored fitness value.
					
					# Save the cube orientation
					orientations.append(new_orientation)
					fitnessValues.append(newFitness)
					print("Orientation : ", new_orientation, end = " ")
					print("Move applied : ", move[0], end = " ")
					print("New Fitnees : ", newFitness, end = " ")
					print("Old Fitnees :", oldFitness)
					print("Fitnees Stack : ",fitnessValues)
					
					# This graph is used to show the fitness value at each depth.
					xIter.append(iter)
					yFitnessIter.append(newFitness)
					
					# We need to update the global minimum value and append it.
					if newFitness < globalMinimum:
						globalMinimum = newFitness
					
					yGlobalIter.append(globalMinimum)	# Global minimum is the minimum value of the fitness
					
					# Save the move applied
					movesApplied.append(move[0])
					
					# Save it to all the moves applied
					AllAppliedMoves = AllAppliedMoves + move[0] + " "
					
					# Break out of this loop as we have applied the move.
					# Break out of the inner while loop.
					break
			
			# Update the maximum depth
			if len(possibleMoveTree) > maxDepth:
				maxDepth = len(possibleMoveTree)
			
			# Print the depth reached and branches at each depth.
			for i in range(len(possibleMoveTree)):				
				print("Depth : ", i+1 , end = " ")
				print("Branches : ", len(possibleMoveTree[i]), end = " ")
				for j in range(len(possibleMoveTree[i])):
					print("|",possibleMoveTree[i][j][0],possibleMoveTree[i][j][1],end = " ")
				print("\n")
			print("\n")
			
			# Now we will take the move that gave the smallest fitness value.		
			# From the last depth take the first move in the list (along with fitness value)			
			# But we need to make sure that there are branches in the last depth
			while (len(possibleMoveTree[-1]) == 0):
				print("Branch empty, so backtracking")
				
				# Remove the cube orientation
				orientations.pop(-1)
				
				# Remove the fitness value
				fitnessValues.pop(-1)		
				
				# Remove the last move applied
				movesApplied.pop(-1)
				
				# Split it by space, we get a list
				AllMoves = AllAppliedMoves.split(" ")
				
				# Copy it to another list, except the last element. 
				# The last element is space and the second last is the move applied.
				AllMoves = AllMoves[:-2]
				
				# Convret the list to string 
				AllAppliedMoves = " ".join([str(elem) for elem in AllMoves]) 
				
				# Add space at the end
				AllAppliedMoves = AllAppliedMoves + " "
				
				# Delete the last depth of the tree as it will be just an empty list.
				arr = possibleMoveTree.pop(-1)			
				
				# If the branches of depth 1 are empty then the possible move tree is also empty.
				# So break out of this while loop
				if len(possibleMoveTree) == 0:
					flag = True
					break
			
			# Now if there are no more branches to search then sadly the algorithm could not find the solution.
			# So break out of the inner while loop. No need to continue further as there are no more moves left.
			if len(possibleMoveTree) == 0:
					flag = True
					break
			
			# Now we will select the move from the last depth
			move = possibleMoveTree[-1].pop(0) # This will be an array [move, fitness]
			
			# Now we have got the move. But we need to check if its fitness is less than previous state.
			# Now apply the move to the cube
			properScramble = convert2Scramble(AllAppliedMoves + move[0] + " ")
	
			# Find the length of the scramble
			scrambleLength = len(properScramble)	
			
			# Make that scramble and get the orientation when the move is applied
			scramble, new_orientation = Scramble.scramble(True, properScramble, scrambleLength)
			
			# Here we will compare the fitness value of previous state with fitness value when a single move is applied.
			# If the finess value of new state is greater than previous state then we need to select a new move.
			newFitness = move[1]	# We have already applied the move and found the fitness value. So we just have to take that from [move, fitness]
			oldFitness = fitnessValues[-1]	# To save time we take the stored fitness value.
			if newFitness > oldFitness:
				print(newFitness, ">", oldFitness)
				continue
			
			# We need to make sure that a cycle isn't produced.
			# If the new orientation is already reached state then there is a chance that a cycle will be produced.
			# So we will skip the move applied so that we don't reach that state and cause a cycle.
			elif new_orientation in orientations:
				print("Cycle.")
				continue
			
			# If the fitness value is less than previous level, we can apply that move 
			# And we are sure that it won't produce a cycle.
			else:
				
				# Save the cube orientation
				orientations.append(new_orientation)
				fitnessValues.append(newFitness)
				print("Orientation : ", new_orientation, end = " ")
				print("Move applied : ", move[0], end = " ")
				print("New Fitnees : ", newFitness, end = " ")
				print("Old Fitnees :", oldFitness)
				print("Fitnees Stack : ",fitnessValues)
				
				# This graph is used to hold the fitness value at each iteration
				xIter.append(iter)
				yFitnessIter.append(newFitness)
				
				# We need to update the global minimum value and append it.
				if newFitness < globalMinimum:
					globalMinimum = newFitness
					
				yGlobalIter.append(globalMinimum)	# Global minimum is the minimum value of the fitness
				
				# Save the move applied
				movesApplied.append(move[0])
				
				# Save it to all the moves applied
				AllAppliedMoves = AllAppliedMoves + move[0] + " "
				
				# Break out of this loop
				break
		
		# Now if there are no more branches to search then sadly the algorithm could not find the solution.
		# So break out of the outer while loop. No need to continue further as there are no more moves left.
		if len(possibleMoveTree) == 0:
			flag = True
			break
		
		# Increment the iteration
		iter+=1
				
		# If the program execution exceded iteration limit we will exit the program
		if iter == iteration_limit:
			flag = True
			print("Iteration Limit of : ",iteration_limit, " exceeded.")
			break
		
	end_time = time.time()	# This is where the entire PSO loop finishes execution
	total_time = end_time - start_time	# This is the total time needed for the loop execution
	
	# Print the initial cube orientation
	print("\n")
	print("Cube orientation: Yellow on top and green on front.")
	print("Reading order goes: Up, Right, Front, Down, Left, Back.")
	print("Scramble: ", originalScramble)
	print("Initial cube orientation : ",initialOrientation)
	print("\n")
	if flag == True:
		print("SOLUTION COULD NOT BE FOUND.")
	
	else:
		print("SOLUTION WAS FOUND.")
	
	# Convert the list to string
	solution = " ".join([str(elem) for elem in movesApplied]) 
	print("Fitnees Stack : ",fitnessValues)
	print("Solution : ", solution)
	print("\n")
	print("Original Fitnees : ",originalFitness)
	print("Obtained Length : ",len(movesApplied))
	print("Minimum Fitnees The Algorithm Reached : ",globalMinimum)
	print("Maximum Depth the algorithm went : ", maxDepth)
	print("Iteration : ",iter)
	print("NUMBER OF FUNCTION EVALUATIONS : ",numberOfEvaluations)
	print("Total Time : ", total_time)	
	
	# Plotting the change of personal best with each iteration for particle
	plt.grid(True)
	plt.plot(xIter,yGlobalIter,c="blue",linestyle="--",marker="o")
	plt.plot(xIter,yFitnessIter,c="red",linestyle=':')	# Plot iteration vs fitness
	
	plt.xlabel('Iterations')	# naming the x axis as iterations
	plt.ylabel('Fitness Score')	# naming the y axis as fitness score	
	plt.title('Iterations vs Fitness')	# giving a title to my graph 
	plt.legend(["Global Fitness","Current Fitnees"]) 	
	plt.yticks(np.arange(0,22,step = 2))
	# WE will set the xtick step to maximum number of iterations done divided by 10
	xSteps = max(xIter)//10

	# If it is 0 we will set it to 1
	if xSteps == 0:
		xSteps = 1

	plt.xticks(np.arange(0,max(xIter),step = xSteps))
	plt.show()
	

# Main program
if __name__ == "__main__":
	print("\n")
	print("Greedy Tree Search Algorithm")
	iterations = int(input("Enter the number of iterations : "))
	randomOrManual = input("Type M for manual scramble or R for random scrabmle : ")
	n = int(input("Enter the number of times fitness of cube has to be evaluated : "))
	if randomOrManual == "R":
		manualflag = False
		scramble = ""
	elif randomOrManual == "M":
		manualflag = True
		scramble = input("Type scramble : ")
		
	# Function call
	# Add space to the scramble entered by the user, implementation reason.
	GREEDY(iterations, manualflag, scramble+" ",n)	# Calling the greedy algorithm	