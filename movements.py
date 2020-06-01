import pyautogui
import config
import gobot
import time

def spinStop():
    pyautogui.moveTo(1200, 1000) 
    pyautogui.mouseDown(1200, 1000)
    pyautogui.moveTo(1900, 1000) 
    pyautogui.mouseUp()
    pyautogui.moveTo(1500, 1700) 
    time.sleep(0.2)
    pyautogui.click()


def mapAction():
    img = gobot.getScreenImg()
    play_area = config.play_area
    output = gobot.layerHSVMasks(img, [config.filters["day"][key] for key in config.filters["day"]], subtract=True)
    boxes = gobot.getContours(output, 10, play_area)
    pokestops = boxes["pokestops"]
    pokemon = boxes["pokemon"]

    gobot.drawBoxes(img, boxes["pokemon"], (0, 0, 255), 2)
    gobot.drawBoxes(img, boxes["pokestops"], (255, 0, 0), 2)

    for pokestop in pokestops:
        x = pokestop[0] + pokestop[2]//2
        y = pokestop[1] + pokestop[3]//2
        screen_x = x * 2
        screen_y = y * 2
        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.click()
        return 
    for poke in pokemon:
        x = poke[0] + poke[2]//2
        y = poke[1] + poke[3]//2
        screen_x = x * 2
        screen_y = y * 2
        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.click()
        return 

    return

def throwPokeball(): 
    PAUSE = 0.0001
    # pyautogui.click(2700, 15)
    # time.sleep(0.5)
    # pyautogui.click(800*2, 800*2) 
    # time.sleep(3)
    pyautogui.moveTo(800*2, 800*2, duration=0.1) 
    pyautogui.mouseDown()
    pyautogui.moveTo(800*2, 950*2, duration=0.1) 
    pyautogui.moveTo(800*2, 700*2) 
    pyautogui.mouseUp()
    # pyautogui.moveTo(550*2, 850*2, duration=0.1) 
    
    # pyautogui.moveTo(1080*2, 800*2, duration=0.1) 
    # pyautogui.moveTo(1080*2, 600*2, duration=0.1) 

def exitCaughtPokemon():
    pyautogui.click(800*2, 650*2)
    pyautogui.click(800*2, 650*2)
    time.sleep(2)
    pyautogui.click(800*2, 870*2)
    pyautogui.click(800*2, 870*2)
