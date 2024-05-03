from resemble_enhance.enhancer.inference import enhance, denoise
import torch
import torchaudio
import base64
from io import BytesIO
import requests
from sources.service import Service

class EnhanceService(Service):
    def __init__(self):
        super(EnhanceService, self).__init__("enhance")
    
    def preload(self):
        pass
    
    def load(self):
        pass
    
    def unload(self):
        pass

    def execute_direct(self, request):

        # Load file
        file = BytesIO(request.data)
        waveform, sr = torchaudio.load(file)
        waveform = waveform[0]

        # Do denoising
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        output, new_sr = denoise(waveform, sr, device)

        # Save
        output_file = BytesIO()
        torchaudio.save(output_file, output.unsqueeze(0), new_sr, format = "flac")
        output_file.seek(0)
        return output_file.read()
        
        