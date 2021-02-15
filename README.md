# Collect_Dataset
## Run.py
This program achieve the task of collecting the dataset using the developed device.

### Functions in run.py
**detectButtonsState:**
This function is for detecting and update the state of the tow buttons
there are two different globally available states for each button:
*Pressed*: Detects when the butten is pressed
*Released*: Detects when the butten is released
the global flags are:
- buttonOnePressed
- buttonOneReleased
- buttonTwoPressed
- buttonTwoReleased


**collectRealsense:**
This function is for collecting the images from the realsense2 camera

**collectZed:**
This function is for collecting the images from the Zed camera

_______________________________________________________
## args.py
This file contains the some global parameters such as the pins used on jetson nano for the buttons.


_______________________________________________________
## img_num.log
This file is a log for remembering the last image number used which allows to continue from the last number even when the program is restarted.


