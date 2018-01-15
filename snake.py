from tkinter import *
import random
 
def init(data):
    data.rows = 16
    data.cols = 16
    data.margin = 10
    data.topmargin = 30
    data.direction = (0, -1)
    loadSnakeBoard(data)
    placeFood(data)
    data.gameOver = False
    data.paused = False
    data.debugMode = False
    data.score = 0
    data.levelTwo = False
    data.timerDelay = 150
 
def loadSnakeBoard(data):
    data.board = []
    for row in range(data.rows): 
        data.board += [[0]*data.cols]
    midPointMagicNo = 2
    headRow = (len(data.board)) // midPointMagicNo
    headCol = len(data.board[0]) // midPointMagicNo
    data.board[headRow][headCol] = 1
    data.headRow = headRow
    data.headCol = headCol
 
def mousePressed(event, data):
    if data.paused:
        if not placeWall(data, event):
            pass

 
def keyPressed(event, data):
    if (event.char == "r"): 
        init(data) #reset
    elif (event.char == "p"): 
        data.paused = not data.paused; return #toggle between two
    elif (event.char == "d"):
        data.debugMode = not data.debugMode
    if (data.gameOver or data.paused): 
        return
    if (event.keysym == "Left"):    
        data.direction = (0, -1)
    elif (event.keysym == "Right"): 
        data.direction = (0,  1)
    elif (event.keysym == "Up"):    
        data.direction = (-1, 0) 
    elif (event.keysym == "Down"):  
        data.direction = ( 1, 0)
    takeStep(data)
 
def timerFired(data):
    if (data.paused or data.gameOver): return 
    #game stops when game over or paused
    if data.levelTwo:
        data.timerDelay = 70
    takeStep(data)
 
def takeStep(data):
    (drow, dcol) = data.direction
    (headRow, headCol) = (data.headRow, data.headCol)
    (newHeadRow, newHeadCol) = (headRow + drow, headCol + dcol)
    wallNo = -2
    levelTwoScore = 3
    placePoisonNo = 2
    foodNo = -1
    poisonNo = -3

    if ((newHeadRow < 0) or (newHeadRow >= data.rows) or
        (newHeadCol < 0) or (newHeadCol >= data.cols) or
        data.board[newHeadRow][newHeadCol] > 0):
        #checks out of board or colide with itself
        data.gameOver = True
    elif data.board[newHeadRow][newHeadCol] == foodNo:
        # eat food
        data.board[newHeadRow][newHeadCol]= data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        placeFood(data)
        data.score += 1

        if data.score == levelTwoScore:
            data.levelTwo = True 
        if data.score > levelTwoScore and data.score % placePoisonNo == 0:
            placePoison(data)

    elif data.board[newHeadRow][newHeadCol] == wallNo:
        #eat wall
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        removeTail(data)
        data.score -= 1
        if data.score < 0:
            data.gameOver= True
    elif data.board[newHeadRow][newHeadCol] == poisonNo:
        #eat poison
        data.gameOver = True
    else:
        # didn't eat, so remove old tail (slither forward)
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol] + 1
        (data.headRow, data.headCol) = (newHeadRow, newHeadCol)
        removeTail(data)

def placeFood(data):
    foodNo = -1

    row = random.randint(0, data.rows - 1)
    col = random.randint(0, data.cols - 1)

    while data.board[row][col] != 0:
        #check for empty cell
        row = random.randint(0, data.rows - 1)
        col = random.randint(0, data.cols - 1)

    data.board[row][col] = foodNo

def placePoison(data):
    poisonNo = -3

    row = random.randint(0, data.rows - 1)
    col = random.randint(0, data.cols - 1)

    while not isLegal(data, row, col):
        row = random.randint(0, data.rows - 1)
        col = random.randint(0, data.cols - 1)

    data.board[row][col] = poisonNo

def isLegal(data, row, col):
    if data.board[row][col] != 0:
        return False

    #location where the head cant be wrt poison
    dirs = [          (-1, 0), 
            ( 0, -1),          ( 0, +1),
                      (+1, 0)              ]

    for dir in range(len(dirs)):
        drow = row + dirs[dir][0] 
        dcol = col + dirs[dir][1]

        if not (drow < 0 or drow >= data.rows or dcol < 0 or dcol >= data.cols) \
        and (data.board[drow][dcol] == data.score + 1):
        #check poison in grid and not beside the head
            return False

    return True


def placeWall(data, event):
    wallNo = -2
    rowHeight = ((data.height - 2*data.topmargin)//data.cols)
    colWidth = ((data.width - 2*data.margin)//data.cols)
    row = (event.y - data.topmargin)//(rowHeight)
    col = (event.x - data.margin)//(colWidth)
    while data.board[row][col] != 0:
        return False
    data.board[row][col] = wallNo

 
def removeTail(data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] > 0:
                data.board[row][col] -= 1
 
def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawSnakeCell(canvas, data, row, col)
    canvas.create_text(data.width//2, data.topmargin//2, \
        text="SCORE: %d" % data.score) 
    canvas.create_text(data.width//2, data.height-data.topmargin//2,\
        text="<p> pauses; <r> resets; blue is snake; green is food; \
purple is poison (KO); red is wall (-1)")  
 
def drawSnakeCell(canvas, data, row,col):
    foodNo = -1
    wallNo = -2
    poisonNo = -3

    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.topmargin
    cellWidth = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.topmargin + gridHeight * row / data.rows
    y1 = data.topmargin + gridHeight * (row+1) / data.rows

    if not data.paused:
        canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gainsbororr")
        if data.board[row][col] > 0:
            # draw snake body
            canvas.create_oval(x0, y0, x1, y1, fill="deep sky blue", width=0)
        elif data.board[row][col] == foodNo:
            # draw food
            canvas.create_oval(x0, y0, x1, y1, fill="olive drab", width=0)
        elif data.board[row][col] == wallNo:
            #draw wall
            canvas.create_rectangle(x0,y0,x1,y1, fill = "brown", width=0)
        elif data.board[row][col] == poisonNo:
            #draw poison
            canvas.create_rectangle(x0,y0,x1,y1, fill = "medium purple", width=0)
        if (data.debugMode):
            canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2,
                               text=str(data.board[row][col]),fill="grey",
                               font=("Helvatica", 14, "bold"))
    else:
        canvas.create_rectangle(x0, y0, x1, y1, fill="dim grey", outline="white")
        if data.board[row][col] > 0:
            # draw snake body
            canvas.create_oval(x0, y0, x1, y1, fill="sky blue", width=0)
        elif data.board[row][col] == foodNo:
            # draw food
            canvas.create_oval(x0, y0, x1, y1, fill="darkolivegreen3", width=0)
        elif data.board[row][col] == wallNo:
            #draw wall
            canvas.create_rectangle(x0,y0,x1,y1, fill = "brown", width=0)
        elif data.board[row][col] == poisonNo:
            #draw poison
            canvas.create_rectangle(x0,y0,x1,y1, fill = "plum1", width=0)
        if (data.debugMode):
            canvas.create_text(x0 + cellWidth/2, y0 + cellHeight/2, fill="grey",
                               text=str(data.board[row][col]),
                               font=("Helvatica", 14, "bold"))

 
def redrawAll(canvas, data):
    drawBoard(canvas, data)
    if (data.gameOver):
        canvas.create_text(data.width/2, data.height/2, text="Game Over!", \
            anchor=S, font=("Helvetica", 32, "bold"))
        if data.score not in data.highScore:
            data.highScore += [data.score]

        highScore = sorted(data.highScore)    
        highScoreDescend = highScore[::-1]
        data.highScore = highScoreDescend[:3]

        canvas.create_text(data.width/2, data.height*2//3, anchor= S, \
            text="High Scores: \n %s" % data.highScore, \
            font=("Helvetica", 24, "bold"))
    
    elif (data.paused):
        canvas.create_text(data.width/2, data.height/2, text="Paused!", \
            fill = "white", 
                           font=("Helvetica", 32, "bold"))

 
####################################
# use the run function as-is
####################################
 
def run(width=600, height=660):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    
 
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
 
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
 
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.highScore = []
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("thanks for playing!")
 
run()

# citation: cs112.github.io