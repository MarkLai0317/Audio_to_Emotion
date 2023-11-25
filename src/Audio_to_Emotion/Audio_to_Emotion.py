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

        # build audio to text model
        MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
        self.processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
        self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)

        # build text sentiment analysis model
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
        self.folder = f"./audio_split/{base_name}/"
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
             
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
        # converting audio to numpy array
        speech_array, _ = librosa.load(self.folder+"/"+AudiosegPath, sr=16_000)
        
        # audio to text recognition
        inputs = self.processor(speech_array, sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentences = self.processor.batch_decode(predicted_ids)

        # text sentiment analysis
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
    silence_info = audio_emotion_clf.detect_silence_duration()

    emotion_data = {"silence_info": silence_info,
                    "emotion_prediction": []}
    
    for chunkName in chunkNamelist:
        emotion = audio_emotion_clf.emotion_recognition(chunkName)
        emotion_data["emotion_prediction"].append({chunkName: emotion[0]})
    
    if not os.path.exists("./emotion_prediction/"):
        os.makedirs("./emotion_prediction/")
    
    with open("./emotion_prediction/prediction.json", "w") as json_file:
        json.dump(emotion_data, json_file, indent=2)

        
