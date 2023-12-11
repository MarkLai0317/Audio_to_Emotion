
### case 5
CUDA_VISIBLE_DEVICES=0 python inference.py --all --name test1 \
    --audio_folder_path "../Audio_to_Emotion/audio_split/audio_sample/" \
    --exp_folder_path "../Audio_to_Emotion/emotion_image/" \
    --app_img_path "data/apps/tsai.jpg" \
    --pose_path "data/motions/pose/demo_trump" \
    --eye_path "data/motions/eye/reagan_clip1_cropped" \
    --json_path "../Audio_to_Emotion/emotion_prediction/audio_sample.json"


