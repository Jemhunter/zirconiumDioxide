def getArea (pixels, x, y):
    '''Count the total amount of ajacent pixels of the same colour'''
    #get starting colour
    startPixel = pixels[y][x]

    #if it wasn't empty
    if startPixel != "E":
        #calculate the total and return it
        allPixels = countAdjacent(pixels, startPixel, x, y, [])
        return len(allPixels)
    else:
        #empty means a value of zero
        return 0


def countAdjacent (pixels, startPixel, x, y, usedList):
    '''Recursively collects all pixel co-ords in a list of the same colour'''
    #add this pixel to the list
    usedList.append((x, y))

    #if the left edge hasn't been reached
    if x > 0:
        #if the left pixel is the same colour and not used yet
        if pixels[y][x - 1] == startPixel and not((x - 1, y) in usedList):
            #calculate for that pixel
            usedList = countAdjacent(pixels, startPixel, x - 1, y, usedList)

    #if the right edge hasn't been reached
    if x < len(pixels[0]) - 1:
        #if the right pixel is the same colour and not used yet
        if pixels[y][x + 1] == startPixel and not((x + 1, y) in usedList):
            #calculate for that pixel
            usedList = countAdjacent(pixels, startPixel, x + 1, y, usedList)

    #if the top edge hasn't been reached
    if y > 0:
        #if the up pixel is the same colour and not used yet
        if pixels[y - 1][x] == startPixel and not((x, y - 1) in usedList):
            #calculate for that pixel
            usedList = countAdjacent(pixels, startPixel, x, y - 1, usedList)

    #if the bottom edge hasn't been reached
    if y < len(pixels) - 1:
        #if the down pixel is the same colour and not used yet
        if pixels[y + 1][x] == startPixel and not((x, y + 1) in usedList):
            #calculate for that pixel
            usedList = countAdjacent(pixels, startPixel, x, y + 1, usedList)

    #return the current list
    return usedList


class command ():
    def __init__ (self, instructions):
        '''Create command object with the instructions, decode to information'''
        self.data = instructions
        #get the command code
        self.code = self.getCode()

        #decode to get data port information
        self.dataUsed = self.getDataPorts()

        #flow control current instruction register movement and false movement
        #z, x, y
        self.cirChange = [0,0,0]
        self.falseCirChange = [0,0,0]

        #get flow movement from instruction
        self.cirChange, self.falseCirChange = self.getFlow()


    def getCode (self):
        '''Get what the instruction is from the data'''
        #default no first colour
        firstColour = ""

        #iterate bottom left, up then right
        for x in range(0, 3):
            for y in range(3, 0, -1):
                #if a first colour hasn't been found yet
                if firstColour == "":
                    #if the colour at this pixel is a code colour
                    if self.data[y][x] in ("r", "b"):
                        #set the first colour
                        firstColour = self.data[y][x]
        
        #default info
        codeInfo = [0,0]

        #if the first is one of the valid colours
        if firstColour in ("r", "b"):
            #iterate across all pixels in instruction
            for y in range(0, len(self.data)):
                for x in range(0, len(self.data[y])):
                    #get the pixel's code
                    code = self.data[y][x]
                    #if it is one of the code colours
                    if code in ("r", "b"):
                        #if it is the same as the first
                        if code == firstColour:
                            #increment first
                            codeInfo[0] = codeInfo[0] + 1
                        else:
                            #increment second
                            codeInfo[1] = codeInfo[1] + 1

        #pass back the number of each colour type
        return codeInfo


    def getFlow (self):
        '''Get the cir changes for false and normal for this instruction'''
        #default values - none
        committedChange = [0, 0, 0]
        committedFalseChange = [0, 0, 0]

        #iterate across instruction - bottom left, up then right
        for xOffset in range (0, 4):
            for yOffset in range (0, -4, -1):
                #get the colour code for this item
                item = self.data[3 + yOffset][xOffset]
                #change for this block
                change = [0, 0, 0]
                #if it is black or purple
                if item in ("bl", "p"):
                    #if it is in the centre two layers
                    if yOffset in (-1, -2):
                        #left side
                        if xOffset == 0:
                            #left
                            change = [0, -4, 0]
                        #right side
                        if xOffset == 3:
                            #right
                            change = [0, 4, 0]
                        #middle left
                        if xOffset == 1:
                            #down
                            change = [-1, 0, 0]
                        #middle right
                        if xOffset == 2:
                            #up
                            change = [1, 0, 0]
                    else:
                        #if it is on the bottom level
                        if yOffset == 0:
                            #bottom middle two
                            if xOffset in (1,2):
                                #backward
                                change = [0, 0, 4]
                            else:
                                #bottom left corner
                                if xOffset == 0:
                                    #backLeft
                                    change = [0, -4, 4]
                                #bottom right corner
                                if xOffset == 3:
                                    #backRight
                                    change = [0, 4, 4]
                        #if it is on the top level
                        if yOffset == -3:
                            #top middle two
                            if xOffset in (1,2):
                                #forward
                                change = [0, 0, -4]
                            else:
                                #top left corner
                                if xOffset == 0:
                                    #forwardLeft
                                    change = [0, -4, -4]
                                #top right corner
                                if xOffset == 3:
                                    #forwardRight
                                    change = [0, 4, -4]

                #if there was a change this pixel
                if change != [0, 0, 0]:
                    #if it was black
                    if item == "bl":
                        #update the normal change
                        committedChange = [change[0], change[1], change[2]]
                    #if it was purple
                    if item == "p":
                        #update the false change
                        committedFalseChange = [change[0], change[1], change[2]]

        #return the final changes (always the last ones found)
        return committedChange, committedFalseChange


    def getDataPorts (self):
        '''Get the positions where data is being read from - not actually getting the data'''
        #possible cyan, magenta, yellow positions that will point at data
        cymPositions = [[0,-1], [0,-2], [1,0], [1,-3], [2,0], [2,-3], [3,-1], [3,-2]]
        #start of data based on the above cym positions (in the same order)
        cymStartPositions = [[-1,-1], [-1,-2], [1,1], [1,-4], [2,1], [2,-4], [4,-1], [4,-2]]

        #the corner coordinates
        corners = [[0, 0], [3, 0], [0, -3], [3, -3]]

        dataList = []

        #iterate for all pixles - bottom left, up then right
        for xOffset in range (0, 4):
            for yOffset in range (0, -4, -1):
                #get the pixel data
                item = self.data[3 + yOffset][xOffset]
                #get the position
                pos = [xOffset, yOffset]

                #if it is stack usage
                if item == "g":
                    #if it is in a data stack position
                    if pos in cymPositions or pos in corners:
                        #add data stack usage
                        dataList.Append("d")
                    else:
                        #if it is in the middle
                        if xOffset in (1,2):
                            #bottom
                            if yOffset == -2:
                                #using x axis of screen stack
                                dataList.append("x")
                            #top
                            if yOffset == -1:
                                #using y axis of screen stack
                                dataList.append("y")

                #if it is a variable
                elif item[0] == "v":
                    #add the variable to the data used
                    dataList.append(item)

                #if it is a data input
                elif item in ("c", "y", "m"):
                    #get the position
                    where = cymPositions.index(pos)
                    #if it is in a valid cym position
                    if where != -1:
                        #add the start position to the list
                        dataList.append(cymStartPositions[where])

        #pass back the list of data usage
        return dataList
                
        
class program ():
    def __init__ (self, fileData, colourControl):
        '''Create new program given a file array and colour control object'''
        #store information from program
        self.pixelData = fileData
        #store colour information object
        self.colours = colourControl

        #create list to hold variable values
        self.variables = [None] * len(self.colours.variableCodes)
        #create empty data stack
        self.dataStack = []
        #create empty 2d screen stack
        self.screenStack = [[],[]]

        #initialize current instruction register to bottom left of first frame (bottom)
        self.CIR = [0,0,len(self.pixelData[0]) - 1]

    def getCodeFromProgram(self, z, x, y):
        '''Returns the colour code present at x(left right) y(forward backward) z (up down) postition'''
        #if each of the parameters are within the program
        if z >= 0 and z < len(self.pixelData):
            if y >= 0 and y < len(self.pixelData[z]):
                if x >= 0 and x < len(self.pixelData[z][y]):
                    #return the pixel data
                    return self.pixelData[z][y][x]
        #if it is not a valid position within the program return an empty
        return "E"

    def buildInstruction(self):
        '''Create 4x4 instruction starting at cir position'''
        #create empty array
        instruction = [["E", "E", "E", "E"],["E", "E", "E", "E"],["E", "E", "E", "E"],["E", "E", "E", "E"]]
        #get positions from cir
        z, x, y = self.CIR

        #iterate for y offset - from bottom to top
        for yOffset in range(0, -4, -1):
            #iterate for x offset - from left to right
            for xOffset in range(0,4):
                #set instruction pixel from value returned by get code function
                instruction[3 + yOffset][xOffset] = self.getCodeFromProgram(z,x + xOffset, y + yOffset)

        #return the completed instruction
        return instruction

    def getCommandFromInstruction(self, instruction):
        '''Convert a set of instructions into a command object'''
        comm = command(instruction)
        return comm
    
    def getCommand (self):
        '''Create a new command'''
        #get the instruction data
        inst = self.buildInstruction()
        #convert to a command
        instCommand = self.getCommandFromInstruction(inst)
        #return the command
        return instCommand

    def getVariable (self, varName):
        '''Get the variable with the var name'''
        #attempt - so if an incorrect name is given an error isn't thrown
        try:
            #remove v from the front of the variable name to leave the number
            #convert to an integer
            num = int(varName[1:])
            #return the variable value
            return self.variables[num]
        #if an error occurs - cannot convert to int or not in range
        except:
            return None

    def setVariable (self, varName, value):
        '''Set a variables value'''
        #attempt - so error isn't thrown if there is no variable
        try:
            #get the position of the variable
            #split off leading v
            #convert to int
            num = int(varName[1:])
            #set the value of that variable
            self.variables[num] = value
        except:
            #if an error occurs - do nothing
            pass

    def getScreenStack (self, pos):
        '''Pop the last value from a screen stack and return it'''
        #attempt - in case an error occurs
        try:
            #if there is an item in the stack
            if len(self.screenStack[pos]) > 0:
                #pop the last item
                item = self.screenStack[pos].pop()
                #return the item
                return item
        except:
            #return nothing if an error occurred
            return None
        #if it doesn't produce an error but there weren't any items
        return None

    def addToScreenStack (self, pos, item):
        '''Add a value to the end of a screen stack'''
        #attempt - in case pos is not a correct value
        try:
            #add the item to the end of the list
            self.screenStack[pos].append(item)
        except:
            #if an error occurrs - do nothing
            pass

    def getDataStack (self):
        '''Pop the last item off the data stack'''
        try:
            #if there is an item in the stack
            if len(self.dataStack) > 0:
                #pop the last item
                item = self.dataStack.pop()
                #return the item
                return item
        except:
            #if an error occurred
            return None
        #no error but also no items in stack
        return None

    def addToDataStack(self, item):
        '''Add an item to the data stack'''
        self.dataStack.append(item)

    def countAdjacentSimilar(self, xChange, yChange):
        '''Count the number of nearby adjacent pixels of the same colour'''
        #get start position values
        x = self.CIR[1] + xChange
        y = self.CIR[2] + yChange
        z = self.CIR[0]

        #call for total calculation
        total = getArea(self.pixelData[z], x, y)
        return total

    def setCIR (self, changes, relative):
        '''Change the CIR manually both zxy'''
        #if there are enough items to change by
        if len(changes) > 2:
            #if it is a relative change
            if relative:
                #change the CIR - modify
                self.CIR[0] = self.CIR[0] + changes[0]
                self.CIR[1] = self.CIR[1] + changes[1]
                self.CIR[2] = self.CIR[2] + changes[2]
            else:
                #change the CIR - overwrite
                self.CIR[0] = changes[0]
                self.CIR[1] = changes[1]
                self.CIR[2] = changes[2]
        
class colourSetup ():
    def __init__ (self):
        '''Create colour controller'''
        #setup all default colours
        self.red = (255, 0, 0, 255)
        self.blue = (0, 0, 255, 255)
        self.green = (0, 255, 0, 255)
        self.black = (0, 0, 0, 255)
        self.purple = (100, 0, 200, 255)
        self.cyan = (0, 255, 255, 255)
        self.yellow = (255, 255, 0, 255)
        self.magenta = (255, 0, 255, 255)
        #setup empty variables
        self.variableCodes = []
        self.variableColours = []

    def getVariable (self, colour):
        '''Get a variable name given a colour'''
        #iterate variable colours
        for varColour in range(0, len(self.variableColours)):
            #if the colour matches
            if self.variableColours[varColour] == colour:
                #return the variable name
                return self.variableCodes[varColour]
        #if none was found create a new variable
        return self.addVariable(colour)
    
    def getColourCode (self, colour):
        '''Get the id name for a colour'''
        #default colours
        if colour == self.red:
            return "r"
        if colour == self.blue:
            return "b"
        if colour == self.green:
            return "g"
        if colour == self.black:
            return "bl"
        if colour == self.purple:
            return "p"
        if colour == self.cyan:
            return "c"
        if colour == self.yellow:
            return "y"
        if colour == self.magenta:
            return "m"
        #if not a default get the variable colour
        varColourName = self.getVariable(colour)
        #return the variable
        return varColourName
    
    def addVariable (self, colour):
        '''Create a new variable'''
        #iterate for colours in the variables
        for varColour in range(0, len(self.variableColours)):
            #if the colour matches
            if self.variableColours[varColour] == colour:
                #return the colour id - not added just found
                return self.variableCodes[varColour]

        #create new variable name
        varName = "v" + str(len(self.variableCodes))
        #add to lists
        self.variableCodes.append(varName)
        self.variableColours.append(colour)
        #return the id
        return varName
