import pyautogui as pag
import pydirectinput as pdi
import time, random

def start_tas():
    pag.hotkey('ctrl', 'shift', 'p')
    time.sleep(0.025)
    pag.hotkey('ctrl', 'a')
    time.sleep(0.025)
    file = open("tas_path.txt", "r")
    path = file.read()
    file.close()
    pag.write(path, interval=0.0125)
    time.sleep(0.025)
    pag.press('enter')
    time.sleep(0.025)
    pag.press('enter')
    
def end_run():
    pag.hotkey('ctrl', 'shift', 's')
    keys = ['7','8','9','0','y','u','i','o','p','h',\
            'j','k','n','m',',','.','/',"'",';']
    buttons = ""
    for i in range(100):
        buttons += keys[random.randint(0, len(keys) - 1)]
    pdi.write(buttons, interval=0.025)

time.sleep(5)

start_tas()

time.sleep(70)

end_run()

time.sleep(0.25)

start_tas()