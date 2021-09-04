import FitnessFunction as fit
import Scramble 
from scrambleGenerator import makeMove
import statistics	# For finding mean, standard deviation, variance, and mode
import time	# To calculate the time taken by the algorithm for execution


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


def calculateDistribution(values):
	"""
	This function will calculate the percetage of the minimum fitness value,
	and the mode value from the sample of fitness values
	"""
	# Create a dictionary to hold the fitness values and the count
	valueCounter = {}

	# Take every element in the array
	for ele in values:
		# If it is not in the dictionary 
		# Then set its value as 1
		if ele not in valueCounter:
			valueCounter[ele] = 1
		
		# Else increment its value by 1
		else:
			valueCounter[ele]+= 1
	
	# Now take the minimum value in the dictionary and the mode value from the list of values
	minValue = min(values)
	modeValue = statistics.mode(values)

	# We have found the total occurance of the minimum values and the mode values 
	# and we have saved them in the dictionary
	# Now divided by the total number of values to get the percentage
	minPer = (valueCounter[minValue]/len(values))*100
	modePer = (valueCounter[modeValue]/len(values))*100
	return minPer, modePer


def kociembaStats(n, flag, scramble):
	"""
	This function takes in three parameters.
	n - number of times the Kociemba's algorithm needs to be called for a cube state
	flag - to determine if the scramble is a manual or a random scramble
	scramble - cube scramble
	In this program the Kociemba's algorithm will be called n times for a particular cube state.
	After it has been called n times the stats are returned like:
	Average of the fitness values, variance, standard devaition, minimum fitness value, attmepts needed to find the minimum fitness value etc.
	"""

	# If it is a random scramble
	if flag == False:
		# This returns the scramble and the orientation of the stickers in the cube
		scramble, cube_orientation = Scramble.scramble(flag,scramble,0)
	
	# Else if it is a manual scramble
	else:
		# Now apply the move to the cube
		properScramble = convert2Scramble(scramble)
		
		# Find the length of the scramble
		noofMmoves = len(properScramble)	
		
		# Make that scramble and get the orientation
		scramble, cube_orientation = Scramble.scramble(flag, properScramble, noofMmoves)
	
	# Save the scramble used
	originalScramble = scramble
	
	# Save the initial cube orientation
	initialOrientation = cube_orientation

	# Now we need a to have an array that will store the fitness values,
	# each time Kociemba's algorithm is executed
	values = []

	# Run this loop based on the value of n
	start_time = time.time()	# This is were the execution begins
	for i in range(n):
		# Find the fitness of the current orientation
		# And save it in the array
		fitnessValue = fit.fitness(cube_orientation)
		values.append(fitnessValue)
	end_time = time.time()	# This is were the execution begins
	
	# Print the stats
	print("\n")
	print("Scramble : ", originalScramble)
	print("Orientation : ",initialOrientation)
	print("Fitness values : ",values)
	print("\n")
	
	# Print the stats
	print("Minimum Fitness : ",min(values))
	print("Maximum Fitness : ",max(values))
	print("Mode of the values : ",statistics.mode(values))
	print("Attempt at which the minimum fitness was found : ",values.index(min(values))+1)
	print("Mean of the fitness values : ",statistics.mean(values))
	print("Standard Devaition of the fitness values : ",statistics.stdev(values))
	print("Variance of the fitness values : ",statistics.variance(values))

	# Print the percentage of minimum values in the sample
	# Print the percentage of mode values in the sample
	minPer, modePer = calculateDistribution(values)
	print("Percentage of minimum values : ", minPer)
	print("Percentage of mode value : ",modePer)	
	print("Total Time : ",end_time - start_time)


# Main program
if __name__ == "__main__":
	print("\n")
	print("Stats for Kociemba's algorithm")
	n = int(input("Enter the number of times Kociemba needs to be called : "))
	randomOrManual = input("Type M for manual scramble or R for random scrabmle : ")
	if randomOrManual == "R":
		flag = False
		scramble = ""
	elif randomOrManual == "M":
		flag = True
		scramble = input("Type scramble : ")
		
	# Function call
	# Add space to the scramble entered by the user, implementation reason.
	# Calling the function to find the stats regarding Kociemba's algorithm
	kociembaStats(n, flag, scramble+" ")	
	