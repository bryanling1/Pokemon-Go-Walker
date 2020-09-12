import gobot
import config
import movements
import time
import cv2
import tools.predictState as ps

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

####################init first state########################
# state = False
# while not state:
#     img = gobot.getScreenImg()
#     state = gobot.detectState(img, states)

######################## RUN ############################
# while True:
    # img = gobot.getScreenImg()
    # img = gobot.maxpool(img, 5)
    # img = gobot.bc(img, -70, 1.3)
    # img = gobot.layerHSVMasks(img, [config.filters["day"][key] for key in config.filters["day"]], True)
    # img = cv2.resize(img, (3000, 2000), interpolation=cv2.INTER_LINEAR)
    # cv2.imshow("pool", img)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    # state = gobot.runState(state) 
    # print(gobot.runState(state) )

###########################Testing##############################
while True:
    img = gobot.getScreenImg()
    # img = cv2.rectangle(img, (config.img_crop[0], config.img_crop[1]), (config.img_crop[2], config.img_crop[3]), (0, 0, 255), 1)
    img = img[config.img_crop[1]: config.img_crop[3],config.img_crop[0]: config.img_crop[2], :]
    cv2.imshow("pool", img)
    print(ps.predict(img))
    time.sleep(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # state = gobot.runState(state) 
    # print(gobot.runState(state) )
