'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import argparse
import glob
import csv
import numpy as np
from config.AudioConfig import AudioConfig


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def proc_frames(src_path, dst_path):
    cmd = 'ffmpeg -i \"{}\" -start_number 0 -qscale:v 2 \"{}\"/%06d.jpg -loglevel error -y'.format(src_path, dst_path)
    os.system(cmd)
    frames = glob.glob(os.path.join(dst_path, '*.jpg'))
    return len(frames)


def proc_audio(src_mouth_path, dst_audio_path):
    audio_command = 'ffmpeg -i \"{}\" -loglevel error -y -f wav -acodec pcm_s16le ' \
                    '-ar 16000 \"{}\"'.format(src_mouth_path, dst_audio_path)
    os.system(audio_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--dst_dir_path', default='/mnt/lustre/DATAshare3/VoxCeleb2',
    #                     help="dst file position")
    parser.add_argument('--dir_path', default='./preprocess_data',
                        help="dst file position")
    parser.add_argument('--src_pose_path', default='./preprocess_data/lang.mp4',
                        help="pose source file position, this could be an mp4 or a folder")
    parser.add_argument('--csv_path', default='./preprocess_data/demo.csv',
                        help="path to output index files")

    args = parser.parse_args()
    dir_path = args.dir_path
    mkdir(dir_path)


    # ===================== process pose =======================================================
    if os.path.isdir(args.src_pose_path):
        num_pose_frames = len(glob.glob(os.path.join(args.src_pose_path, '*.jpg')) + glob.glob(os.path.join(args.src_pose_path, '*.png')))
        dst_pose_frame_path = args.src_pose_path
    else:
        pose_source_save_path = os.path.join(dir_path, 'Pose_Source')
        mkdir(pose_source_save_path)
        pose_name = args.src_pose_path.split('/')[-1].split('.')[0]
        dst_pose_frame_path = os.path.join(pose_source_save_path, pose_name)
        mkdir(dst_pose_frame_path)
        num_pose_frames = proc_frames(args.src_pose_path, dst_pose_frame_path)

    # ===================== form csv =======================================================

    with open(args.csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerows([[dst_pose_frame_path, str(num_pose_frames)]])
        print('meta-info saved at ' + args.csv_path)

    csvfile.close()

'''

import argparse
import os
import csv
import glob

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def proc_frames(src_path, dst_path):
    cmd = 'ffmpeg -i \"{}\" -start_number 0 -qscale:v 2 \"{}\"/%06d.jpg -loglevel error -y'.format(src_path, dst_path)
    os.system(cmd)
    frames = glob.glob(os.path.join(dst_path, '*.jpg'))
    return len(frames)


def preprocess_pose(src_pose_path, dir_path):
    if os.path.isdir(src_pose_path):
        num_pose_frames = len(glob.glob(os.path.join(src_pose_path, '*.jpg')) + glob.glob(os.path.join(src_pose_path, '*.png')))
        dst_pose_frame_path = src_pose_path
    else:
        #pose_source_save_path = os.path.join(dir_path, 'Pose_Source')
        pose_source_save_path = dir_path
        mkdir(pose_source_save_path)
        pose_name = src_pose_path.split('/')[-1].split('.')[0]
        dst_pose_frame_path = os.path.join(pose_source_save_path, pose_name)
        mkdir(dst_pose_frame_path)
        num_pose_frames = proc_frames(src_pose_path, dst_pose_frame_path)
    return dst_pose_frame_path, num_pose_frames

def preprocess_mp4_files(dir_path):
        for mp4_file in glob.glob(os.path.join(dir_path, '*.mp4')):
            src_pose_path = mp4_file
            dst_pose_frame_path, num_pose_frames = preprocess_pose(src_pose_path, dir_path)
            #writer.writerow([dst_pose_frame_path, str(num_pose_frames)])
            print(f'Preprocessed pose for {src_pose_path}')
'''
def preprocess_mp4_files(dir_path, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        for mp4_file in glob.glob(os.path.join(dir_path, '*.mp4')):
            src_pose_path = mp4_file
            dst_pose_frame_path, num_pose_frames = preprocess_pose(src_pose_path, dir_path)
            writer.writerow([dst_pose_frame_path, str(num_pose_frames)])
            print(f'Preprocessed pose for {src_pose_path} and saved metadata at {csv_path}')
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', default=None, help="directory containing mp4 files")
    #parser.add_argument('--csv_path', default='./preprocess_data/demo.csv', help="path to output index files")
    args = parser.parse_args()

    dir_path = args.dir_path

    #mkdir(dir_path)
    preprocess_mp4_files(dir_path)
