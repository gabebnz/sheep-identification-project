from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo

import cv2

import os
from os import listdir
from os.path import isfile, join
import datetime

# Get current time. For timestamping purposes
x = datetime.datetime.now()
year = x.strftime("%Y")
month = x.strftime("%m")
day = x.strftime("%d")

class Detector:
    def __init__(self):
        self.cfg = get_cfg()

        # Load model config and pretrained model
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.cfg.MODEL.DEVICE = "cpu"
        
        self.predictor = DefaultPredictor(self.cfg)

    def onImage(self, imagePath):
        image = cv2.imread(imagePath)

        predictions = self.predictor(image) # Dictionary containing predicted features

        viz = Visualizer(image[:,:,::-1], metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), instance_mode = ColorMode.SEGMENTATION) # Visualizer is used to draw bounding boxes on image using predictions.
        
        output = viz.draw_instance_predictions(predictions["instances"].to("cpu")) # Visualizer output is stored in output variable
        
        # Code block below is used to upload image to Detectron2 for sheep detection.
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # Count images in file.
        all_files = [item for item in listdir('/home/kauricone/TeamSheep/ObjectDetection/detectron_images') if isfile(join('/home/kauricone/TeamSheep/ObjectDetection/detectron_images', item))]

        # Get Timestamp for today.
        todays_folder =  "/home/kauricone/TeamSheep/ObjectDetection/detectron_images/{}/{}/{}/".format(year, month, day)
        
        # Make directory for today's processed images
        if not os.path.exists(todays_folder):
            os.makedirs(todays_folder)

        filename = imagePath.replace('/home/kauricone/TeamSheep/SheepData/Images/{}/{}/{}/'.format(year, month, day), '')
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        # Must write seperate code for local use/use outside of Kauricone Server.
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # filename = "path/to/image"
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        # Timestamp each image, then saves the image.
        output.save(todays_folder +  filename)

        # String Manipulation: For the purposes extracting the sheep count 
        pred_string = str(predictions).split("pred_classes:")
        shp_count = pred_string[1].count("18")

        return shp_count


        
        


