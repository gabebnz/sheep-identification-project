#!/bin/sh

# -----------------------------------------------
# BE VARY CAREFUL AND SPECIFIC WHEN RUNNING THIS
# -----------------------------------------------

# Delete the files that are not needed
# Deletes files that are before 7am. (they are black and white, no sheep, not useful for us)
#find Images/2022/09/ -mmin +570 -ls

# delete jpg files that are under 150kb in size (these are severely corrupted files)
find . -type f -name "*.jpg" -size -350k -delete