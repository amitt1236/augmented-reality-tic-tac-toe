import numpy as np
import cv2
import tictactoe as tic
import boardcreate
import pygame

'''
tic tac toe parameters
'''
board = tic.initial_state()
turn = "X"
move = None

'''
corners for birdeye view
'''
corner1 = None
corner2 = None
corner3 = None
corner4 = None
cord = None
end = False

#video feed
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 60)

#initial text
text = 'hello'

#displaing an empty board
boardcreate.update(board)

#restart game flag
restart = False

#ball dedection threshold 
threshold = 500

#reset music
def reset():
    pygame.mixer.init()
    pygame.mixer.music.load("/Users/amitaflalo/Desktop/tic/fight2.mp3")
    pygame.mixer.music.queue('/Users/amitaflalo/Desktop/tic/main.mp3')
    pygame.mixer.music.play()
 

while cap.isOpened():

    if restart:
        reset()
        restart = False

    ret, frame = cap.read()
    user = frame
    grey = cv2.GaussianBlur(frame, (11, 11), 0) 
    
    '''
    calibration, selecting corners
    '''
    def click_event(event, x, y, flags, param):
        global cord
        if event == cv2.EVENT_LBUTTONDOWN:
            cord = (x,y)

    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(user,text,(0,100), font, 4,(255,255,255),2,cv2.LINE_AA)
    key = cv2.waitKey(1)
    if key == ord('1'):
        text = 'top left'
    if key == ord('2'):
        text = 'top right'
    if key == ord('3'):
        text = 'bottom right'
    if key == ord('4'):
        text = 'bottom left'
    if key == ord('5'):
        text = 'play'
        restart = True
    if key == ord('r'):
        board = tic.initial_state()
        boardcreate.update(board)
        reset = True

    if text == 'top left':
        corner1 = cord
    if text == 'top right':
        corner2 = cord
    if text == 'bottom right':
        corner3 = cord
    if text == 'bottom left' and cord != corner3:
        corner4 = cord

    '''
    display corners for birdeyeview to the user
    '''
    if corner1 is not None:
        cv2.circle(user,corner1, 20, (0,0,255), -1)
    if corner2 is not None:
        cv2.circle(user,corner2, 20, (0,0,255), -1)
    if corner3 is not None:
        cv2.circle(user,corner3, 20, (0,0,255), -1)
    if corner4 is not None:
        cv2.circle(user,corner4, 20, (0,0,255), -1)

    
    '''
    detects which cell the the ball hits
    '''
    def mastersplinter(grid):
        height = np.shape(grid)[0]
        width = np.shape(grid)[1]

        cell_height = np.shape(grid)[0] // 3
        cell_width = np.shape(grid)[1] // 3

        left = cv2.countNonZero(grid[ : , 0 : cell_width])
        mid = cv2.countNonZero(grid[ : , cell_width : cell_width * 2])
        right = cv2.countNonZero(grid[ : , cell_width * 2 : cell_width * 3])

        if mid > left and mid > right and mid > threshold:
            bottom = cv2.countNonZero(grid[cell_height * 2: cell_height * 3 , cell_width : cell_width * 2])
            mid = cv2.countNonZero(grid[cell_height : cell_height * 2, cell_width : cell_width * 2])
            top = cv2.countNonZero(grid[0 : cell_height, cell_width : cell_width * 2])
            if top > threshold and  mid < threshold:
                return (0,1)
            elif mid > threshold and bottom < threshold:
                return (1,1)
            elif bottom > threshold:
                return (2,1)

        if left > threshold:
            bottom = cv2.countNonZero(grid[cell_height * 2: cell_height * 3 , 0 : cell_width])
            mid = cv2.countNonZero(grid[cell_height : cell_height * 2, 0 : cell_width])
            top = cv2.countNonZero(grid[0 : cell_height, 0 : cell_width])
            if top > threshold and mid < threshold:
                return (0,0)
            elif mid > threshold and bottom < threshold:
                return (1,0)
            elif bottom > threshold:
                return (2,0) 
    
        if right > threshold:
            bottom = cv2.countNonZero(grid[cell_height * 2: cell_height * 3 , cell_width * 2 : cell_width * 3])
            mid = cv2.countNonZero(grid[cell_height : cell_height * 2, cell_width * 2 : cell_width * 3])
            top = cv2.countNonZero(grid[0 : cell_height, cell_width * 2 : cell_width * 3])
            if top > threshold and mid < threshold:
                return (0,2)
            elif mid > threshold and bottom < threshold:
                return (1,2)
            elif bottom > threshold:
                return (2,2)   
        else:
            return None
        
    '''
    when calibration is over
    '''    
    if corner1 and corner2 and corner3 and corner4:
        
        
        npcorners = np.array([corner1,corner2,corner3,corner4], dtype="float32")
        
        # the width of the new frame
        widthA = np.sqrt(((corner3[0] - corner4[0]) ** 2) + ((corner3[1] - corner4[1]) ** 2))
        widthB = np.sqrt(((corner2[0] - corner1[0]) ** 2) + ((corner2[1] - corner1[1]) ** 2))

        #the height of the new frame
        heightA = np.sqrt(((corner2[0] - corner3[0]) ** 2) + ((corner2[1] - corner3[1]) ** 2))
        heightB = np.sqrt(((corner1[0] - corner4[0]) ** 2) + ((corner1[1] - corner4[1]) ** 2))

        #final dimensions
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))

        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")

        M = cv2.getPerspectiveTransform(npcorners, dst)
        grid = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))

        '''
        mask , isoliting ball color 
        '''
        # set lower and upper color limits
        lower_val = (100,30,0)
        upper_val = (170,255,255)
        # Threshold the HSV image to get only green colors
        blurred = cv2.GaussianBlur(grid, (11, 11), 0) 
        # convert to HSV
        hsv = cv2.cvtColor(grid, cv2.COLOR_BGR2HSV) 

        mask = cv2.inRange(hsv, lower_val, upper_val)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=3)
        cv2.imshow('mask',mask)

        #if ball is in frame 
        if mastersplinter(mask) is not None:
            if move is None:
                move = mastersplinter(mask)
            newmove = mastersplinter(mask)
            if newmove[0] > move[0]:
                move = newmove
            print(move)

        #ball is out of the frame
        elif move is not None and board[move[0]][move[1]] is None:
            board[move[0]][move[1]] = turn
            turn = tic.player(board)
            boardcreate.update(board)
            print(board)
            move = None

        if tic.terminal(board) and not end:
            boardcreate.winner(tic.utility(board),board)
            end = True     
            
    # Display the resulting frame
    cv2.imshow('user',user)
    cv2.setMouseCallback("user", click_event)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()