import torch
import base64
from io import BytesIO
import requests
import whisperx
from sources.service import Service
import torchaudio

class WhisperXService(Service):
    def __init__(self):
        super(WhisperService, self).__init__("whisperX")
        
    def preload(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = whisperx.load_model("large-v2", self.device, compute_type="float16")

    def load(self):
        self.model.to(self.device)
    
    def unload(self):
        self.model.cpu()
    
    def execute(self, data):

        # Load file
        file = None
        if "contents" in data:
            file = BytesIO(base64.b64decode(data["contents"]))
        elif "url" in data:
            yield { "status": "downloading" }
            response = requests.get(data["url"])
            file = BytesIO(response.content)
        else:
            yield { "status": "error", "message": "No audio file provided" }
            return
        yield { "status": "loaded" }

        # Prepare
        yield { "status": "preparing" }
        audio = whisperx.load_audio(file)

        # Transcribing
        yield { "status": "transcribing" }
        result = model.transcribe(audio, batch_size=16)
        print(result["segments"])

        # Return result
        yield { "status": "transcribed", "text": result["text"].strip() }

        