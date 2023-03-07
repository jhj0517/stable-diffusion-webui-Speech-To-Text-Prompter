import whisper
import os 
import gradio as gr
from modules import safe
from modules.paths import models_path
import torch
from modules import shared

whipser_models_path = os.path.join(models_path, "Whisper")

class WhisperInference():
    def __init__(self,model_size=None):
        self.model_path = whipser_models_path
        self.current_model_size = model_size
        self.model = None
        self.available_models = whisper.available_models()
        self.available_langs = sorted(list(whisper.tokenizer.LANGUAGES.values()))

    def transcribe(self,micaudio,
                   model_size,
                   lang,
                   istranslate,
                   prbar=gr.Progress()):
        
        def progress_callback(progress_value):
            prbar(progress_value,desc="Transcribing..")
            shared.state.textinfo = f'Transcribing...'

        if model_size != self.current_model_size or self.model is None:
            self.current_model_size = model_size
            print(f'Loading Whipser model "{model_size}"  ..wait')
            shared.state.textinfo = f'Loading Whipser model "{model_size}"  ..wait'

            try:
                torch.load = safe.unsafe_torch_load
                self.model = whisper.load_model(name=model_size, download_root=whipser_models_path)
                torch.load = safe.load
            except Exception as e:
                print(f"Error while loading whisper model! : {e}")

        if lang == "Automatic Detection":
            lang = None    

        translatable_model = ["large","large-v1","large-v2"]

        
        if self.current_model_size in translatable_model and istranslate :
            result = self.model.transcribe(audio=micaudio,language=lang,verbose=False,task="translate",progress_callback=progress_callback)
        else: 
            result = self.model.transcribe(audio=micaudio,language=lang,verbose=False,progress_callback=progress_callback)    

        result_text = self.get_text(result["segments"])
        shared.state.textinfo = ''
        return result_text

    def get_text(self,segments):
        output = ""
        for seg in segments:
            output += f"{seg['text']} , "
        output = output[:-2]
        return output    