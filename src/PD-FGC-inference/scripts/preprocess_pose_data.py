import os
import argparse

def process_folders_in_path(root_path):
    for folder_name in os.listdir(root_path):

        if folder_name.find('cropped')>=0 or folder_name.find('landmark')>=0:
            print("{} has exist".format(folder_name))
            #print(folder_name.find('cropped'))
            #print(folder_name.find('landmark'))
            continue
        else:
            folder_path = os.path.join(root_path, folder_name)
            if os.path.isdir(folder_path):
                print("folder path : {}".format(folder_path))
                command = f"python scripts/align_68.py --folder_path {folder_path}"
                os.system(command)
                print(f"Executed command for folder: {folder_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', default=None, help="directory containing frame folder")
    args = parser.parse_args()
    process_folders_in_path(args.dir_path)
