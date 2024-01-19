"""Module providing a function for prayer flicking."""
from random import randrange
import time
import pyautogui

################
# Processing #
################

def nightmare_zone():
    """function for making guthix rest."""
    max_timeout = time.time() + 30000
    while True:
        if time.time() > max_timeout:
            break

        a = str(randrange(10)) # random number generation
        b = str(randrange(10)) # random number generation
        c = str(randrange(10)) # random number generation
        d = str(randrange(10)) # random number generation

        # random ~30s string -> float
        wait_time = float('30.' + a + b + c + d)
        print( 'Time: '+ str(wait_time))

        # double click
        pyautogui.click()
        pyautogui.click()

        # sleep
        time.sleep(wait_time)
