import pyautogui
import time

pyautogui.FAILSAFE = True

print("Move your mouse to the window")
time.sleep(10)
print("Starting now")

for i in range(1, 477):
    pyautogui.click(button="right") # opens right click menu
    pyautogui.move(100, 270) # moves mouse to save button
    time.sleep(0.5) # wait for save drop down to open
    pyautogui.move(200, 0) # moves to the top of the save drop down
    pyautogui.move(0, 50) # moves down the drop down to "Image to File"
    pyautogui.click(button="left") # click "save image to file"
    time.sleep(0.5) # wait for file explorer to open
    pyautogui.write(str(i)) # type the name of the image into the box

    pyautogui.press("tab") # select file save type box
    pyautogui.press("right") # open file save type box
    for j in range(0,4): # navigate down to PNG
        pyautogui.press("down")
    pyautogui.press("enter") # save choice and close box
    pyautogui.press("tab") # go to save option
    pyautogui.press("enter") # save image
    pyautogui.move(-300, -320) # move mouse back to original location
    pyautogui.click(button="left") # click window to focus on it
    pyautogui.press("down") # advance to the next image

