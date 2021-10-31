#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/07/27"
__license__ = "MIT"

import robotathome as rh
import cv2

def get_video_from_rgbd(self,
                        source='lblrgbd',
                        home_session_name='alma-s1',
                        home_subsession=0,
                        room_name='alma_masterroom1',
                        sensor_name='RGBD_1',
                        video_file_name=None
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

    for _, row in rows.iterrows():
        image_path = row['pth']
        file_name = row['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)

        if rh.is_being_logged():
            cv2.imshow('Debug mode (press q to exit)', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.write(img)

    out.release()

    if rh.is_being_logged():
        cv2.destroyAllWindows()

    return video_file_name

def get_composed_video_from_lblrgbd(self,
                                    home_session_name='alma-s1',
                                    home_subsession=0,
                                    room_name='alma_masterroom1',
                                    video_file_name=None
                                    ):

    ''' Docstring '''

    rows_rgbd_1 = self.get_sensor_observation_files('lblrgbd',
                                                    home_session_name,
                                                    home_subsession,
                                                    room_name,
                                                    'RGBD_1')

    rows_rgbd_2 = self.get_sensor_observation_files('lblrgbd',
                                                    home_session_name,
                                                    home_subsession,
                                                    room_name,
                                                    'RGBD_2')

    rows_rgbd_3 = self.get_sensor_observation_files('lblrgbd',
                                                    home_session_name,
                                                    home_subsession,
                                                    room_name,
                                                    'RGBD_3')

    rows_rgbd_4 = self.get_sensor_observation_files('lblrgbd',
                                                    home_session_name,
                                                    home_subsession,
                                                    room_name,
                                                    'RGBD_4')

    # Computing frames per second
    num_of_frames = len(rows_rgbd_1)
    seconds = (rows_rgbd_1.iloc[-1]['t'] - rows_rgbd_1.iloc[0]['t']) / 10**7
    frames_per_second = num_of_frames / seconds
    rh.logger.debug("frames per second: {:.2f}", frames_per_second)

    # Get frame size
    image_path = rows_rgbd_1.iloc[0]['pth']
    file_name = rows_rgbd_1.iloc[0]['f2']
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
                '_RGBD_3412',
                dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                '.avi'
            ]
        )

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                        video_file_name))
    out = cv2.VideoWriter(video_path_file_name,
                          fourcc,
                          frames_per_second,
                          (4 * img_w, img_h))

    for i in range(len(rows_rgbd_1)):
        image_rgbd_1_path = rows_rgbd_1.iloc[i, 2]
        file_rgbd_1_name = rows_rgbd_1.iloc[i, 4]
        image_rgbd_1_path_file_name = os.path.join(self.__rh_path,
                                                   self.__rgbd_path,
                                                   image_rgbd_1_path,
                                                   file_rgbd_1_name)

        image_rgbd_2_path = rows_rgbd_2.iloc[i, 2]
        file_rgbd_2_name = rows_rgbd_2.iloc[i, 4]
        image_rgbd_2_path_file_name = os.path.join(self.__rh_path,
                                                   self.__rgbd_path,
                                                   image_rgbd_2_path,
                                                   file_rgbd_2_name)

        image_rgbd_3_path = rows_rgbd_3.iloc[i, 2]
        file_rgbd_3_name = rows_rgbd_3.iloc[i, 4]
        image_rgbd_3_path_file_name = os.path.join(self.__rh_path,
                                                   self.__rgbd_path,
                                                   image_rgbd_3_path,
                                                   file_rgbd_3_name)

        image_rgbd_4_path = rows_rgbd_4.iloc[i, 2]
        file_rgbd_4_name = rows_rgbd_4.iloc[i, 4]
        image_rgbd_4_path_file_name = os.path.join(self.__rh_path,
                                                   self.__rgbd_path,
                                                   image_rgbd_4_path,
                                                   file_rgbd_4_name)


        img_rgbd_1 = cv2.imread(image_rgbd_1_path_file_name, cv2.IMREAD_COLOR)
        img_rgbd_2 = cv2.imread(image_rgbd_2_path_file_name, cv2.IMREAD_COLOR)
        img_rgbd_3 = cv2.imread(image_rgbd_3_path_file_name, cv2.IMREAD_COLOR)
        img_rgbd_4 = cv2.imread(image_rgbd_4_path_file_name, cv2.IMREAD_COLOR)

        img = cv2.hconcat([img_rgbd_3, img_rgbd_4, img_rgbd_1, img_rgbd_2])

        if rh.is_being_logged():
            cv2.imshow('Debug mode (press q to exit)', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.write(img)
    out.release()

    if rh.is_being_logged():
        cv2.destroyAllWindows()

    return video_file_name

def get_rgb_image_from_lblrgbd(self, so_id):
    """
    This function 

    Parameters
    ----------

    Returns
    -------
    A BGR cv2 image

    """

    sql_str = f"""
    select pth, f2
    from rh_temp_lblrgbd
    where id = {so_id}
    """

    df_rows = pd.read_sql_query(sql_str, self.__con)
    # rh.logger.debug("df_rows.shape: {}", df_rows.shape)
    rgb_image_path_file_name = os.path.join(self.__rh_path,
                                        self.__rgbd_path,
                                        df_rows.loc[0, "pth"],
                                        df_rows.loc[0, "f2"])

    # rh.logger.debug("rgb_image_path_file_name: {}",
    #                 rgb_image_path_file_name)
    bgr_img = cv2.imread(rgb_image_path_file_name, cv2.IMREAD_COLOR)

    return bgr_img

def get_depth_image_from_lblrgbd(self, so_id):
    """
    This function

    Parameters
    ----------

    Returns
    -------
    A gray levels cv2 image

    """

    sql_str = f"""
    select pth, f1
    from rh_temp_lblrgbd
    where id = {so_id}
    """

    df_rows = pd.read_sql_query(sql_str, self.__con)
    rh.logger.debug("df_rows.shape: {}", df_rows.shape)
    rgb_image_path_file_name = os.path.join(self.__rh_path,
                                        self.__rgbd_path,
                                        df_rows.loc[0, "pth"],
                                        df_rows.loc[0, "f1"])

    rh.logger.debug("rgb_image_path_file_name: {}",
                    rgb_image_path_file_name)
    img = cv2.imread(rgb_image_path_file_name, cv2.IMREAD_COLOR)

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def lblrgbd_plot_labels(self, so_id):
    img = self.get_rgb_image_from_lblrgbd(so_id)
    labels = self.get_labels_from_lblrgbd(so_id)
    rh.logger.debug("labels: {}", labels)
    mask = self.get_mask_from_lblrgbd(so_id)
    label_mask = self.get_label_mask(mask, labels['local_id'])
    alpha = 0.7
    out_img, colors = rh.overlay_mask(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
                                      label_mask,
                                      alpha)
    rh.plot_mask(out_img, labels['name'], colors)


"""
Helpers
"""

def bin2rgba(img):
    """
    TODO
    """

    img = cv2.cvtColor(img*255, cv2.COLOR_GRAY2RGB)
    color_mask = np.random.random((1, 3)).tolist()[0]

    my_mask = cv2.compare(img,245,cv2.CMP_GT)
    img[my_mask > 0] = 255

    for i in range(3):
        img[:,:,i] = color_mask[i]*255
    plt.imshow(img, interpolation='nearest')
    plt.show()

def overlay_mask(img, masks, alpha=0.5):
    # cv2.addWeighted(ovl_img, alpha, base_img, 1 - alpha, 0, base_img)
    # return base_img
    colors = []
    for mask in masks:
        color = np.random.random(3)
        colors.append(np.append(color,[alpha]))
        mask = np.repeat((mask > 0)[:, :, np.newaxis], repeats=3, axis=2)
        img = np.where(mask, img * (1 - alpha) + color*255 * alpha, img)
    return img.astype('uint8'), colors

def plot_mask(patched_img, names, colors):
    plt.imshow(patched_img)
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    mpatches_=[]
    for i, color_ in enumerate(colors):
        mpatches_.append(mpatches.Patch(color=color_, label=names[i]))
    plt.legend(handles=mpatches_)
    plt.show()


