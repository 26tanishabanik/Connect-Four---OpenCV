import cv2
from time import sleep

from numpy.lib.shape_base import row_stack
import HandTrackingModule as htm
import time
import random
import numpy as np

def draw_text(frame, text, x, y, color=(255,0,255), thickness=4, size=3):
    if x is not None and y is not None:
        cv2.putText(frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)


def drawAll(img, buttonList = [], button1=None):
    for circle,button in zip(circleList, buttonList):
        x, y = button.pos
        w, h = button.size
        center_coordinates = circle.coor
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.circle(img, center_coordinates, 100, (0,0,0), -1)
    if button1:
        button2 = button1
        x1, y1 = button2.pos
        w1, h1 = button2.size
        cv2.rectangle(img, button2.pos, (x1 + w1, y1 + h1), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, button2.text, (x1 + 50, y1 + 70),cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 128), 4)
    return img
def draw(img,id):
    button = buttonList[id]
    x, y = button.pos
    w, h = button.size
    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
    return img

class Button():
    def __init__(self, pos, row,column,text,size=[230, 230]):
        self.pos = pos
        self.size = size
        self.row = row
        self.column = column
        self.text = text
class DoneButton():
    def __init__(self, pos, text, size=[230, 230]):
        self.pos = pos
        self.size = size
        self.text = text

class Circle():
    def __init__(self, coor, text):
        self.coor = coor
        self.text = text



buttonList = []

counter = 10
num=1
for i in range(5):
    for j in range(6):
        if (i == 0 and j == 0):
            buttonList.append(Button([300 * j + 400, 50 * i + 50], str(i), str(j), str(num)))
        elif j>=0 and i != 0:
            buttonList.append(Button([300 * j + 400, 250 * i + 50], str(i), str(j), str(num)))
        else:
            buttonList.append(Button([300 * j + 400, 250 * i + 50], str(i), str(j), str(num)))
        num += 1
doneButton = DoneButton([2500, 900], "Done", size = [400, 100])

circleList = []       
for _,button in enumerate(buttonList):
    x, y = button.pos
    w, h = button.size
    center_coordinates = (x+w//2, y+h//2)
    circleList.append(Circle(center_coordinates, button.text))

ROW_COUNT = 5
COLUMN_COUNT = 6

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece


def checkWin(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

	
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

	
    for c in range(COLUMN_COUNT-3):
        for r in range(0, 2):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
init_time = time.time()
counter_timeout_text = init_time+1
timer_timeout_text = init_time+1
counter_timeout = init_time+1
timer_timeout = init_time+1

cap = cv2.VideoCapture(0)


show = False
detector = htm.handDetector(detectionCon=0.8)
flag1 = False
circles1 = []
circles2 = []
done = False
flag2 = False
num = {}
for button in buttonList:
    num[str(button.row)+str(button.column)] = " "
board = create_board()
gameOver = False
win = -1
timer = 5
tip = False
while True:
    success, img = cap.read()
    
    img = cv2.resize(img,(3000,1900),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)


    
    img = cv2.flip(img, 1)
    
    _, img = detector.findHands(img)
    center_x = int(img.shape[0]/2)
    center_y = int(img.shape[0]/2)
    lmList, bboxInfo = detector.findPosition(img)
    
    

    img = drawAll(img, buttonList, doneButton)
    if lmList:
        if done == False:
        
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h: 

                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (250, 206, 135), cv2.FILLED)
                    l, _, _ = detector.findDistance(8, 12, img)

                    if l < 100:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        flag1 = True
                        if int(button.row) != 4:
                            if num[str(int(button.row) + 1)+str(button.column)] == "filled":
                                circles1.append(button)
                                num[str(button.row)+str(button.column)] = "filled"

                                sleep(0.15)
                                print(board)
                                break
                            else:
                                tip = True
                                #draw_text(img, "Start from bottom row", center_x-150, center_y+750,color = (0,255,255), thickness = 10, size = 6)
                                

                        else:
                            circles1.append(button)
                            num[str(button.row)+str(button.column)] = "filled"
                            sleep(0.15)
                            print(board)
                            break
            x1, y1 = doneButton.pos
            w1, h1 = doneButton.size
            if x1 < lmList[8][1] < x1 + w1 and y1 < lmList[8][2] < y1 + h1:

                cv2.rectangle(img, (x1 - 5, y1 - 5), (x1 + w1 + 5, y1 + h1 + 5), (193, 182, 255), cv2.FILLED)
                l, _, _ = detector.findDistance(8, 12, img)
                
                
                if l < 100:
                    cv2.rectangle(img, doneButton.pos, (x1 + w1, y1 + h1), (0, 255, 0), cv2.FILLED)
                    #if timer == 0:
                    done = True
            
    

        if done == True:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h: 

                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (250, 206, 135), cv2.FILLED)
                    l, _, _ = detector.findDistance(8, 12, img)
                    
                    
                    if l < 100:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
                        flag2 = True
                        if int(button.row) != 4:
                            
                            if num[str(int(button.row) + 1)+str(button.column)] == "filled":
                                done = False
                                circles2.append(button)
                                num[str(button.row)+str(button.column)] = "filled"
                        
                                sleep(0.15)
                                print(board)
                                break
                            else:
                                draw_text(img, "Start from bottom row", center_x-150, center_y+750,color = (0,255,255), thickness = 10, size = 6)
                        else:
                            done = False
                            circles2.append(button)
                            num[str(button.row)+str(button.column)] = "filled"
                            sleep(0.15)
                            print(board)
                            break

                    
    

    for circle1 in circles1:
        x, y = circle1.pos
        w, h = circle1.size
        drop_piece(board, int(circle1.row), int(circle1.column), 1)
        center_coordinates = (x+w//2, y+h//2)
        cv2.circle(img, center_coordinates, 100, (0,0,255), -1)

    for circle2 in circles2:
        x, y = circle2.pos
        w, h = circle2.size
        drop_piece(board, int(circle2.row), int(circle2.column), 2)
        center_coordinates = (x+w//2, y+h//2)
        cv2.circle(img, center_coordinates, 100, (0,255,255), -1)
    
    if checkWin(board, 1):
        print("Red wins!!")
        win = 1
        
        gameOver = True
    if checkWin(board, 2):
        print("Yellow wins!!")
        win = 2
        
        gameOver = True
    
    

    if gameOver:
        tip = False
        if win == 1:
            draw_text(img, "Red Wins!!", center_x+1300, center_y-600,color = (0,255,255), thickness = 12, size = 4)
        elif win == 2:
            draw_text(img, "Yellow Wins!!", center_x+1300, center_y-600,color = (0,255,255), thickness = 12, size= 3)
    if tip:
        draw_text(img, "#Rule: Start from", center_x+1300, center_y-600,color = (0,255,255), thickness = 10, size = 2)
        draw_text(img, "Bottom row", center_x+1300, center_y-400,color = (0,255,255), thickness = 10, size = 2)
    cv2.imshow("Image", img)
    
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    
cap.release()
cv2.destroyAllWindows()