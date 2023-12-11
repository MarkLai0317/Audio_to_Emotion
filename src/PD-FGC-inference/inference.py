#################################################
# Copyright (c) 2021-present, xiaobing.ai, Inc. #
# All rights reserved.                          #
#################################################
# CV Research, xiaobing.                        #
# written by wangduomin@xiaobing.ai             #
#################################################

import os
import cv2
import numpy as np
import json
from lib.config.config import cfg
from lib.inferencer import Tester

save_dir = "test/images/"
mp4_dir = "test/mp4s/"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(mp4_dir, exist_ok=True)

if __name__ == "__main__":

    tester = Tester(cfg)

    tester.reset_cfg(cfg)
    
    #not change
    json_path = cfg.json_path
    app_img_path = cfg.app_img_path
    pose_path = cfg.pose_path
    eye_path = cfg.eye_path
    audio_folder_path = cfg.audio_folder_path
    exp_folder_path = cfg.exp_folder_path
    
    with open(json_path) as file:
        file_contents = json.load(file)
        print(file_contents["emotion_prediction"])
        exp_predictions = file_contents["emotion_prediction"]

    frame_list = []
    mp4_list = []
    print('exp_prediction len: {}'.format(len(exp_predictions)))
    for i in range(len(exp_predictions)):
        #change
        print(exp_predictions[i]['file_name'])
        audio_path = audio_folder_path + exp_predictions[i]['file_name']
        exp_path = exp_folder_path + exp_predictions[i]['expression']
        driving_path = [pose_path, exp_path, eye_path]

        _save_dir = "test/images/{}".format(cfg.name)
        os.makedirs(_save_dir, exist_ok=True)
        
        frame_dict = {}
        images_return = tester.inference(audio_path, app_img_path, driving_path)
        #得知上一個影片的最後一個frame
        if len(frame_list) > 0:
            last_frame = frame_list[i-1]['idx']
        else:
            last_frame = 0
        
        for idx, img in enumerate(images_return):  
            cv2.imwrite(os.path.join(_save_dir, "{:0>4d}.jpg".format(idx + last_frame)), img)
            #print("idx: {}".format(idx + last_frame))
            frame_dict['idx'] = idx + last_frame

        frame_list.append(frame_dict)
        save_mp4 = "test/mp4s/{}.mp4".format(cfg.name + '_' +str(i))
        mp4_list.append(save_mp4.replace("test/mp4s/",''))
        command = "ffmpeg -y -start_number {} -r 25 -i {}/%04d.jpg -i {} {}".format(last_frame, _save_dir, audio_path, save_mp4)
        os.system(command)
        
    txt_path = "test/mp4s/{}.txt".format(cfg.name)
    with open(txt_path, 'w') as file:
        for i in range(len(mp4_list)):
            file.write('file \'{}\'\n'.format(mp4_list[i]))

    concat_mp4 = "test/mp4s/{}.mp4".format(cfg.name + '_' + 'concat')
    command = "ffmpeg -f concat -i {} -c copy {}".format(txt_path, concat_mp4)
    os.system(command)
