import tkinter
sizeX, sizeY = 400,400
farbArray = ["#F2F2F2","#D8D8D8","#151515", "#F7FE2E"]
root = tkinter.Tk()
root.title("Breakthrough")
root.geometry(str(sizeX)+"x"+str(sizeY))
cv = tkinter.Canvas(root,width = sizeX, height = sizeY)
oldPos = []
newPos = []
figurenArray = []
spielFeld = []
spielerAmZug = -1
click = 0
cv.pack()
def maleSchachbrett():
    for x in range(8):
        for y in range(8):
            if ((y*7)+x)%2 == 1:
                cv.create_rectangle(x*50,y*50,x*50+50,y*50+50, fill = farbArray[3])
            else:
                cv.create_rectangle(x * 50, y * 50, x * 50 + 50, y * 50 + 50, fill=farbArray[1])
maleSchachbrett()
def erstelleSpielFeld():
    for x in range(8):
        if x == 0 or x == 1:
            spielFeld.append([1,1,1,1,1,1,1,1])
        elif x == 6 or x == 7:
            spielFeld.append([-1,-1,-1,-1,-1,-1,-1,-1])
        else:
            spielFeld.append([0,0,0,0,0,0,0,0])
erstelleSpielFeld()
def wechsleSpieler():
    global spielerAmZug
    spielerAmZug = -spielerAmZug
def zugImSpielFeld(pos):
    if pos[0] > -1 and pos[0] < 8 and pos[1] > -1 and pos[1] < 8:
        return True
    else:
        return False
def getValidMoves(spieler):
    möglicheZüge = []
    for y in range(8):
        for x in range(8):
            if spielFeld[y][x] == spieler:
                for z in range(x-1,x+2):
                    if z == x:
                        if zugImSpielFeld([x,y+spieler]):
                            if spielFeld[y+spieler][x] == 0:
                                möglicheZüge.append([[x],[y],[x],[y+spieler]])
                    else:
                        if zugImSpielFeld([z,y + spieler]):
                            if spielFeld[y+spieler][z] == spieler*-1 or spielFeld[y+spieler][z] == 0:
                                möglicheZüge.append([[x],[y],[z],[y+spieler]])
    return möglicheZüge
def zeichneFiguren():
    global figurenArray
    for x in figurenArray:
        cv.delete(x)
    figurenArray.clear()
    for y in range(8):
        for x in range(8):
            if spielFeld[y][x] != 0:
                id = cv.create_oval(x*50,y*50,x*50+50, y*50+50, fill = farbArray[(spielFeld[y][x] + 1)])
                figurenArray.append(id)
zeichneFiguren()
def checkIfStartPosInValidPositionsAndReturnPosArray(validPositions, pos):
    validPositionsFromPos = []
    isValidStartPos = False
    for x in range(len(validPositions)):
        if validPositions[x][0][0] == pos[0] and validPositions[x][1][0] == pos[1]:
            isValidStartPos = True
            validPositionsFromPos.append([validPositions[x][2][0],validPositions[x][3][0]])
    return isValidStartPos, validPositionsFromPos
def checkWIN(spieler):
    if spieler == -1:
        for x in range(8):
            if spielFeld[0][x] == -1:
                print("Weiß hat gewonnen")
            if spielFeld[7][x] == 1:
                print("Schwarz hat gewonnen")
def movePlayer(oldPos,newPos,spieler):
    global spielFeld
    spielFeld[oldPos[1]][oldPos[0]] = 0
    spielFeld[newPos[1]][newPos[0]] = spieler
    checkWIN(spieler)
def mousePress(event):
    global oldPos
    global click
    posX,posY = int(event.x/50), int(event.y/50)
    if click == 0:
        validMoves = getValidMoves(spielerAmZug)
        isPosibbleMove, possibleNewPositions = checkIfStartPosInValidPositionsAndReturnPosArray(validMoves, [posX,posY])
        if isPosibbleMove:
            oldPos = [posX,posY]
            click = 1
    if click == 1:
        validMoves = getValidMoves(spielerAmZug)
        isPosibbleMove, possibleNewPositions = checkIfStartPosInValidPositionsAndReturnPosArray(validMoves,[oldPos[0], oldPos[1]])
        clickedPos = [posX,posY]
        if clickedPos in possibleNewPositions:
            movePlayer(oldPos,clickedPos, spielerAmZug)
            click = 0
            wechsleSpieler()
    zeichneFiguren()
cv.bind("<Button-1>", mousePress)
root.mainloop()