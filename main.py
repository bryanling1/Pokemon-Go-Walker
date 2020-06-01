import gobot
import config
import movements
import time
import cv2

filters = config.filters
states=config.states
play_area = config.play_area #x, y, w, h
player_dimension = (25, 55) # width, height
play_area_pt1 = (play_area[0], play_area[1])
play_area_pt2 = (play_area[0] + play_area[2], play_area[1] + play_area[3])

player_pt2_x = play_area[0] + ((play_area[2] + player_dimension[0]) // 2)
player_pt2_y = play_area[1] + ((play_area[3] + player_dimension[1]) // 2)
player_pt2 = (player_pt2_x, player_pt2_y)
player_pt1_x = player_pt2_x - player_dimension[0]
player_pt1_y = player_pt2_y - player_dimension[1]
player_pt1 = (player_pt1_x, player_pt1_y)

#init first state
state = False
while not state:
    img = gobot.getScreenImg()
    state = gobot.detectState(img, states)

while True:
    # img = gobot.getScreenImg()
    # state = gobot.runState(state) 
    # print(gobot.runState(state) )
    gobot.drawMapBoxes()
