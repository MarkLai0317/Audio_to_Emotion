dir_path=$1
python scripts/simple_prepare_testing_files.py --dir_path $dir_path
python scripts/preprocess_pose_data.py --dir_path $dir_path
