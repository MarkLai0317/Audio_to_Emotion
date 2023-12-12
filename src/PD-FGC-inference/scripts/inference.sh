
### case 5
CUDA_VISIBLE_DEVICES=0 python inference.py --all --name test1 \
    --audio_folder_path "../Audio_to_Emotion/audio_split/playaudio_20s/" \
    --exp_folder_path "../Audio_to_Emotion/emotion_image/" \
    --app_img_path "data/apps/tsai.jpg" \
    --pose_path "data/motions/pose/demo_trump_all" \
    --eye_path "data/motions/eye/id01333_00040/images" \
    --json_path "../Audio_to_Emotion/emotion_prediction/playaudio_20s.json"

