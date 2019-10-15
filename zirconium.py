import PIL
from PIL import Image
import numpy
import matplotlib.pyplot as plot
import random
import time
from objects import command
from objects import program
from objects import colourSetup


def newColourSetup():
    '''Create a new colour controller and return it'''
    colours = colourSetup()
    return colours


def getFile(fileName):
    '''Retrive the data from a file and return as id array and colour control'''
    #attempt to get the file
    try:
        #open the gif file
        gif = Image.open(fileName)
        #get the dimensions of the file
        width, height = gif.size

        #array to store pixels in
        framePixels = []
        #not finished getting frames
        done = False

        #get the first frame
        framePixels.append(list(gif.convert("RGBA").getdata()))
        #while there are still frames left to get
        while not done:
            #attempt to get the next frame
            try:
                #seek to next frame
                gif.seek(gif.tell() + 1)
                #append data to pixels
                framePixels.append(list(gif.convert("RGBA").getdata()))
            except:
                #if an error occured then the eof was reached so it is done
                done = True

        #iterate for each of the frames
        for frame in range(0, len(framePixels)):
            #create a new frame list to hold the information
            newFrame = []
            #empty row holder
            row = []
            #a counter to keep the shape
            current = 0
            #iterate for the pixels in that frame
            for colourValue in range(0, len(framePixels[frame])):
                #get the colour for the current pixel
                colour = framePixels[frame][colourValue]
                #add to the current row
                row.append(colour)
                #increase current
                current = current + 1

                #if the end of the row is reached
                if current >= width:
                    #add row to the frame
                    newFrame.append(row)
                    #empty row and reset counter
                    row = []
                    current = 0
            #add the re-ordered frame to the pixel data (replace old)
            framePixels[frame] = newFrame

        #create a colour control object
        colours = newColourSetup()

        #iterate for each pixel in the image
        for frame in range(0, len(framePixels)):
            for row in range(0, len(framePixels[frame])):
                for pixel in range(0, len(framePixels[frame][row])):
                    #get the colour associated with that pixel (R, G, B, A)
                    pixelData = framePixels[frame][row][pixel]

                    #default code is empty "E"
                    code = "E"

                    #if the pixel has 100% alpha it is read (but not white)
                    if pixelData[3] == 255 and pixelData != (255, 255, 255, 255):
                        #get the code for that colour
                        #- variable if not default
                        #- creates new variable if not present
                        code = colours.getColourCode(pixelData)

                    #replace the pixel data with it's code
                    framePixels[frame][row][pixel] = code
        
        #return the pixel data and the colour control object
        return framePixels, colours

    #if an error occured loading the file            
    except:
        #output error to user
        print("File error occurred. Check the file exists and that it is formatted correctly.")
        #return nothing so the program doesn't try to run with broken data
        return None, None


def createNewPlot():
    '''Close all existing plots and create a new 15x15 plot with no axis labels'''
    #close any plots that are open
    plot.close("all")
    #create a new numpy array that is all zeros
    screenObj = numpy.zeros((16, 16))

    #set the plot to interactive mode - keeps window responsive between draws
    plot.ion()
    #get the frame of the plot
    frame1 = plot.gca()
    #remove axis labels
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])

    #return the screen object so it can be edited and re-drawn
    return screenObj


def endPlot():
    '''Close all plots'''
    plot.close("all")


def updatePlot(screenObj):
    '''Update the current plot to show current data'''
    #draw as binary format
    plot.imshow(screenObj, cmap='binary')
    #show the plot but don't block
    plot.show(block = False)


def setPixel(x, y, data, screenObj):
    '''Set a pixel at x and y position from bottom left to specific value in screen'''
    #if a valid screen array was passed
    if screenObj.all() != None:
        #if the x and y values are in the screen
        if x > -1 and x < 16 and y > -1 and y < 16:
            #as matplotlib swaps x and y and inverts y switch them like this
            screenObj[15 - y, x] = data


def invertPixel(x, y, screenObj):
    '''Invert a pixel at x and y position in the screen object'''
    #if a valid screen array was passed
    if screenObj.all() != None:
        #if x and y values are in the screen
        if x > -1 and x < 16 and y > -1 and y < 16:
            #if it was on
            if screenObj[15 - y, x] == 1:
                #turn it off
                screenObj[15 - y, x] = 0
            else:
                #turn it on
                screenObj[15 - y, x] = 1


def getPixel (x, y, screenObj):
    '''Get a specific pixels value'''
    #if a valid screen array was passed
    if screenObj.all() != None:
        #if x and y values are in the screen
        if x > -1 and x < 16 and y > -1 and y < 16:
            #return the integer value of the screen point
            return int(screenObj[x, 15 - y])
    #if not valid
    return -1
    

def output(letter):
    '''Print a letter with no return character'''
    print(letter, end="")


def outputNumber(number):
    '''Print a number with a return character'''
    print(number)


def convertIntChar(num):
    '''Convert an integer to a character using 7 bit ascii table'''
    #if it is an integer
    if type(num) == type(0):
        #MOD by 128 to limit to 7 bit ascii
        num = num % 128
        #return as a character
        return(chr(num))

    #if it is a string
    if type(num) == type(""):
        #if there is only one character
        if len(num) == 1:
            #return the character
            return num
    
    #return a question mark as a number or char was not given
    return "?"


def convertCharInt(char):
    '''Convert a single character to an integer'''
    #if it is a string
    if type(char) == type(""):
        #if it is only one character
        if len(char) == 1:
            #convert to ascii value
            num = ord(char)
            #MOD by 128 to limit to 7 bit ascii
            num = num % 128
            #return the ascii value
            return num
    #no valid character given so give -1
    return -1


def inputNumber():
    '''Take input from user that is an integer number'''
    #valid input has not yet been given
    valid = False
    #nothing in input yet
    inp = ""

    #repeat until a valid number is entered
    while not valid:
        #get input from user
        inp = input("<int>:")
        #if it is a number
        if inp.isdigit():
            #valid input was given
            valid = True
            #cast to integer
            inp = int(inp)

    #return the input value
    return inp


def inputString():
    '''Take input from user that is a string'''
    #valid input has not yet been given
    valid = False
    #nothing in input yet
    inp = ""

    #until something has been entered
    while not valid:
        #get input from user
        inp = input("<str>:")
        #if something was entered
        if len(inp) > 0:
            #input is valid
            valid = True

    #return the entered string
    return inp

def getValue (dataType, prog):
    '''Retrieve data value from the program'''
    #no data to begin with
    item = None

    #if it is data stack
    if dataType == "d":
        item = prog.getDataStack()
    #if it is x axis of the screen stack
    elif dataType == "x":
        item = prog.getScreenStack(0)
    #if it is y axis of the screen stack
    elif dataType == "y":
        item = prog.getScreenStack(1)
    #if it is a data starter
    elif type(dataType) == type([]):
        item = prog.countAdjacentSimilar(dataType[0], dataType[1])
    #if it is a variable
    elif dataType[0] == "v":
        item = prog.getVariable(dataType)

    #return the item
    return item

def storeValue (dataType, value, prog):
    '''Store a value in the program'''
    #if it is data stack
    if dataType == "d":
        prog.addToDataStack(value)
    #if it is x axis screen stack
    elif dataType == "x":
        prog.addToScreenStack(0, value)
    #if it is y axis screen stack
    elif dataType == "y":
        prog.addToScreenStack(1, value)
    #if it is a variable
    elif dataType[0] == "v":
        prog.setVariable(dataType, value)


def splitOutData (dataList):
    '''Split the data list into others and data input (cym)'''
    #create lists to hold data
    normalList = []
    dataInList = []

    #iterate items
    for item in dataList:
        #if it is a cym
        if type(item) == type([]):
            #add to data inputs
            dataInList.append(item)
        else:
            #add to others
            normalList.append(item)

    #return data lists
    return normalList, dataInList

def splitOutStacks (dataList):
    '''Split  the data list into others and stacks'''
    #create lists to hold data
    normalList = []
    stackList = []

    #iterate items
    for item in dataList:
        #if it is a stack
        if item in ("d", "x", "y"):
            #add to stacks list
            stackList.append(item)
        else:
            #add to others
            normalList.append(item)

    #return the data lists
    return normalList, stackList

def attemptDataGet(dataList, num, prog):
    '''Try to get num number of data items using the data list from the program'''
    #list to hold stored data values
    data = []
    #iterate data list
    for item in dataList:
        #if the number hasn't been reached (don't get unnecessary data)
        if len(data) < num:
            #get the value
            value = getValue(item, prog)
            #if the value does exist
            if value != None:
                #add data to the list
                data.append(value)

    #return all the data
    return data


def getScreenPosition(dataList, prog):
    '''Attempt to get a screen position from the memory'''
    #attempt with override data items
    data = attemptDataGet(dataList, 2, prog)
    #if none were provided (or found)
    if len(data) == 0:
        #get data from x and y stack - could be None
        xData = getValue("x", prog)
        yData = getValue("y", prog)
        data = [xData, yData]
    else:
        #if there is only one
        if len(data) == 1:
            #fill with zero
            data.append(0)
        else:
            #truncate excess data (not necessary but will prevent error behaviour)
            data = [data[0], data[1]]
    #pass back the retrieved data
    return data


def runProgram (prog, screen):
    '''Run the passed program until termination'''
    #it is currently running
    running = True
    lastTime = 0

    #repeat until the end is reached
    while running:
        lastTime = time.time()
        #get the next command from the program
        thisCommand = prog.getCommand()
        #get the code for what to do
        code = thisCommand.code

        #get the list of data addresses from the command
        dataList = thisCommand.dataUsed

        #whether or not the program jumped during the command
        jumped = False

        #code first part is 1 - stores/data transfers/jumps
        if code[0] == 1:
            if code[1] == 0:
                #store value
                #split into where to store and data inputs
                storeIn, getFrom = splitOutData(dataList)
                #get all the possible data from the inputs up to store length
                data = attemptDataGet(getFrom, len(storeIn), prog)
                #which store position has been reached
                pos = 0
                #iterate retrived data items (should never exceed length of storeIn)
                for dataItem in data:
                    #store value
                    storeValue(storeIn[pos], dataItem, prog)
                    #increment position counter
                    pos = pos + 1
            elif code[1] == 1:
                #push onto stack
                getFrom, pushTo = splitOutStacks(dataList)
                #get all possible data from inputs up to stacks length
                data = attemptDataGet(getFrom, len(pushTo), prog)
                pos = 0
                #iterate retrived data items (should never exceed length of storeIn)
                for dataItem in data:
                    #push value to stack
                    storeValue(pushTo[pos], dataItem, prog)
                    #increment position counter
                    pos = pos + 1
            elif code[1] == 2:
                #pop from stack
                #split into not stack and stack
                notStack, popFrom = splitOutStacks(dataList)
                #split into store in (vars) and unused (cym)
                storeIn, notUsed = splitOutData(notStack)
                #get all possible data items
                data = attemptDataGet(popFrom, len(storeIn), prog)
                pos = 0
                #for all the data retrieved (should never exceeed len(storeIn))
                for dataItem in data:
                    #store value in variable
                    storeValue(storeIn[pos], dataItem, prog)
                    #increment position counter
                    pos = pos + 1
            elif code[1] == 3:
                #jump (non relative)
                if len(dataList) > 2:
                    #get data (xyz)
                    data = attemptDataGet(dataList, 3, prog)
                    #fill with 0 up to 3
                    for i in range(0, 3 - len(data)):
                        data.append(0)
                    #invert y axis so 0 is bottom not top
                    data[1] = len(prog.pixelData[0]) - 1 - data[1]
                    #jump (should always happen but will prevent errors)
                    if len(data) > 2:
                        #re-order (xyz -> zxy)
                        data = [data[2], data[0], data[1]]
                        #call for change
                        prog.setCIR(data, False)
                        #program has jumped
                        jumped = True
                    
            elif code[1] == 4:
                #jump (relative)
                if len(dataList) > 2:
                    #get data (xyz)
                    data = attemptDataGet(dataList, 3, prog)
                    #fill with 0 up to 3
                    for i in range(0, 3 - len(data)):
                        data.append(0)
                    #invert y axis
                    data[1] = -data[1]
                    #jump (should always happen but will prevent errors)
                    if len(data) > 2:
                        #re-order (xyz -> zxy)
                        data = [data[2], data[0], data[1]]
                        #call for change
                        prog.setCIR(data, True)
                        #program has jumped
                        jumped = True
                
        elif code[0] == 2:
            if code[1] == 0:
                #input int
                value = inputInt()
                #not completed yet
                done = False
                #iterate data store locations
                for destination in dataList:
                    #if it hasn't finished yet
                    if not done:
                        #if it isn't a data input
                        if type(destination) != type([]):
                            #store the value
                            storeValue(destination, value, prog)
                            #store has finished
                            done = True
            elif code[1] == 1:
                #input str
                string = inputString()
                #list to hold numeric values
                nums = []
                #iterate for characters
                for letter in string:
                    #add character converted to an integer to the list
                    nums.append(convertCharToInt(char))
                #reverse the list (first character will be at top)
                nums = nums[::-1]
                #add the number of characters stored
                nums.append(len(nums))
                #iterate values
                for number in nums:
                    #add to data input stack
                    storeValue("d", number, prog)
            elif code[1] == 2:
                #output int
                #get all data possible
                data = attemptDataGet(dataList, len(dataList), prog)
                #iterate retrieved data
                for dataItem in data:
                    #output the numbers
                    outputNumber(dataItem)
            elif code[1] == 3:
                #output char
                #get all data possible
                data = attemptDataGet(dataList, len(dataList), prog)
                #iterate retrieved data
                for dataItem in data:
                    #output the values as characters
                    output(convertIntChar(dataItem))
        
        elif code[0] == 3:
            if code[1] == 0:
                #equal
                #get two data if possible
                data = attemptDataGet(dataList, 2, prog)
                #if none found
                if len(data) < 1:
                    #try data stack
                    data = attemptDataGet(["d"], 1, prog)
                #fill with 0 up to 2 items
                for i in range(0, 2 - len(data)):
                    data.append(0)
                #if there are at least two (should be unnecessary but prevents errors)
                if len(data) > 1:
                    #if they are not the same
                    if data[0] != data[1]:
                        #get false change
                        change = thisCommand.falseCirChange
                        #modify cir by change
                        prog.setCIR(change, True)
                        #a movement has occurred so don't do normal change
                        jumped = True
            elif code[1] == 1:
                #less than
                #get two data if possible
                data = attemptDataGet(dataList, 2, prog)
                #if none found
                if len(data) < 1:
                    #try data stack
                    data = attemptDataGet(["d"], 1, prog)
                #fill with 0 up to 2 items
                for i in range(0, 2 - len(data)):
                    data.append(0)
                #if there are 2 items (unnecessary but prevents errors)
                if len(data) > 1:
                    #if both are integers - cannot compare < / > with others
                    if type(data[0]) == int and type(data[1]) == int:
                        #if 1 is greater than or equal
                        if data[0] >= data[1]:
                            #get false change
                            change = thisCommand.falseCirChange
                            #modify cir by change
                            prog.setCIR(change, True)
                            #a movement has occurred so don't do normal change
                            jumped = True
            elif code[1] == 2:
                #greater than
                #get two data if possible
                data = attemptDataGet(dataList, 2, prog)
                #if none found
                if len(data) < 1:
                    #try data stack
                    data = attemptDataGet(["d"], 1, prog)
                #fill with 0 up to 2 items
                for i in range(0, 2 - len(data)):
                    data.append(0)
                #if there are two items (unnecessary but prevents errors)
                if len(data) > 1:
                    #if both are integers - cannot compare < / > with others
                    if type(data[0]) == int and type(data[1]) == int:
                        #if 1 is less than or equal
                        if data[0] <= data[1]:
                            #get false change
                            change = thisCommand.falseCirChange
                            #modify cir by change
                            prog.setCIR(change, True)
                            #a movement has occurred so don't do normal change
                            jumped = True
        
        elif code[0] == 4:
            if code[1] == 0:
                #get pixel
                #get position (from data first, default to stacks)
                position = getScreenPosition(dataList, prog)
                #if 2 position values were given
                if len(position) > 1:
                    #if both values are integers
                    if type(position[0]) == int and type(position[1]) == int:
                        #mod both by 16 (to limit to the screen)
                        position[0] = position[0] % 16
                        position[1] = position[1] % 16
                        #get the value of the pixel
                        value = getPixel(position[0], position[1], screen)
                        #store in data stack
                        storeValue("d", value, prog)
            elif code[1] == 1:
                #set pixel on
                #get position (from data first, default to stacks)
                position = getScreenPosition(dataList, prog)
                #if 2 position values were given
                if len(position) > 1:
                    #if both values are integers
                    if type(position[0]) == int and type(position[1]) == int:
                        #mod both by 16 (to limit to the screen)
                        position[0] = position[0] % 16
                        position[1] = position[1] % 16
                        #get the value of the pixel
                        setPixel(position[0], position[1], 1, screen)
            elif code[1] == 2:
                #set pixel off
                #get position (from data first, default to stacks)
                position = getScreenPosition(dataList, prog)
                #if 2 position values were given
                if len(position) > 1:
                    #if both values are integers
                    if type(position[0]) == int and type(position[1]) == int:
                        #mod both by 16 (to limit to the screen)
                        position[0] = position[0] % 16
                        position[1] = position[1] % 16
                        #get the value of the pixel
                        setPixel(position[0], position[1], 0, screen)
            elif code[1] == 3:
                #invert pixel
                #get position (from data first, default to stacks)
                position = getScreenPosition(dataList, prog)
                #if 2 position values were given
                if len(position) > 1:
                    #if both values are integers
                    if type(position[0]) == int and type(position[1]) == int:
                        #mod both by 16 (to limit to the screen)
                        position[0] = position[0] % 16
                        position[1] = position[1] % 16
                        #get the value of the pixel
                        invertPixel(position[0], position[1], screen)
        elif code[0] == 16 or code[0] == 0:
            #halt
            running = False

        #change cir to next instruction (if not jumped)
        if not jumped:
            #get the change from the command
            change = thisCommand.cirChange
            #change the cir of the program
            prog.setCIR(change, True)

        #get the time since last update
        waitTime = 0.25 - (time.time() - lastTime)
        #if the wait time is negative
        if waitTime < 0:
            #don't wait
            waitTime = 0

        #update the screen
        updatePlot(screen)
        plot.pause(0.05)
        
        #wait for next frame
        time.sleep(waitTime)
        #update last frame time
        lastTime = time.time()


def startProgram ():
    '''Initialize a program and start it running'''
    fileInput = input("Enter file path:")
    pixels, colours = getFile(fileInput)

    if pixels != None and colours != None:
        endPlot()
        screen = createNewPlot()
        updatePlot(screen)
        programObj = program(pixels, colours)
        runProgram(programObj, screen)
        print("\nExecution finished, press enter to close.")
        input()
        endPlot()
    else:
        print("Could not run program, interpreter will now close.\nPress enter to close.")
        input()

startProgram()
