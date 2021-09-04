# Swarm-Intelligence-Algorithms-For-The-Rubik-s-Cube-2
New code with some minor changes and bug fixes

# Swarm-Intelligence-Algorithms-for-Solving-Rubik-s-Cube
Particle swarm optimization, greedy tree search, ant colony optimization and krill herd optimization algorithms for solving the Rubik's cube. <br>
M.Tech final year project done under the guidance of Dr. Madhu S. Nair during the academic year 2020-2021. <br>
Made a few changes to the code for the repository [https://github.com/JishnuJeevan/Swarm-Intelligence-Algorithms-for-Solving-Rubik-s-Cube]

## Code
The repository contains codes for the following swarm intelligence algorithms. 
1. Particle Swarm Optimization, which can be found in the file 1_PSO.py
2. Greedy Tree Search, which can be found in the file 2_GREEDY.py
3. Ant Colony Optimization, which can be found in the file 3_ACO.py
4. Krill Herd Optimization, which can be found in the file 4_KHO.py
The code is a modified version of the orginal algorithms and they are written in such a way that they can solve the Rubik's cube.

## Kociemba's Algorithm
When Kociemba's algorithm is used to solve the cube, it returns more than one solution for some cube state. The file 0_KociembaStats.py is used to run the Kociemba's algorithm n times on the cube state to get n different solution length and to find out the mean, mode, standard deviation etc of these solution lengths.  

## Running the code
To run the code for the PSO just type `python 1_PSO.py` <br>
To run the code for greedy tree search type `python 2_GREEDY.py` <br>
To run the code for ACO just type `python 3_ACO.py` <br>
To run the code for KHO just type `python 4_KHO.py` <br>
To run the code for doing analaysis of Kociemba's algorithm just type `python 0_KociembaStats.py` <br>
NOTE: When you first run the program, the program will generate databases and look up tables. This might take an hour or so. These databases and look up tables contain different configurations of the cube which is used by the Kociemba algorithm for solving it. <br>
The Kociemba algorithm here is used for finding the fitness of the cube i.e. the number of moves needed to solve the cube from the current state.

## Providing scrambles to the cube
When we run the PSO, greedy, ACO or the KHO algorithm we need to scramble the cube and give it to the algorithm so that it can solve it. Scrambles can be provided either manually or generated within the program randomly. Each program will ask the user to type M for providing a manual scramble or type R for providing random scrambles.
1. For random scrambles <br>
1.1. Type R for giving the algorithm random scramble. <br>
1.2. This will give the algorithm a randomly generated scramble. <br>
1.3. The length of the scramble can be anywhere between 5 and 30 moves. <br>
1.4. To change the length of the scramble you can go to the file scrambleGenerator.py and go to line no. 11. In the code `slen = random.randint(5,30)` you can provide two numbers and the algorithm will generate scrambles of length within the provided range. <br>
2. For manual scramble <br>
2.1. Type M for giving manual scrambles to the cube. <br>
2.2. When giving manual scrambles the user must type the scrabmbles for the algorithm.  <br>
2.3. The letters for the scramle must be capital and there should be a space between each move. <br>
2.4. Valid letters are R for right side, L for left side, U for up, D for down, F for front and B for back. <br>
2.5. Letter can have an apostrophe ( ' ) next to it which says to turn that side anti-clockwise and letters with the number 2 next to it is denoting that, the side should be turned twice. This should be provided next to the letter without space. <br>
3. Valid and invalid scrambles. <br>
3.1. Example of a valid scrambles: R' L D2 U F B2 R L2 U2 <br>
3.2. Invalid scramble: <br>
3.2.1. RL - No space between each move. There should be space between each move. <br>
3.2.2. r l - Letters are small letters. Every letter should be captial. <br>
3.2.3. R ' - This is invalid as there is space between the letter and the apostrophe. There should not be a space between the letter and the apostrophe. Correct way to write it is R' <br>
3.2.4. R 2 - This is invalid as there is space between the letter and the number 2. There should not be a space between the letter and the the number 2. Correct way to write it is R2 <br>

## Orientation of the cube.
A standard Rubik's cube will have the following color scheme: Yellow on top, white on bottom, green on front, blue on back, red on left and orange on right. <br>
So in the code the cube is scrambled with the following orientation: Yellow on top and green on front. <br>
When the algorithm is running it will output the orientation of the cube during each itertion for each particle. The orientation denotes where the stickers of the cube are. <br>
The orientation outputed by the program is a string. The solved cube will have the following orientation "yyyyyyyyyooooooooogggggggggwwwwwwwwwrrrrrrrrrbbbbbbbbb". <br>
The first 9 characters denotes the colors on the top side of the cube which is yellow, "yyyyyyyyy". <br>
The next 9 characters denotes the color of the right side of the cube which is orange, ooooooooo. <br>
The next 9 characters is for the front side of the cube which is green, "ggggggggg". <br>
Then next 9 is for the bottom side which is white "wwwwwwwww". <br>
Then next 9 is for the left side which is red, "rrrrrrrrr". <br>
And finally the last 9 characters denote the colors of the back side which is blue, "bbbbbbbbb". <br>
The colors are read in order Up, Right, Front, Down, Left, Back. <br>
If we open up the cube then we will get the following orientation with U for up, L for left, F for front, R for right, B for back and D for down.<br>
&emsp;&emsp;&emsp; | U | U | U | <br>
&emsp;&emsp;&emsp; | U | U | U | <br>
&emsp;&emsp;&emsp; | U | U | U | <br>
| L | L | L | F | F | F | R | R | R | B | B | B | <br>
| L | L | L | F | F | F | R | R | R | B | B | B | <br>
| L | L | L | F | F | F | R | R | R | B | B | B | <br>
&emsp;&emsp;&emsp; | D | D | D | <br>
&emsp;&emsp;&emsp; | D | D | D | <br>
&emsp;&emsp;&emsp; | D | D | D | <br>
and if yellow is on top and green on front then we will get the following orientation <br>
&emsp;&emsp;&emsp; | y | y | y | <br>
&emsp;&emsp;&emsp; | y | y | y | <br>
&emsp;&emsp;&emsp; | y | y | y | <br>
| r | r | r | g | g | g | o | o | o | b | b | b | <br>
| r | r | r | g | g | g | o | o | o | b | b | b | <br>
| r | r | r | g | g | g | o | o | o | b | b | b | <br>
&emsp;&emsp;&emsp; | w | w | w | <br>
&emsp;&emsp;&emsp; | w | w | w | <br>
&emsp;&emsp;&emsp; | w | w | w | <br>
and we can use numbers from 1 to 9 denoting the order for reading the color for each side of the cube <br>
&emsp;&emsp;&emsp; | 1 | 2 | 3 | <br>
&emsp;&emsp;&emsp; | 4 | 5 | 6 | <br>
&emsp;&emsp;&emsp; | 7 | 8 | 9 | <br>
| 1 | 2 | 3 | | 1 | 2 | 3 | | 1 | 2 | 3 | | 1 | 2 | 3 | <br>
| 4 | 5 | 6 | | 4 | 5 | 6 | | 4 | 5 | 6 | | 4 | 5 | 6 | <br>
| 7 | 8 | 9 | | 7 | 8 | 9 | | 7 | 8 | 9 | | 7 | 8 | 9 | <br>
&emsp;&emsp;&emsp; | 1 | 2 | 3 | <br>
&emsp;&emsp;&emsp; | 4 | 5 | 6 | <br>
&emsp;&emsp;&emsp; | 7 | 8 | 9 | <br>
were we read the colors on the top side first, then the right side, then the front side, then the down side, then the left side and finally the back side.

# Code Reference
1. The code for scrambling the cube is taken from: [https://github.com/BenGotts/Python-Rubiks-Cube-Scrambler]
2. The code for the fitness function (Kociemba Algorithm) is taken from: [https://github.com/hkociemba/RubiksCube-TwophaseSolver]

# Changes made
1. The file 0_KociembaStats.py is used to run the Kociemba's algorithm n times on the cube state to get n different solution length and to find out the mean, mode, standard deviation etc of these solution lengths. This is to determine the appropriate number of times the cube state should be evaluted since Kociemba's algorithm returns more than one solution for a cube state. The distance between the current state of the cube and the solved state is used as the fitness value by the swarm intelligence algorithms.
2. Originally the distance between the current state of the cube and the solved state is used as the fitness value. Now we run the Kociemba's algorithm n times on the cube state and the rounded average of these n values is taken as the fitnes value of the cube state. Suitable value for n are 1, 2 or 3. If n is set to 3 the ACO and KHO will take hours to solve the cube. It also depends on the number of iterations and the krills (or the ants) used by the algorithm. Therefore it would be better to set the value of n to 1. 
3. Each algorithm prints the total number of times the Kociemba's algorithm was called.
4. When the cube is solved the fitness value returned by Kociemba's algorithm was 1. This mistake has been rectified and now it returns 0.
5. Changes have been made to the graphs that plot the change in fitness value with iteration.

