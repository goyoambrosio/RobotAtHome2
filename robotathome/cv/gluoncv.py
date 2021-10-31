#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/07/27"
__license__ = "MIT"


import robotathome as rh
import mxnet as mx
from mxnet import image
from mxnet import context
import gluoncv as gcv
from gluoncv import model_zoo, data, utils


def lblrgbd_rgb_image_object_detection(self, so_id,
                                       model='yolo3_darknet53_coco'):
    bgr_img = self.get_rgb_image_from_lblrgbd(so_id)
    chw_img, class_names, nn_out = rh.object_detection_with_gluoncv(
        cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB),
        model
    )
    return bgr_img, chw_img, class_names, nn_out

def lblrgbd_object_detection(self,
                             source='lblrgbd',
                             home_session_name='alma-s1',
                             home_subsession=0,
                             room_name='alma_masterroom1',
                             sensor_name='RGBD_1',
                             video_file_name=None,
                             model='yolo3_darknet53_coco',
                             gpu=False
                             ):
    """
    This functions ...
    """
    rows = self.get_sensor_observation_files(source,
                                             home_session_name,
                                             home_subsession,
                                             room_name,
                                             sensor_name)

    # Computing frames per second
    num_of_frames = len(rows)
    seconds = (rows.iloc[-1]['t'] - rows.iloc[0]['t']) / 10**7
    frames_per_second = num_of_frames / seconds
    rh.logger.debug("frames per second: {:.2f}", frames_per_second)

    # Get frame size
    img = self.get_rgb_image_from_lblrgbd(rows.iloc[0]['id'])
    img_h, img_w, _ = img.shape

    # Opening video file
    if video_file_name is None:
        video_file_name = ''.join(
            [
                home_session_name,
                '_', str(home_subsession),
                '_', room_name,
                '_', sensor_name,
                '_by_', model,
                dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                '.avi'
            ]
        )
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                        video_file_name)
                                           )
    rh.rename_if_exist(video_path_file_name)

    out = cv2.VideoWriter(video_path_file_name,
                          fourcc,
                          frames_per_second,
                          (img_w, img_h))

    ##############################################
    #                     NN
    ##############################################

    yolo_models = rh.get_yolo_models()
    rcnn_models = rh.get_rcnn_models()

    if model not in yolo_models + rcnn_models:
        raise Exception(f"Sorry, the model '{model}' is not allowed")

    #  Set context to cpu or gpu
    ctx_ = mx.context.gpu() if gpu else mx.context.cpu()

    # Load Pretrained Model from the CV model zoo
    net = gcv.model_zoo.get_model(model,
                                  pretrained=True,
                                  ctx=ctx_)
    class_names_ = net.classes
    nn_out_list = []
    i = 0
    for _, row in rows.iterrows():
        img = self.get_rgb_image_from_lblrgbd(row['id'])

        i += 1
        if rh.is_being_logged('INFO'):
            sys.stdout.write("\rProcessing frame %i of %i" % (i, len(rows)))
            sys.stdout.flush()

        short_edge_size = min(img.shape[0:2])
        if model in yolo_models:
            trnf_img, _ = gcv.data.transforms.presets.yolo.transform_test(mx.nd.array(img),
                                                                          short=short_edge_size)
        if model in rcnn_models:
            trnf_img, _ = gcv.data.transforms.presets.rcnn.transform_test(mx.nd.array(img),
                                                                          short=short_edge_size)
        class_ids, scores, bounding_boxs = net(trnf_img)

        df_nn_out = rh.nn_out2df(class_ids, scores, bounding_boxs)
        nn_out_list.append(df_nn_out)

        utils.viz.cv_plot_bbox(img,
                               bounding_boxs[0],
                               scores[0],
                               class_ids[0],
                               class_names=class_names_,
                               thresh=0.2,
                               linewidth=1)
        if rh.is_being_logged():
            cv2.imshow('Debug mode (press q to exit)', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.write(img)

    out.release()

    if rh.is_being_logged():
        cv2.destroyAllWindows()

    df_nn_out = pd.DataFrame(nn_out_list, columns=['class_ids',
                                                   'scores',
                                                   'bounding_boxs'])
    return df_nn_out, video_file_name

def process_with_yolo(self,
                      source='lblrgbd',
                      home_session_name='alma-s1',
                      home_subsession=0,
                      room_name='alma_masterroom1',
                      sensor_name='RGBD_1',
                      video_file_name=None,
                      gpu=False
                      ):

    """
    This functions ...
    """

    rh.logger.warning("This function is DEPRECATED, use lblrgbd_object_detection()")
    rh.logger.warning("with model='yolo3_darknet53_coco' instead ")

    rows = self.get_sensor_observation_files(source,
                                             home_session_name,
                                             home_subsession,
                                             room_name,
                                             sensor_name)

    # Computing frames per second
    num_of_frames = len(rows)
    seconds = (rows.iloc[-1]['t'] - rows.iloc[0]['t']) / 10**7
    frames_per_second = num_of_frames / seconds
    rh.logger.debug("frames per second: {:.2f}", frames_per_second)

    # Get frame size
    image_path = rows.iloc[0]['pth']
    file_name = rows.iloc[0]['f2']
    image_path_file_name = os.path.join(self.__rh_path,
                                        self.__rgbd_path,
                                        image_path,
                                        file_name)
    img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
    img_h, img_w, _ = img.shape

    # Opening video file
    if video_file_name is None:
        video_file_name = ''.join(
            [
                home_session_name,
                '_', str(home_subsession),
                '_', room_name,
                '_', sensor_name,
                '_by_YOLO',
                dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                '.avi'
            ]
        )
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                        video_file_name)
                                           )
    rh.rename_if_exist(video_path_file_name)

    out = cv2.VideoWriter(video_path_file_name,
                          fourcc,
                          frames_per_second,
                          (img_w, img_h))



    ##############################################
    #                     NN
    ##############################################


    #  get NN model
    ctx_ = context.gpu() if gpu else context.cpu()
    net = model_zoo.get_model('yolo3_darknet53_coco',
                              pretrained=True,
                              ctx=ctx_)

    nn_out = []
    i = 0
    for _, row in rows.iterrows():
        image_path = row['pth']
        file_name = row['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        i += 1
        if rh.is_being_logged('INFO'):
            sys.stdout.write("\rProcessing frame %i of %i" % (i, len(rows)))
            sys.stdout.flush()

        # core
        try:
            img = image.imread(image_path_file_name)
        except:
            print('%s is not a valid raster image' % image_path_file_name)

        # long_edge_size = img.shape[0]
        short_edge_size = img.shape[1]

        x, img = data.transforms.presets.yolo.load_test(image_path_file_name,
                                                        short=short_edge_size)
        # rh.logger.debug('Shape of pre-processed image: {}', x.shape)
        class_ids, scores, bounding_boxs = net(x)

        # to DataFrame
        df_class_ids = pd.DataFrame(class_ids.asnumpy()[0].tolist(),
                                    columns=['class_ids'])
        df_scores = pd.DataFrame(scores.asnumpy()[0].tolist(),
                                 columns=['scores'])
        df_bounding_boxs = pd.DataFrame(
            bounding_boxs.asnumpy()[0].tolist(),
            columns=['xmin', 'ymin', 'xmax', 'ymax'])

        nn_out.append([df_class_ids,
                       df_scores,
                       df_bounding_boxs])

        utils.viz.cv_plot_bbox(img,
                               bounding_boxs[0],
                               scores[0],
                               class_ids[0],
                               class_names=net.classes,
                               thresh=0.2,
                               linewidth=1)
        if rh.is_being_logged():
            cv2.imshow('Debug mode (press q to exit)', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.write(img)

    out.release()

    if rh.is_being_logged():
        cv2.destroyAllWindows()

    df_nn_out = pd.DataFrame(nn_out, columns=['class_ids',
                                              'scores',
                                              'bounding_boxs'])
    return df_nn_out, video_file_name

def process_with_rcnn(self,
                      source='lblrgbd',
                      home_session_name='alma-s1',
                      home_subsession=0,
                      room_name='alma_masterroom1',
                      sensor_name='RGBD_1',
                      video_file_name=None,
                      gpu=False
                      ):

    """
    This functions ...
    """

    rh.logger.warning("This function is DEPRECATED, use lblrgbd_object_detection()")
    rh.logger.warning("with model='faster_rcnn_resnet50_v1b_coco' instead ")

    rows = self.get_sensor_observation_files(source,
                                             home_session_name,
                                             home_subsession,
                                             room_name,
                                             sensor_name)

    # Computing frames per second
    num_of_frames = len(rows)
    seconds = (rows.iloc[-1]['t'] - rows.iloc[0]['t']) / 10**7
    frames_per_second = num_of_frames / seconds
    rh.logger.debug("frames per second: {:.2f}", frames_per_second)

    # Get frame size
    image_path = rows.iloc[0]['pth']
    file_name = rows.iloc[0]['f2']
    image_path_file_name = os.path.join(self.__rh_path,
                                        self.__rgbd_path,
                                        image_path,
                                        file_name)
    img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
    img_h, img_w, _ = img.shape

    # Opening video file
    if video_file_name is None:
        video_file_name = ''.join(
            [
                home_session_name,
                '_', str(home_subsession),
                '_', room_name,
                '_', sensor_name,
                '_by_RCNN',
                dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                '.avi'
            ]
        )
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                        video_file_name)
                                           )
    out = cv2.VideoWriter(video_path_file_name,
                          fourcc,
                          frames_per_second,
                          (img_w, img_h))



    ##############################################
    #                     NN
    ##############################################


    #  get NN model
    # import mxnet as mx
    # ctx = mx.gpu() if gpu else mx.cpu()  # Set context
    # ctx = context.cpu()
    # ctx = context.cpu_pinned()
    # ctx = context.gpu(dev_id)
    ctx_ = context.gpu() if gpu else context.cpu()
    net = model_zoo.get_model('faster_rcnn_resnet50_v1b_coco',
                              pretrained=True,
                              ctx=ctx_) 
    nn_out = []
    i = 0
    for _, row in rows.iterrows():
        image_path = row['pth']
        file_name = row['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        i += 1
        sys.stdout.write("\rProcessing frame %i of %i" % (i, len(rows)))
        sys.stdout.flush()

        # core
        try:
            img = image.imread(image_path_file_name)
        except:
            print('%s is not a valid raster image' % image_path_file_name)

        # long_edge_size = img.shape[0]
        short_edge_size = img.shape[1]

        x, img = data.transforms.presets.rcnn.load_test(image_path_file_name,
                                                        short=short_edge_size)
        # rh.logger.debug('Shape of pre-processed image: {}', x.shape)
        class_ids, scores, bounding_boxs = net(x)
        # to DataFrame
        df_class_ids = pd.DataFrame(class_ids.asnumpy()[0].tolist(),
                                    columns=['class_ids'])
        df_scores = pd.DataFrame(scores.asnumpy()[0].tolist(),
                                 columns=['scores'])
        df_bounding_boxs = pd.DataFrame(
            bounding_boxs.asnumpy()[0].tolist(),
            columns=['xmin', 'ymin', 'xmax', 'ymax'])

        nn_out.append([df_class_ids,
                       df_scores,
                       df_bounding_boxs])

        utils.viz.cv_plot_bbox(img,
                               bounding_boxs[0],
                               scores[0],
                               class_ids[0],
                               class_names=net.classes,
                               thresh=0.2,
                               linewidth=1)
        if rh.is_being_logged():
            cv2.imshow('Debug mode (press q to exit)', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.write(img)

    out.release()

    if rh.is_being_logged():
        cv2.destroyAllWindows()

    df_nn_out = pd.DataFrame(nn_out, columns=['class_ids',
                                              'scores',
                                              'bounding_boxs'])
    return df_nn_out, video_file_name


"""
Helpers
"""

def get_yolo_models():
    models = list(gcv.model_zoo.get_model_list())
    yolo_models = [models[i] for i in [176, 177, 179, 180, 182, 183]]
    return yolo_models

def get_rcnn_models():
    models = list(gcv.model_zoo.get_model_list())
    rcnn_models = [models[i] for i in [84, 86, 87, 88, 89, 91, 92, 93, 94, 95, 97]]
    return rcnn_models

def nn_out2df(class_ids, scores, bounding_boxs):
    # to DataFrame

    df_class_ids = pd.DataFrame(class_ids.asnumpy()[0].tolist(),
                                columns=['class_ids'])
    df_scores = pd.DataFrame(scores.asnumpy()[0].tolist(),
                             columns=['scores'])
    df_bounding_boxs = pd.DataFrame(
        bounding_boxs.asnumpy()[0].tolist(),
        columns=['xmin', 'ymin', 'xmax', 'ymax'])

    return [df_class_ids, df_scores, df_bounding_boxs]

def object_detection_with_gluoncv(img,
                                  model='yolo3_darknet53_coco',
                                  gpu=False):
    """ Using a pre-trained model for object detection using GluonCV

    Parameters
    ----------
    img: a preloaded image with HWC layout
    model: a string with the model to apply
    gpu: boolean indicating if gpu context must be used

    Returns
    -------
    nn_out: a list with three MXNet ndarrays [class_ids, scores, bounding_boxs]
    df_nn_out: a dataframe with the three MXNet ndarrays converted
               to dataframes
    """

    yolo_models = get_yolo_models()
    rcnn_models = get_rcnn_models()

    if model not in yolo_models + rcnn_models:
        raise Exception(f"Sorry, the model '{model}' is not allowed")

    #  Set context to cpu or gpu
    ctx_ = mx.context.gpu() if gpu else mx.context.cpu()

    # Load Pretrained Model from the CV model zoo
    net = gcv.model_zoo.get_model(model,
                                  pretrained=True,
                                  ctx=ctx_)

    # Transform the Image

    """Function that applies all of the necessary preprocessing steps for the
    yolo network

    Outputs:

    trnf_img    the transformed image that is ready to be given to the network.
    chw_img     a resized version of the image for plotting results
                - It’s in NCHW format instead of NHWC format
                - It’s an array of 32-bit floats instead of 8-bit integers
                - It’s normalized using the image net 1K statistics
                - It can be plotted because it’s in the CHW format that is
                  used by pipeline: plt.imshow(chw_image)

    Note about CHW/HCW layouts (https://github.com/Microsoft/CNTK/issues/276):

     It is essentially the same terminology that is used by cuDNN (see cuDNN API
     reference/manual). cuDNN is a very popular library which is supported by
     all popular DNN toolkits, not just CNTK, so we decided to use the same
     terminology to simplify migration between the toolkits. Note that cuDNN
     also uses N for a sample in a batch and D for the depth dimension used,
     for example, in 3D convolutions, so full description of the data layout
     may look like: NCHW

    H: height
    W: width
    C: channels (3 for color images, 1 for B&W images)

    CHW: RR...R, GG..G, BB..B
    HWC: RGB, RGB, ... RGB

    """
    short_edge_size = min(img.shape[0:2])

    if model in yolo_models:
        rh.logger.trace("yolo_model: {}", model)
        trnf_img, chw_img = gcv.data.transforms.presets.yolo.transform_test(mx.nd.array(img),
                                                                            short=short_edge_size)
    if model in rcnn_models:
        rh.logger.trace("rcnn_model: {}", model)
        trnf_img, chw_img = gcv.data.transforms.presets.rcnn.transform_test(mx.nd.array(img),
                                                                            short=short_edge_size)


    """ Make prediction
    It returns three MXNet ndarrays:
    1st array contains the object class indexes.
        shape : (1, 100, 1)
        1 image
        100 potential objects
        1 class index per object
    2nd array contains the object class probabilities.
        shape : (1, 100, 1)
        1 image
        100 potential objects
        1 object class probability (score)
    3rd array contains the object bounding box coordinates.
        shape : (1, 100, 4)
        1 image
        100 potential objects
        4 values for each object to define its bounding box:
            xmin, ymin, xmax, ymax

    net.classes is an array with coco classes
    -1 is a special value used to indicate there is no detected object
    """
    class_ids, scores, bounding_boxs = net(trnf_img)

    nn_out = [class_ids, scores, bounding_boxs]

    return chw_img, net.classes, nn_out

