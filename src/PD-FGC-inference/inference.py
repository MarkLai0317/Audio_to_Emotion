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
from PIL import Image
import shutil


save_dir = "test/images/"
mp4_dir = "test/mp4s/"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(mp4_dir, exist_ok=True)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_image(folder_path):
    file_list = os.listdir(folder_path)
    img_list = []
    file_list = sorted(file_list, key=lambda x: int(x.split('/')[-1].split('.')[0]))
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            img = Image.open(file_path)
            img_list.append(img)
            #print(f"file name：{file_name}")
        except Exception as e:
            print(f"error: {e} when loading {file_name}")
    return img_list, file_list

def traverse_path(path_length, direction, start_index, n_steps):
    path = []  # 用來記錄走過的索引

    current_index = start_index
    steps_taken = 0

    # (慣性)移動方向，1為向前 -1為向後
    # direction = 1  

    while steps_taken < n_steps:
        path.append(current_index)  # 將當前索引加入路徑中

        if current_index == 0:  # 如果走到了起點，改變移動方向為向後
            direction = 1
        elif current_index == path_length - 1:  # 如果走到了終點，改變移動方向為向
            direction = -1
        
        current_index += direction  # 根據移動方向更新當前索引
        steps_taken += 1

    return path, direction

def frame_for_clip(pose_path, current_pose_frame_list, last_pose_frame_list, clip_pose_path):
    #給予要用到的frame 資料夾
    #給出現在的方向

    img_list, file_list= get_image(pose_path)
    print('pose length: {}'.format(len(img_list)))
    
    start_index = current_pose_frame_list['idx'] - current_pose_frame_list['len'] + 1
    steps = current_pose_frame_list['len']

    if last_pose_frame_list['dir'] == 'forward':
        start_index = current_pose_frame_list['idx'] - current_pose_frame_list['len'] + 1
        last_direction = 1
    else:
        start_index = current_pose_frame_list['idx'] - 1
        last_direction = -1

    path, direction= traverse_path(len(img_list), last_direction, start_index, steps)
    
    if direction == 1:
        current_pose_frame_list['dir'] = 'forward'
    elif direction == -1:
        current_pose_frame_list['dir'] = 'backward'
    current_pose_frame_list['idx'] = path[len(path)-1]

    print(path)
    print(current_pose_frame_list)

    for i, idx in enumerate(path):
        #print("i: {} idx: {} img: {} filename: {}".format(i, idx, img_list[idx], file_list[idx]))
        try:
            img = img_list[idx]  # 因為索引是從1開始的，而列表索引是從0開始，所以減1
            file_path = os.path.join(clip_pose_path, f"{i+1:06d}.jpg")  # 使用連續的數字作為檔案名稱
            img.save(file_path)
            #print(f"Image {i+1:06d} saved successfully.")
        except Exception as e:
            print(f"Error: {e} when saving Image {i+1:06d}")
    
    for i in range(5):
        #print("patch i: {} idx: {} img: {} filename: {}".format(i + len(path), len(path)-1, img_list[path[len(path)-1]], file_list[path[len(path)-1]]))
        try:
            img = img_list[path[len(path)-1]]  # 多補幾張
            file_path = os.path.join(clip_pose_path, f"{ (i + len(path))+1:06d}.jpg")  # 使用連續的數字作為檔案名稱
            img.save(file_path)
            #print(f"Image {i+1:06d} saved successfully.")
        except Exception as e:
            print(f"Error: {e} when saving Image {i+1:06d}")
    
    return current_pose_frame_list

    

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
    mkdir("test/mp4s/{}/".format(cfg.name))
    
    
    # 列出資料夾內的所有內容
    for filename in os.listdir("test/mp4s/{}/".format(cfg.name)):
        file_path = os.path.join("test/mp4s/{}/".format(cfg.name), filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                # 如果是檔案或符號連結，直接刪除
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                # 如果是子目錄，使用 shutil.rmtree() 刪除
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"刪除 {file_path} 時發生錯誤: {e}")
    
    with open(json_path) as file:
        file_contents = json.load(file)
        print(file_contents["emotion_prediction"])
        exp_predictions = file_contents["emotion_prediction"]

    _save_dir = "test/images/{}".format(cfg.name)
    os.makedirs(_save_dir, exist_ok=True)
    # 列出資料夾內的所有內容
    for filename in os.listdir(_save_dir):
        file_path = os.path.join(_save_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                # 如果是檔案或符號連結，直接刪除
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                # 如果是子目錄，使用 shutil.rmtree() 刪除
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"刪除 {file_path} 時發生錯誤: {e}")

    pose_frame_list = []
    eye_frame_list = []
    mp4_list = []
    clip_pose_list = []  #pose for each audio clip
    clip_eye_list = []  #pose for each audio clip
    save_list =[]
    print('exp_prediction len: {}'.format(len(exp_predictions)))
    for i in range(len(exp_predictions)):

        #create each folder and save each images
        #pose
        clip_pose_list.append(_save_dir + '/{}_pose'.format(exp_predictions[i]['file_name'].replace('.mp3','')))
        os.makedirs(clip_pose_list[i], exist_ok=True)
        #eye
        clip_eye_list.append(_save_dir + '/{}_eye'.format(exp_predictions[i]['file_name'].replace('.mp3','')))
        os.makedirs(clip_eye_list[i], exist_ok=True)
        #output
        save_list.append(_save_dir + '/{}'.format(exp_predictions[i]['file_name'].replace('.mp3','')))
        os.makedirs(save_list[i], exist_ok=True)

        #change
        print(exp_predictions[i]['file_name'])
        audio_path = audio_folder_path + exp_predictions[i]['file_name']
        exp_path = exp_folder_path + exp_predictions[i]['expression']
        driving_path = [pose_path, exp_path, eye_path]  #pose original video

        pose_frame_dict = {}
        eye_frame_dict = {}
        images_return = tester.inference(audio_path, app_img_path, driving_path)
        

        #得知上一個影片的最後一個frame 給下一個audio算起點
        #pose
        if len(pose_frame_list) > 0:
            pose_last_frame = pose_frame_list[i-1]['idx']
            pose_start_frame = pose_last_frame + 1 
        else:
            pose_last_frame = 0
            pose_start_frame = pose_last_frame
        #idx 表示目前audio的用到pose video最後一個frame（總長度）
        if len(pose_frame_list) > 0:
            if pose_frame_list[i-1]['dir'] == 'forward':
                pose_frame_dict['idx'] = pose_start_frame + len(images_return) -1
            else:
                pose_frame_dict['idx'] = pose_frame_list[i-1]['idx']
        else:
            pose_frame_dict['idx'] = pose_start_frame + len(images_return) -1
        
        pose_frame_dict['len'] = len(images_return)

        
        #eye
        if len(eye_frame_list) > 0:
            eye_last_frame = eye_frame_list[i-1]['idx']
            eye_start_frame = eye_last_frame + 1 
        else:
            eye_last_frame = 0
            eye_start_frame = eye_last_frame
        #idx 表示目前audio的用到eye video最後一個frame（總長度）
        if len(eye_frame_list) > 0:
            if eye_frame_list[i-1]['dir'] == 'forward':
                eye_frame_dict['idx'] = eye_start_frame + len(images_return) -1
            else:
                eye_frame_dict['idx'] = eye_frame_list[i-1]['idx']
        else:
            eye_frame_dict['idx'] = eye_start_frame + len(images_return) -1
        
        eye_frame_dict['len'] = len(images_return)
        
        
        
        
        ######### 製作專屬的pose frames #########
        clip_pose_path = clip_pose_list[i]
        if len(pose_frame_list) > 0:
            pose_frame_dict = frame_for_clip(pose_path, pose_frame_dict, pose_frame_list[i-1], clip_pose_path)
        else:
            temp_dict = {}
            temp_dict['idx'] = 0
            temp_dict['len'] = 0
            temp_dict['dir'] = 'forward'
            pose_frame_dict = frame_for_clip(pose_path, pose_frame_dict, temp_dict, clip_pose_path)

        
        ######### 製作專屬的eye frames #########
        clip_eye_path = clip_eye_list[i]
        if len(eye_frame_list) > 0:
            eye_frame_dict = frame_for_clip(eye_path, eye_frame_dict, eye_frame_list[i-1], clip_eye_path)
        else:
            temp_dict = {}
            temp_dict['idx'] = 0
            temp_dict['len'] = 0
            temp_dict['dir'] = 'forward'
            eye_frame_dict = frame_for_clip(eye_path, eye_frame_dict, temp_dict, clip_eye_path)
        

        #temp_path = [clip_pose_path, exp_path, eye_path]
        temp_path = [clip_pose_path, exp_path, clip_eye_path]  #clip pose video
        images_return = tester.inference(audio_path, app_img_path, temp_path)

        for idx, img in enumerate(images_return):  
            cv2.imwrite(os.path.join(save_list[i], "{:0>4d}.jpg".format(idx)), img)
            #print("idx: {}".format(idx + pose_start_frame))


        pose_frame_list.append(pose_frame_dict)
        eye_frame_list.append(eye_frame_dict)
        save_mp4 = "test/mp4s/{}/{}.mp4".format(cfg.name, cfg.name + '_' +str(i))
        mp4_list.append(save_mp4.replace("test/mp4s/{}/".format(cfg.name),''))
        command = "ffmpeg -y -r 25 -i {}/%04d.jpg -i {} {} ".format(save_list[i], audio_path, save_mp4)
        os.system(command)
        
    json_frame_path = "test/mp4s/{}/{}.json".format(cfg.name, cfg.name + '_frames')
    with open(json_frame_path, 'w') as f:
        json.dump(pose_frame_list, f, ensure_ascii=False, indent=4)
    txt_path = "test/mp4s/{}/{}.txt".format(cfg.name, cfg.name)
    with open(txt_path, 'w') as file:
        for i in range(len(mp4_list)):
            file.write('file \'{}\'\n'.format(mp4_list[i]))

    concat_mp4 = "test/mp4s/{}/{}.mp4".format(cfg.name, cfg.name + '_' + 'concat')
    command = "ffmpeg -f concat -i {} -c copy {}".format(txt_path, concat_mp4)
    os.system(command)
    print("final output in {}".format(concat_mp4))
