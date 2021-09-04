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


def findVelocity(legal_moves, particle_personalBest, global_best, currentFitness, global_best_moves):
	"""
	This function will return the velocity i.e. the number moves that need to be applied to the cube
	legal_moves: The set of moves that can be applied on the cube i.e. R, R', R2, ... etc
	particle_personalBest: The personal best score reached by the particle(integer)
	global_best: The global best fitness score (integer)
	currentFitness: Current fitness score reached by the particle (integer)
	global_best_moves: Moves that led to the global best
	"""

	# Find the personal acceleration, P(t) - X(t)
	# Which is the difference between the personal best fitness and current fitness
	personalAcceleration = particle_personalBest - currentFitness

	# Find the global acceleration G(t) - X(t)
	# Which is the difference between the global best and current fitness
	globalAcceleration = global_best - currentFitness

	# If personalAcceleration <=0 and globalAcceleration < 0
	# Then the cube is moving away from the best solutions
	# So we need to go back to the state that gave the global best and try again,
	# till a better solution is obtained
	if personalAcceleration <= 0 and globalAcceleration < 0:
		# The number of random moves that the particle needs to take,
		# is between 1 and the absolute value of global acceleration.
		# Absolute value of globalAcceleration should be taken as it is negative value
		# And it should be rounded to a whole number, 
		# since we took the average while calculating the fitness
		noOfMoves = random.randint(1, abs(globalAcceleration))

		# Take a few random number of moves from the set of moves that can be applied
		newMoves = ""
		for i in range(noOfMoves):
			newMoves = newMoves + random.choice(legal_moves) + " "

		# The velocity is the moves that were needed to reach the global best from start state
		# plus the new random moves
		velocity = global_best_moves + newMoves

		# Since we need to retrace back to the global best we need to set this flag to true
		retrace = True	

	# If personalAcceleration > 0 and globalAcceleration <= 0
	# Then the cube is moving towards the local best
	# So we apply random moves from the current position
	if personalAcceleration > 0 and globalAcceleration <= 0:
		# The number of random moves that the particle needs to take,
		# is between 1 and the value of personal acceleration.
		# It should be rounded to a whole number, 
		# since we took the average while calculating the fitness
		noOfMoves = random.randint(1, personalAcceleration)

		# Take a few random number of moves from the set of moves that can be applied
		# Which will be the velocity of the particle
		velocity = ""
		for i in range(noOfMoves):
			velocity = velocity + random.choice(legal_moves) + " "

		# We are not retracing here as we are applying new moves to the cube
		retrace = False

	# If personalAcceleration > 0 and globalAcceleration >= 0
	# Then the cube is moving towards the global best
	# So we apply random moves from the current position
	if personalAcceleration > 0 and globalAcceleration >= 0:
		# The number of random moves that the particle needs to take,
		# is between 1 and the value of global acceleration,
		# or between 1 and the value of personal acceleration if global acceleration = 0
		# It should be rounded to a whole number, 
		# since we took the average while calculating the fitness
		if globalAcceleration == 0:
			noOfMoves = random.randint(1, personalAcceleration)
		else:
			noOfMoves = random.randint(1, globalAcceleration)

		# Take a few random number of moves from the set of moves that can be applied
		# Which will be the velocity of the particle
		velocity = ""
		for i in range(noOfMoves):
			velocity = velocity + random.choice(legal_moves) + " "

		# We are not retracing here as we are applying new moves to the cube
		retrace = False
	
	# If personalAcceleration == 0 and globalAcceleration == 0
	if personalAcceleration == 0 and globalAcceleration == 0:
		# Then just apply a single random move
		velocity = random.choice(legal_moves) + " "	

		# We are not retracing here as we are applying new moves to the cube
		retrace = False

	# Retun the moves that needs to be applied and an indication if we need to retrace our steps
	return velocity,retrace


def convert2Scramble(scramble):
	"""
	This will take a string "F F' F2"and will convert it into the form [['F',''],['F',"'"],['F','2']].
	We need to give it in the above format for the scrambling to work
	"""
	
	# Create an empty array to store the moves
	properScramble = []
	
	# Split based on the space between characters
	moves = scramble.split(" ")
	#print("Moves : ",moves)
	
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


def PSO(iterations, particles, flag, scramble,n):
	"""
	This is a function that will run the PSO algorithm on the cube and will output a solution.
	The PSO is defined by two equations:
	X(t+1) = X(t) + V(t+1)
	V(t+1) = (W * V(t)) + (C1 * rand(0,1) * (P(t) - X(t))) + (C2 * rand(0,1) *(G(t) - X(t)))
	
	X(t+1): next position of the particles
	X(t): Current position
	V(t): Velocity takn by the particle in previous time step
	V(t+1): Velocity to be taken by the particle in the next time step
	W, c1, c2 = Inertia coefficent, personal acceleration coefficent, global acceleration coefficent
	rand(0,1) = random number between 0 and 1
	P(t) = personal best
	G(t) = Global best
	
	In terms of the Rubik's cube problem we will modify the equations.
	More details are given in the function findVelocity()

	iteration - number of iterations to run the PSO
	particles - number of particles
	flag - to check if the scramble is random or manual scramble
	scrambe - scramble. 
	It is a NULL string ("") if flag is "R" i.e. random scramble
	Or it is a string if flag is "M" i.e. user given scramble
	n - number of times the Kociemba needs to be called on a cube state
	"""
	
	# If it is a random scramble
	if flag == False:
		# Problem definition
		# This returns the scramble and the orientation of the stickers in the cube
		scramble, cube_orientation = Scramble.scramble(flag,scramble,0)	
	
	# Else if it is a manual scramble
	else:
		# Now apply the move to the cube
		properScramble = convert2Scramble(scramble)
		
		# Find the length of the scramble
		scrambleLength = len(properScramble)	
		
		# Make that scramble and get the orientation
		scramble, cube_orientation = Scramble.scramble(flag, properScramble, scrambleLength)
	
	# Save the scramble used
	originalScramble = scramble
	
	# Save the initial cube orientation
	initialOrientation = cube_orientation
	
	# Original Fitnees score
	originalFitness = evaluationFunction(cube_orientation, n)
	
	# Refer to the global variable numberOfEvaluations
	global numberOfEvaluations

	# We will decrease number of evaluations by n, since 
	# we just want to find the fitness of the scrambled cube for comparing
	# how the algorithm did with Kociemba.
	# This fitness evaluation is not part of the program, so we will decrease it by n
	numberOfEvaluations = numberOfEvaluations - n
	
	# Print the scramble, fitness and orientation
	print("Scaramble: ", originalScramble)
	print("Initial Fitnees : ", originalFitness)
	print("Initial cube orientation: ", cube_orientation)
	print("\n")
	
	# Parameters of the PSO
	maxIter = iterations	# Maximum number of iterations
	nPop = particles	# Maximum population size i.e th total number of particles
	
	# We wont be needing these so we will comment it out
	# w = 1		# Inertia coefficent
	# c1 = 1	# Personal acceleration coefficent
	# c2 = 1	# Global acceleration coefficent
	
	# Declaration of variable
	# We will use a list and each index of the list represents a particle
	
	# This list will store the all the moves that was applied to the cube including the scramble.
	# This list holds all the information regarding what moves are to be applied.
	particle_scramble = []	
	
	particle_position = []	# A data structure to hold the position of each particle i.e which orientation they are in
	particle_positionMoves = [] # A data structure to hold the moves that made the particle to reach this position
	particle_velocity = []	# A data structure to hold the velocity of each particle
	particle_personalBest = []	# A data structure to hold the personal best of each particles 
	particle_personalBest_moves = [] # A data structure to hold the moves that gave the personal best
	global_best = math.inf # A variable to hold the global best. Initially the global best is infinity
	global_best_moves = "" # A variable to hold the moves that gave the global best
	solution = []	# This list is used to hold all the particles that found the solved state
	
	# A data structure to hold the legal moves available  i.e. U,U',U2,...,R,R',R2.
	# Since Kociemba works on half turn metric where two turns of the side are counted as one move,
	# we will use half turn metric.
	legal_moves = ["U", "U'", "U2", "D", "D'","D2", 
				   "L","L'", "L2", "R", "R'", "R2",
				   "F","F'", "F2", "B", "B'", "B2",				   
				  ]	
	
	# Initialization of varibles. Here we are going to initailze all the partices
	for i in range(nPop):
		particle_scramble.append(scramble)	# We are going to append the scramble used. 
		particle_position.append(cube_orientation)	# Initially all the particles will be in the initial scrambled position		
		particle_positionMoves.append("")	# Initially since no moves were made the data structure is empty
		particle_velocity.append("")	# Since this is initailzation we will intialze all velocity to empty
		particle_personalBest.append(originalFitness)	# Initially all the particles personal best will be the fitness score of the initial scrabmle
		particle_personalBest_moves.append("")	# Since they didn't make any moves in the beginig the moves that gave them personal best are also empty
		
		# Update global best.
		# If particle i has a fitness score better than the global best, update the global best 
		# and save the moves that led to the global best
		if particle_personalBest[i] < global_best:
			global_best = particle_personalBest[i]
			global_best_moves = particle_personalBest_moves[i]
	
	"""# Diplay the initial values
	for i in range(nPop):
		print("\n")
		print("For particle : ",i)
		print("Scramble : ", particle_scramble[i])
		print("Particle positions : ",particle_position[i])
		print("Particle positions moves : ",particle_positionMoves[i])
		print("Particle velocities : ",particle_velocity[i])
		print("Particle personal best : ",particle_personalBest[i])
		print("Moves that gave perosnal best : ",particle_personalBest_moves[i])
	
	print("\n")
	print("Global best : ", global_best)
	print("Moves that led to global best: ", global_best_moves)"""
	
	# These variables are used to plot the graph between the number of iterations, personal best and particle
	xIter = []	# X axis is used for the iterations
	yPersonalFitness = []	# Y axis is used for the average of the personal best
	yGlobalFitness = []	# Y axis is used for plotting the global fitness
	yCurrentFitness = [] # We are also going to store the current fitness average
	
	# Main loop of PSO
	start_time = time.time()	# This is were the execution begins
	for iteration in range(maxIter):
		print("\n")
		print("Iterations : ", iteration)
		
		# If all the particles found the solution break out of the loop
		if len(solution) == nPop:
				break	
		
		# This varible is used to find the average of the personal fitness and current Fitness
		personalFitnessSum = 0
		currentFitnessSum = 0
		
		# We are saving the global fitness before the inner loop begins for plotting
		yGlobalFitness.append(global_best)
		
		# For each particle
		for i in range(nPop):
			print("Particle : ", i,end = " ")

			#print("Cube Orientation: ",particle_position[i],end=" ")
			# Find the fitness score of the particle
			currentFitness = evaluationFunction(particle_position[i],n)
			personalFitnessSum = personalFitnessSum + particle_personalBest[i]	# To find average of personal fitness
			currentFitnessSum = currentFitnessSum + currentFitness	# To find average of currentFitness

			# Only apply moves if the cube is not already solved
			if particle_position[i] != "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":

				print("Current Fitness : ", currentFitness,end = " ")
				print("Personal Best : ", particle_personalBest[i],end = " ")
				print("Global Best : ",global_best,end = " ")

				# Find the velocity of the particle
				particle_velocity[i],retrace = findVelocity(legal_moves, particle_personalBest[i], global_best, currentFitness,global_best_moves)
				
				# If the particle is lost then it needs to go back to the position that gave the global best
				if retrace == True:
					
					# Convert it to the proper scrambling format.
					# Since we are going back to the position that gave global best,
					# We need to scramble it using original scramble and apply the moves that gave the global best score.
					# The cube will always be reinitailized when we scramble it.
					properScramble = convert2Scramble(originalScramble + particle_velocity[i])
					
					# Find the length of the scramble
					scrambleLength = len(properScramble)	
					
					# Make that scramble and get the orientation
					scramble, cube_orientation = Scramble.scramble(True, properScramble,scrambleLength)
					
					# Since we are retracing the step the only moves applied to the cube is the velocity
					particle_positionMoves[i] = particle_velocity[i]
				
				else:
					# Convert it to the proper scrambling format
					# Here we are going to apply a move to the cube, so we don't need to scramble it from the start.
					properScramble = convert2Scramble(particle_scramble[i] + particle_velocity[i])
					
					# Find the length of the scramble
					scrambleLength = len(properScramble)	
					
					# Make that scramble and get the orientation
					scramble, cube_orientation = Scramble.scramble(True, properScramble, scrambleLength)
					
					# Add the moves that are applied to the cube.
					particle_positionMoves[i] = particle_positionMoves[i] + particle_velocity[i]
				
				# Save the cubes orientation
				particle_position[i] = cube_orientation
				
				# Save the moves that was applied to the cube.
				particle_scramble[i] = scramble
				
				# Print the new cube orientation
				print("After: ", particle_position[i])

				# Update if the particle has beat its best score 
				# and save the moves that gave the best personal best fitness
				if currentFitness < particle_personalBest[i]:
					particle_personalBest[i] = currentFitness
					particle_personalBest_moves[i] = particle_positionMoves[i]
					
				# Update if the particle has beat the global best 
				# and save the moves that gave the global best
				if currentFitness < global_best:
					global_best = currentFitness
					global_best_moves = particle_positionMoves[i]
				
				# If the particle has solved the cube add it to the solution vector.
				if cube_orientation == "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb":
					
					intermediate_time = time.time()	# This is where a particle will find the solved state
					solve_time = intermediate_time - start_time # The time for a particle to find the solution
					
					# The moves applied is a string. So split it by space and remove the last character as it is a space.
					# This is needed to find the length of the solution. 
					# If it was a string then it would count the spaces.
					move = particle_positionMoves[i].split(" ")[:-1]
					solution.append([iteration, i, particle_position[i], particle_positionMoves[i], len(move), solve_time])		

					# The current fitness is the fitness of the cube before the moves were applied.
					# And not the fitness of the cube after the moves were applied.
					# The fitness of the cube after the moves are applied is calculated in the next iteration
					# So if the cube is solved then its fitness will be calculated in the next iteration
					# But in the next iteration, this loop won't get executed if the cube is solved.
					# So we update the personal and global fitness to 0, 
					# immediately after the cube is solved.

					# If the global best is not 0, and cube gets solved, 
					# update the global best.
					# If a particle as already found the solution, then global best was already 0
					# Then we don't need to update the global best again.
					# and the moves needed t reach the global best
					if global_best!=0:
						global_best = 0
						global_best_moves = particle_positionMoves[i]
					
					# Update personal best and the moves needed to reach the personal best
					particle_personalBest[i] = 0
					particle_personalBest_moves[i] = particle_positionMoves[i]

			else:
				# If cube is solved just print personal best and global best and 
				# show the solved state of the cube.
				print("Current Fitness : ", currentFitness,end = " ")
				print("Personal Best : ", particle_personalBest[i],end = " ")
				print("Global Best : ",global_best,end = " ")
				print("NOW : ", particle_position[i])
				
		# Append values for plotting
		# X axis for iteration
		# Y axis for perosnal fitness average
		# Y axis for global fitness. It is saved just before the inner loop starts
		xIter.append(iteration)
		yPersonalFitness.append(personalFitnessSum/nPop)
		yCurrentFitness.append(currentFitnessSum/nPop)
	end_time = time.time()	# This is where the entire PSO loop finishes execution
	total_time = end_time - start_time	# This is the total time needed for the loop execution
	
	# Print the initial cube orientation
	print("\n")
	print("Cube orientation: Yellow on top and green on front.")
	print("Reading order goes: Up, Right, Front, Down, Left, Back.")
	print("Scramble: ", originalScramble)
	print("Initial cube orientation : ",initialOrientation)
	
	# Print the solution vector
	for sol in solution:
		print("\n")
		print("Iterations: ", sol[0])
		print("Particle : ", sol[1])
		print("Cube Orientation : ", sol[2])
		print("Solution : ", sol[3])
		print("Solution length : ", sol[4])
		print("Time : ", sol[5])
		
	"""# Display details for each particle
	for i in range(nPop):
		print("\n")
		print("For particle: ",i)
		print("Particle positions: ",particle_position[i])
		print("Particle prersonal best: ",particle_personalBest[i])
		print("Moves that gave perosnal best: ",particle_personalBest_moves[i])
	
	# Print the global best
	print("\n")
	print("Scaramble: ", originalScramble)
	print("Global best: ", global_best)
	print("Moves that led to global best: ", global_best_moves)"""
	
	# If the solution was not found print the appropriate information
	if len(solution)==0:
		print("\n")
		print("Solution was not found by any particle")
		print("The total number of particles that found solution: ",len(solution),"/",nPop)	# 0 particles solved it
		print("Original Solution Length: ", originalFitness)
		print("Average solution length: NIL")	# Since the solution was not found	
		print("Iteration at which the first solution was found: NIL")	# Since the solution was not found
		print("Iteration at which the last particle found the solution: NIL")	# Since the solution was not found
		print("Average iterations it takes for the next particle to reach solved state: NIL")	# Since the solution was not found
		print("Total time for loop execution : ",total_time)
		print("Minimum Fitnees Reached : ",global_best)
		print("NUMBER OF FUNCTION EVALUATIONS : ",numberOfEvaluations)
	
	# Else if the solution was found
	else:
		# Print the details:
		# Find the average length of the solution
		print("\n")
		sumSol = 0
		for sol in solution:
			sumSol = sumSol + sol[4]
					
		averageSol = sumSol/len(solution)
		
		print("The total number of particles that found solution: ",len(solution),"/",nPop)
		print("Original Solution Length: ", originalFitness)
		print("Average solution length: ", averageSol)	
		
		# Find the average iteration and time it takes for the next particle to reach the solved state
		sumIter = 0
		sumIterTime = 0
		for i in range(len(solution)):
			if (i+1) >= len(solution):
				break
			else:
				sumIter = sumIter + (solution[i+1][0]-solution[i][0])
				sumIterTime = sumIterTime + (solution[i+1][5]-solution[i][5])
		
		averageIter = sumIter/len(solution)
		averageIterTime = sumIterTime/len(solution)
		
		
		# The minimum iteration at which the solution was found and also the maximum iteration	
		print("Iteration at which the first solution was found: ",solution[0][0])		
		print("Iteration at which the last particle found the solution: ", solution[-1][0])
		print("Average iterations it takes for the next particle to reach solved state: ",averageIter)
		print("\n")
		print("Time required to find the first solution : ",solution[0][5],"seconds")	# At the fifth index of the solution vector the time is stored
		print("Total time for PSO loop execution: ", solution[-1][5],"seconds")
		print("Average time it takes for the next particle to reach solved state: ",averageIterTime, "seconds")
		print("NUMBER OF FUNCTION EVALUATIONS : ",numberOfEvaluations)
	
	# Plotting the change of personal best with each iteration for particle
	plt.grid(True)
	plt.semilogx(xIter,yPersonalFitness,c="green",linestyle="-")	# Plot iteration vs personal fitness
	plt.semilogx(xIter,yGlobalFitness,c="blue",linestyle="--",marker="o")	# Plot iteration vs global fitness
	plt.semilogx(xIter,yCurrentFitness,c="red",linestyle=":")	# Plot iteration vs currentFitness
	
	plt.xlabel('Iterations')	# naming the x axis as iterations
	plt.ylabel('Fitness Score')	# naming the y axis as fitness score	
	plt.title('Iterations vs Fitness')	# giving a title to my graph  
	plt.legend(["Personal Fitness AVG","Global Fitness","Current Fitness AVG"])
	#ax = plt.axes()
	plt.yticks(np.arange(0,22,step = 2))
	plt.show()


# Main program
if __name__ == "__main__":
	print("\n")
	print("Particle Swarm Optimization")
	iterations = int(input("Enter the number of iterations : "))
	particles = int(input("Enter the number of particles : "))
	randomOrManual = input("Type M for manual scramble or R for random scramble : ")
	n = int(input("Enter the number of times fitness of cube has to be evaluated : "))
	if randomOrManual == "R":
		flag = False
		scramble = ""
	elif randomOrManual == "M":
		flag = True
		scramble = input("Type scramble : ")
		
	# Function call
	# Add space to the scramble entered by the user, implementation reason.
	PSO(iterations, particles, flag, scramble+" ",n)	# Calling the particle swarm algorithm