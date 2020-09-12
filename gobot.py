import config
import numpy as np
import cv2
from PIL import Image
from mss import mss
import pdb
import time
import config
import pyautogui
import movements
import skimage.measure

mon = {'top': 0,'left': 0, 'width': config.screen_size[0], 'height': config.screen_size[1]}
sct = mss()

def getScreenImg():
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    img = np.array(img)
    img = cv2.resize(img, (config.img_size[0], config.img_size[1]))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def detectState(img, states):
    """
    Given a dictionary of states (masks and area paraemeters), returns the state

    """
    for state in states:
        bounds = states[state]["bounds"]
        err = states[state]["area_err"]
        area = states[state]["area"]
        new_img = layerHSVMasks(img, [bounds])
        new_img_gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(new_img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img_area = 0
        for contour in contours:
            img_area += cv2.contourArea(contour)
        img_area = img_area / (img.shape[0] * img.shape[1] ) 
        if abs(area - img_area) < err:
            return state
        
    return False
        # cv2.imshow("mask", new_img)

def runState(state):
    wait = config.state_functions[state]["wait"]
    next_states = config.state_functions[state]["next_states"]
    function = config.state_functions[state]["function"]

    function()
    time.sleep(wait)
    img = getScreenImg()
    state = detectState(img, config.states)
    while state not in next_states:
        img = getScreenImg()
        state = detectState(img, config.states)
        time.sleep(0.1)
    
    return state

def getScreenImg():
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    img = np.array(img)
    img = cv2.resize(img, (config.img_size[0], config.img_size[1]))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def drawMapBoxes(min_area=10, play_area=None):
    img = getScreenImg()
    img = maxpool(img, 4)
    img = bc(img, -70, 1.3)
    # play_area = config.play_area
    output = layerHSVMasks(img, [config.filters["day"][key] for key in config.filters["day"]], subtract=True)
    img = cv2.resize(img, (1500, 1000), interpolation=cv2.INTER_LINEAR)
    boxes = getContours(output, 1, play_area)
    pokestops = boxes["pokestops"]
    pokemon = boxes["pokemon"]

    drawBoxes(output, boxes["pokemon"], (0, 0, 255), 1)
    drawBoxes(output, boxes["pokestops"], (255, 0, 0), 1)
    output = cv2.resize(output, (3000, 2000))
    cv2.imshow("boxes", output)
    

def getContours(img, min_area, play_area=None):
    """
    Returns a list of sqaure images around contours given a minimum area

    PARAMETERS
    ----------

    play_area(optional): array-like
        [(x1, y1), (x2, y2)]
    """
    #indentify pokestops
    pokestops_img = layerHSVMasks(img, [config.filters["pokestop"]])
    pokestops_img_gray = cv2.cvtColor(pokestops_img, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(pokestops_img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    pokestop_boxes = []
    for contour in contours:
        # cv2.drawContours(pokestops_img_gray, contour, -1, (255, 255, 255), 1)
        area = cv2.contourArea(contour)
        arc_len = cv2.arcLength(contour, True)
        points = cv2.approxPolyDP(contour, 0.05*arc_len, False)
        x, y, w, h = cv2.boundingRect(points)
        if area > 0:
            if play_area is not None:
                if arePointsInArea([(x, y), (x+w, y), (x, y+h), (x+w, y+h)], play_area):
                    pokestop_boxes.append((x, y, w, h))
            else:
                pokestop_boxes.append((x, y, w, h))
        
    #######################   everthing else   ################################
    img_just_pokemon = layerHSVMasks(img, [config.filters["pokestop"]], True)
    # img_just_pokemon = layerHSVMasks(img, [], True)
    img_gray = cv2.cvtColor(img_just_pokemon, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    boxes = []
    for countour in contours:
        area = cv2.contourArea(countour)
        cv2.drawContours(img, countour, -1, (255, 255, 255), 1)
        arc_len = cv2.arcLength(countour, True)
        points = cv2.approxPolyDP(countour, 0.05*arc_len, False)
        x, y, w, h = cv2.boundingRect(points)
        if area > 0:
            if play_area is not None:
                if arePointsInArea([(x, y), (x+w, y), (x, y+h), (x+w, y+h)], play_area):
                    boxes.append((x, y, w, h))
            else:
                boxes.append((x, y, w, h))
    return {"pokemon": boxes, "pokestops": pokestop_boxes}


def drawBoxes(img, boxes, color, width):
    for box in boxes:
        pt1 = (box[0], box[1])
        pt2 = (box[0] + box[2], box[1] + box[3])
        cv2.rectangle(img, pt1, pt2, color, width)

def arePointsInArea(points, area):
    area_x1 = area[0]
    area_y1 = area[1]
    area_x2 = area[0] + area[2]
    area_y2 = area[1] + area[3]

    for point in points:
        point_x = point[0]
        point_y = point[1]

        if point_x > area_x1 and point_x < area_x2 and point_y > area_y1 and point_y < area_y2:
            return True
    return False

def createMask(img, limits, invert=False):
    """
    Creates a Gray scale mask with hsv given upper and lower limit ranges

    img: BRG Image
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, limits[0], limits[1])
    if invert == True:
        mask = np.invert(mask)
    return mask

def layerHSVMasks(img, limits, subtract=False):
    """
    Cleans the map by using HSV masks to remove certain objects

    Removes the background environment and roads
    """
    masks = []
    for limit in limits:
       masks.append(createMask(img, limit, subtract))

    #init the first one
    output = cv2.bitwise_and(img, img, mask=masks[0])
    for i in range(1, len(masks)):
        output = cv2.bitwise_and(output, output, mask=masks[i])
    return output

def maxpool(img, f):
    img = skimage.measure.block_reduce(img, (f, f, 1), np.max)
    return img

def bc(img, b, c):
    a = c
    return cv2.addWeighted(img, a, np.zeros(img.shape, img.dtype), 0, b)