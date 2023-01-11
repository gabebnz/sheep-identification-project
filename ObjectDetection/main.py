#!/usr/bin/env python3

from Detector import *
import json
from datetime import datetime
import statistics
import math
import random

detector = Detector()

# This python file is used to input the images used in detectron2 object detections. 
time = datetime.now()
scriptRuntime = str(time)
masterData = {
    "time": scriptRuntime,
    "images":[],
    "sheep": [],
    "grass":[],
}

# prepare todays date for file extensions
year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d")

# Method to write data to json file.
def write_json(data, filename="results.json"):
    with open(filename, 'r+') as file:
        # read in json file to variable
        file_data = json.loads(file.read())

        # add new data to json file
        file_data["results"].append(data)

        # move write head
        file.seek(0)

        # write data to file
        json.dump(file_data, file, indent=4)

# The piece of code below is used for accessing the filepath of the directory containing 
# images recently collected in the from the FTP server. Uncomment when deemed necessary. 
#----------------------------------------------------------------------------------------#
filepath = "/home/kauricone/TeamSheep/SheepData/Images/{}/{}/{}/".format(year, month, day)
#----------------------------------------------------------------------------------------#

# For filepaths to other datasets, edit the code block below
#----------------------------------------------------------------------------------------#
#filepath = "/home/kauricone/TeamSheep/SheepData/Images/2022/10/03/"
#----------------------------------------------------------------------------------------#

# get all images from image folder
all_files = [item for item in listdir(filepath) if isfile(join(filepath, item))]
files = all_files


#This script takes a very long time to run, and occasionally breaks if there are a large number of images to process...
#So if there are more than 50 images, randomly take 50 from the full file list to process.
#50 files should take ~25 minutes to process
print("FULL FILE COUNT:", len(files))

if len(files)>50:
    photoList = random.sample(files, 50)
    print("Using sublist:", photoList)
else: #otherwise, just process the images
    photoList = files
    print("Processing regular file list (<50 files)")

# List to hold counts of sheep in each image for median
shpCountList = []
countMax = 0;

#Check if any images are in the folder. It is > 1 because there is always a listing file
if len(files) > 1:
    print("\n Processing images.")
    #There is a listing file, skip it, and any other random file that might break it
    for file in photoList:
        if not file.endswith('.jpg'):
            continue

        # Start timer to measure detectron statistics
        start_time = datetime.now() 

        # Run the onImage function of the Detector class on the given image, effectively running detectron2 on said image. 
        count_response = detector.onImage(filepath +  str(file))

        #end time
        time_elapsed = datetime.now() - start_time 

        imgurl = file
        print(file, " DONE! | {}".format(time_elapsed))

        # get the maximum number of sheep found today
        if count_response > countMax:
            countMax = count_response

        # create data dictionary for this image
        data = {
            "image": imgurl,
            "sheepCount": int(count_response),
        }
        shpCountList.append(count_response)
        masterData["images"].append(data)

    # Add data value to json data for email script
    masterData["sheep"] = [countMax, math.ceil(statistics.median(shpCountList))]
    

    print("The median number of sheep in these images are: ", math.ceil(statistics.median(shpCountList)))
else:
    print("\nThere are no image files...\n")

write_json(masterData)