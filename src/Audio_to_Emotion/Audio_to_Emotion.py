from pydub import AudioSegment
from pydub.silence import split_on_silence

class Audio_to_Emotion:
    def __init__(self, length_of_silence=1000, silence_threshold=-40):

        self.length_of_silence = length_of_silence
        self.silence_threshold = silence_threshold
       

    



    def read_audio_file(self, filePath):
        self.audio = AudioSegment.from_file(filePath)

    def split_audio(self):
        
        chunks = split_on_silence(
            self.audio, 
            min_silence_len=self.length_of_silence,  # in ms, the length of silence to consider as a split
            silence_thresh=self.silence_threshold   # in dBFS, the silence threshold <=0
        )

        # Export each chunk as a separate audio file
        chunkNameList = []
        for i, chunk in enumerate(chunks):
            chunk.export(f"chunk{i}.mp3", format="mp3")
            chunkNameList.append(f"chunk{i}.mp3")

        return chunkNameList


