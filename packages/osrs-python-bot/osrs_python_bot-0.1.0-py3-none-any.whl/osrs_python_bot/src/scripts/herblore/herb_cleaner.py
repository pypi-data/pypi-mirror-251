"""Module for cleaning herbs."""
from random import randrange
import time
import pyautogui
from osrs_python_bot.src.common.bank_manager import withdraw_all
from osrs_python_bot.src.common.bank_manager import mouse_to_bank_slot_1_8
from osrs_python_bot.src.common.bank_manager import deposit_inventory
from osrs_python_bot.src.common.bank_manager import close_bank_menu
from osrs_python_bot.src.common.bank_manager import open_bank_chest
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_1_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_1_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_1_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_1_4
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_2_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_2_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_2_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_2_4
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_3_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_3_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_3_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_3_4
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_4_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_4_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_4_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_4_4
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_5_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_5_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_5_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_5_4
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_6_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_6_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_6_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_6_4
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_7_1
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_7_2
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_7_3
from osrs_python_bot.src.common.inventory_clicker import mouse_to_inventory_slot_7_4

################
# Processing #
################

def herb_cleaner():
    """function for cleaning herbs."""
    max_timeout = time.time() + 30000
    while True:
        if time.time() > max_timeout:
            break

        x = str(randrange(10))              # global random number generation
        y = str(randrange(10))              # global random number generation
        z = str(randrange(10))              # global random number generation


        open_bank_chest(x, y, z)            # open the bank chest
        deposit_inventory(x, y,z)           # deposit inventory
        mouse_to_bank_slot_1_8(x, y, z)
        withdraw_all(x, y, z)

        close_bank_menu()                   # close bank menu

        mouse_to_inventory_slot_1_1(x, y, z)# click every inventory slot
        pyautogui.click()
        mouse_to_inventory_slot_1_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_1_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_1_4(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_2_1(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_2_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_2_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_2_4(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_3_1(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_3_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_3_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_3_4(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_4_1(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_4_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_4_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_4_4(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_5_1(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_5_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_5_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_5_4(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_6_1(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_6_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_6_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_6_4(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_7_1(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_7_2(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_7_3(x, y, z)
        pyautogui.click()
        mouse_to_inventory_slot_7_4(x, y, z)
        pyautogui.click()

        time.sleep(2)
