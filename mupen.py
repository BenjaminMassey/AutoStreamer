import pyautogui as pag
import pydirectinput as pdi
import time, random

def start_tas(settings):
    pag.hotkey('ctrl', 'shift', 'p')
    time.sleep(0.025)
    pag.hotkey('ctrl', 'a')
    time.sleep(0.025)
    path = settings.get("tas_path")
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