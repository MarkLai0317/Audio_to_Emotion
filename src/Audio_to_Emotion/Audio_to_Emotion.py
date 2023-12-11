from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import argparse
import os
import json
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
import torch


class Audio_to_Emotion:
    def __init__(self, length_of_silence=1000, silence_threshold=-40):

        self.length_of_silence = length_of_silence
        self.silence_threshold = silence_threshold

        MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-english"

        self.processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
        self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)
        self.clf = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

    def read_audio_file(self, filePath):
        self.audio = AudioSegment.from_file(filePath)

    def split_audio(self):
        
        chunks = split_on_silence(
            self.audio, 
            min_silence_len=self.length_of_silence,  # in ms, the length of silence to consider as a split
            silence_thresh=self.silence_threshold,   # in dBFS, the silence threshold <=0
            keep_silence=200
        )

        # Export each chunk as a separate audio file   
        base_name, _ = os.path.splitext(os.path.basename(filePath))
        self.folder = "./audio_split/" + base_name + "/"
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
                
        silence = detect_silence(self.audio, min_silence_len=self.length_of_silence, silence_thresh=self.silence_threshold)

        for i, chunk in enumerate(chunks):
            if i < len(chunks) - 1:
                # Add silent period between segments
                duration = silence[i][1] - silence[i][0]
                chunk += AudioSegment.silent(duration=duration)

        chunkNameList = []
        for i, chunk in enumerate(chunks):
            chunk.export(self.folder + f"chunk{i}.mp3", format="mp3")
            chunkNameList.append(f"chunk{i}.mp3")

        return chunkNameList

    def detect_silence_duration(self):
        silence = detect_silence(self.audio, min_silence_len=self.length_of_silence, silence_thresh=self.silence_threshold)
        
        # Calculating the silence interval and the silence duration (in ms)
        silence_info = [{"inteval_id": i, "start":start, "stop":stop, "duration_ms":stop-start} for i, (start,stop) in enumerate(silence)]
        return silence_info
    
    def emotion_recognition(self, AudiosegPath):
        speech_array, _ = librosa.load(self.folder+"/"+AudiosegPath, sr=16_000)
        inputs = self.processor(speech_array, sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentences = self.processor.batch_decode(predicted_ids)
        emotion = self.clf(predicted_sentences)
        return emotion

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description='Audio to emotion.')
    parser.add_argument('--audio_pth',
                        dest='filePath',
                        action='store',
                        default=None)
    parser.add_argument('--silence_leng',
                        dest='length_of_silence',
                        action='store',
                        default=1000)
    parser.add_argument('--silence_dB',
                        dest='silence_threshold',
                        action='store',
                        default=-40)
    
    args = parser.parse_args()
    filePath = args.filePath
    length_of_silence = int(args.length_of_silence)
    silence_threshold = int(args.silence_threshold)

    audio_emotion_clf = Audio_to_Emotion(length_of_silence, silence_threshold)
    audio_emotion_clf.read_audio_file(filePath)
    chunkNamelist = audio_emotion_clf.split_audio()
    # silence_info = audio_emotion_clf.detect_silence_duration()

    emotion_data = {#"silence_info": silence_info,
                    "emotion_prediction": []}
    for i, chunkName in enumerate(chunkNamelist):
        emotion = audio_emotion_clf.emotion_recognition(chunkName)
        emotion = emotion[0]
        emotion["file_name"] = chunkName
        emotion["expression"] = emotion.pop("label")
        print(emotion)
        emotion_data["emotion_prediction"].append(emotion)
    if not os.path.exists(f"./emotion_prediction/"):
        os.makedirs("./emotion_prediction/")
    base_name, _ = os.path.splitext(os.path.basename(filePath))
    with open(f"./emotion_prediction/{base_name}.json", "w") as json_file:
        json.dump(emotion_data, json_file, indent=2)

        
