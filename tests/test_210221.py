#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/19"
__license__ = "MIT"

import sys
import robotathome as rh

rh.log.enable_logger(sink=sys.stderr, level="INFO")
rh.logger.info("Processing images from a room with yolo")

rh_path = '/media/goyo/WDGREEN2TB-A/Users/goyo/Documents/PhD2020/Robot@Home_DataSet_v2.0.0/'
wspc_path = '/media/goyo/WDGREEN2TB-A/Users/goyo/Documents/PhD2020/WORKSPACE'

rh_obj = rh.RobotAtHome(rh_path, wspc_path)

# ####### YOLO ########
yolo_detections, yolo_video_file_name = rh_obj.process_with_yolo(
    'lblrgbd',
    'anto-s1',
    0,
    'anto_livingroom1',
    'RGBD_2'
)

yolo_class_ids = yolo_detections['class_ids']
yolo_scores = yolo_detections['scores']
yolo_bounding_boxs = yolo_detections['bounding_boxs']

rh.logger.info("yolo_class_ids: {}", yolo_class_ids)
rh.logger.info("yolo_scores: {}", yolo_scores)
rh.logger.info("yolo_bounding_boxs: {}", yolo_bounding_boxs)

rh.logger.info("yolo_video_file_name: {}", yolo_video_file_name)

# ####### RCNN ########
rcnn_detections, rcnn_video_file_name = rh_obj.process_with_rcnn(
    'lblrgbd',
    'anto-s1',
    0,
    'anto_livingroom1',
    'RGBD_2'
)

rcnn_class_ids = rcnn_detections['class_ids']
rcnn_scores = rcnn_detections['scores']
rcnn_bounding_boxs = rcnn_detections['bounding_boxs']

rh.logger.info("rcnn_class_ids: {}", rcnn_class_ids)
rh.logger.info("rcnn_scores: {}", rcnn_scores)
rh.logger.info("rcnn_bounding_boxs: {}", rcnn_bounding_boxs)

rh.logger.info("rcnn_video_file_name: {}", rcnn_video_file_name)
