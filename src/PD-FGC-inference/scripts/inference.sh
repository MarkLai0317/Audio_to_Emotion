
### case 5
CUDA_VISIBLE_DEVICES=0 python inference.py --all --name test5 \
    --audio_path "data/audios/playaudio_20s.mp3" \
    --app_img_path "data/apps/lang.jpg" \
    --pose_path "data/motions/pose/681600002/" \
    --exp_path "/home/kevinchiu/Documents/CVPDL/PD-FGC-inference/data/motions/exp/kwj_cropped" \
    --eye_path "data/motions/eye/id01333_00040/images/"

### case 6
CUDA_VISIBLE_DEVICES=0 python inference.py --all --name test6 \
    --audio_path "data/audios/playaudio_20s.mp3" \
    --app_img_path "data/apps/lang.jpg" \
    --pose_path "data/motions/pose/lang_cropped" \
    --exp_path "/home/kevinchiu/Documents/CVPDL/PD-FGC-inference/data/motions/exp/kwj_cropped" \
    --eye_path "data/motions/eye/lang_cropped/"

### case 7
CUDA_VISIBLE_DEVICES=0 python inference.py --all --name test7 \
    --audio_path "data/audios/playaudio_20s.mp3" \
    --app_img_path "data/apps/Satoh_Takeru_2.jpg" \
    --pose_path "data/motions/pose/681600002/" \
    --exp_path "/home/kevinchiu/Documents/CVPDL/PD-FGC-inference/data/motions/exp/kwj_cropped" \
    --eye_path "data/motions/eye/id01333_00040/images/"

### case 8
CUDA_VISIBLE_DEVICES=0 python inference.py --all --name test8 \
    --audio_path "data/audios/playaudio_20s.mp3" \
    --app_img_path "data/apps/Satoh_Takeru_1.jpg" \
    --pose_path "data/motions/pose/681600002/" \
    --exp_path "/home/kevinchiu/Documents/CVPDL/PD-FGC-inference/data/motions/exp/kwj_cropped" \
    --eye_path "data/motions/eye/id01333_00040/images/"