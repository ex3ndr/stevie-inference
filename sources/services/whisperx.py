import torch
import base64
from io import BytesIO
import requests
import whisperx
from sources.service import Service
import torchaudio
import tempfile
import os

align_models = {
    "ja", "zh", "nl", "uk", "pt", "ar", "cs", "ru", "pl", "hu", "fi", "fa", "el", "tr", "da", "he", "vi", "ko", "ur", "te", "hi", "ca", "ml", "no", "nn"
}

class WhisperXService(Service):
    def __init__(self):
        super(WhisperXService, self).__init__("whisperx")
        
    def preload(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if torch.cuda.is_available() else "float32"
        self.model = whisperx.load_model("large-v2", 
                self.device, 
                compute_type = self.compute_type,
                asr_options = {
                    "suppress_numerals": True
                }
        )
        self.diarize_model = whisperx.DiarizationPipeline(device=self.device, use_auth_token=os.environ.get('HF_TOKEN'))

    def load(self):
        pass
        # self.model.to(self.device)
    
    def unload(self):
        pass
        # self.model.cpu()
    
    def execute(self, data):

        # Load file
        file = None
        if "contents" in data:
            file = base64.b64decode(data["contents"])
        elif "url" in data:
            yield { "status": "downloading" }
            response = requests.get(data["url"])
            print("Downloaded file from url %s" % data["url"])
            file = response.content
        else:
            yield { "status": "error", "message": "No audio file provided" }
            return
        yield { "status": "loaded" }

        # Prepare
        yield { "status": "preparing" }
        print("Preparing audio file...")
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(file)
            temp_file.flush()
            audio = whisperx.load_audio(temp_file.name)

        # Transcribing
        yield { "status": "transcribing" }
        print("Transcribing audio file...")
        result = self.model.transcribe(audio, batch_size=16)

        # Hack to not crash on unknown languages
        lang = "en"
        if result["language"] in align_models:
            lang = result["language"]

        # Alignment
        yield { "status": "aligning" }
        print("Aligning audio file...")
        model_a, metadata = whisperx.load_align_model(language_code=lang, device=self.device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)

        # Diarize
        print("Diarize...")
        diarize_segments = self.diarize_model(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result)

        # Return result
        text = "".join(segment["text"] for segment in result['segments'])
        yield { "status": "transcribed", "text": text.strip(), "segments": result['segments']}

        