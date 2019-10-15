# zirconiumDioxide
An esoteric programming language concept inspired by piet

This was my first attempt creating a programming language, I did it for fun and because I could.
The simple interpreter may not work fully but is at least capable of some simple programs (hello world should work)

Each program file should be a gif. Each frame of the gif is a layer of program code.
Each command is a 4x4 pixel square on a specific layer.

The intention of this language is to be a bit strange but to allow for a program to be build using 3d building blocks e.g. Lego.

Each command is read from the bottom left corner upwards to the top corner then each column in order.


Different colours have meaning.
The reserved colours are:

Red (#ff0000) and Blue (#0000ff) for command codes (to state what action to take)

Green (#00ff00) is for stack reference (telling the program when to use a stack)

Black (#000000) is for flow control (telling the program where to go next)

Purple (#6400c8) is for alternative flow control (if a condition evaluates false it will take this path instead)

Cyan (#00ffff), Yellow (#ffff00) and Magenta (#ff00ff) are for data (tells the program where to look for values)


All other colours that have 100% alpha (except white) are treated as variables but can be used as data or just decoration.
Any colour with less than 100% alpha and white are ignored.


Based on the proportions of red and blue determines the command that is executed. Which one counts as code part 1 depends on which is found first, they do not need to be in any specific position around the command.

There are 2 (technically 3) stacks - a data stack and a 2d screen co-ordinates stack

This language also provides a 16x16 binary pixel display so simple images / animations can be produced. Though it could easily be ommitted as it is probably unecessary.


Commands:

1, 0 - Store Value - uses cyan, yellow and magenta to get values and then stores them in any variables and stacks (in order found)

1, 1 - Push - takes values from cyan, yellow, magenta and variables and then pushes these values onto stacks (in order found)

1, 2 - Pop - takes values from stacks and stores in variables where possible (in order found) and discards the rest

1, 3 - Jump (not relative) - takes three inputs from variables, stacks or data (in order) and jumps the Current Instruction Register to that location

1, 4 - Jump (relative) - same as not relative but moves the Current Instruction Register's x,y,z position by the values instead of setting them

2, 0 - Input (int) - get a single integer input from the user and store in variable or stack (first given)

2, 1 - Input (str) - get a string input from the user - convert each character to ascii-7 code and store in data stack (top item will be first character value) and then store the strings length in the data stack

2, 2 - Output (int) - takes as many values as given from stacks, variables and data and outputs them in order to the console

2, 3 - Output (char) - takes as many values as given and outputs them in order as chars (ascii-7 encoding) with no return after each

3, 0 - Condition = - takes up to 2 values (if one is given 0 is the other) (if none are given it uses data stack and 0 if possible) and progresses the flow via black if they are equal and purple if they aren't

3, 1 - Condition < - takes up to 2 values (if one is given 0 is the other) (if none are given it uses data stack and 0 if possible) and progresses the flow via black if the first is smaller and purple if it isn't

3, 2 - Condition > - takes up to 2 values (if one is given 0 is the other) (if none are given it uses data stack and 0 if possible) and progresses the flow via black if the first is larger and purple if it isn't

4, 0 - Get Pixel - takes 2 values (uses screen stack if missing) and will store the state of that screen pixel (mod 16 for both axes) as 1 or 0 in the data stack

4, 1 - Set Pixel On - takes 2 values (uses screen stack if missing) and will set the state of that screen pixel (mod 16 for both axes) to 1

4, 2 - Set Pixel Off - takes 2 values (uses screen stack if missing) and will set the state of that screen pixel (mod 16 for both axes) to 0

4, 3 - Invert Pixel - takes 2 values (uses screen stack if missing) and will set the state of that screen pixel (mod 16 for both axes) to the inverse of what it currently is


Structure of a command:

Stacks - If a green pixel is in the command it represents a stack usage - where the d's are in the diagram below it represents the data stack while y and x are the y and x axes of the screen position stack
dddd

dyyd

dxxd

dddd


Flow - black or purple in these positions represent a movement of 4 (a whole instruction) in the following directions: f - forward by 4 (y axis), b - backward by 4 (y axis), l - left by 4 (x axis), r - right by 4 (x axis), u - up by one (next frame, z axis), d - down by one (last frame, z axis) 
lf f f rf

l  d u  r

l  d u  r

lb b b rb


Data can be read from any of the edges of the square (not corners) as the number of adjacent pixels matching the colour that is adjacent outwards from the square are totaled and that is the value the data input represents.
e.g.
xxxx

xxxma

xxxx

xxxx

Will count the total number of adjacent pixels matching 'a' and use that as magenta's data input.


As jumping can be done it is possible to shift the program counter (starting bottom left of first frame - which counts 4 up and right) so that a command can be read between commands or as part of a command. I don't know how possible it is to program with this but it could allow for further code efficiency.


It is written in python 3.7 and requires numpy, matplotlib and PIL (non standards) to run.
I doubt anyone will read this and much less have any interest in it but you are more than welcome to use/modify this.
There is no IDE as I am not skilled enough to create one.
I recommend using a gif editor/creator to program in, if for some insane reason you want to try.
