from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo
import cv2


# LIGHT VERSION OF DETECTION SCRIPT
# SET IMAGE PATH
# OUTPUTS NUMBER OF SHEEP


imagePath = "path/to/image.jpg" # <--- you set this :)


## CFG setup
cfg = get_cfg()

# Load model config and pretrained model
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
cfg.MODEL.DEVICE = "cpu"

predictor = DefaultPredictor(cfg)

# RUN MAIN

image = cv2.imread(imagePath)

predictions = predictor(image) # Dictionary containing predicted features

viz = Visualizer(image[:,:,::-1], metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), instance_mode = ColorMode.SEGMENTATION) # Visualizer is used to draw bounding boxes on image using predictions.

output = viz.draw_instance_predictions(predictions["instances"].to("cpu")) # Visualizer output is stored in output variable

# Timestamp each image, then saves the image.
output.save('.')

# String Manipulation: For the purposes extracting the sheep count 
pred_string = str(predictions).split("pred_classes:")
shp_count = pred_string[1].count("18")

print("Sheep Detected in image: ", shp_count)