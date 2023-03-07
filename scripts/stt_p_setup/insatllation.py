import os
import sys
from modules import modelloader
from modules.sd_models import model_hash
from modules.paths import models_path

from basicsr.utils.download_util import load_file_from_url

whipser_models_path = os.path.join(models_path, "Whisper")
DEFAULT_MODEL_SIZE_NAME = "medium"

def list_models(model_path):
        model_list = modelloader.load_models(model_path=model_path, ext_filter=[".pt"])
        
        def modeltitle(path, shorthash):
            abspath = os.path.abspath(path)

            if abspath.startswith(model_path):
                name = abspath.replace(model_path, '')
            else:
                name = os.path.basename(path)

            if name.startswith("\\") or name.startswith("/"):
                name = name[1:]

            shortname = os.path.splitext(name.replace("/", "_").replace("\\", "_"))[0]

            return f'{name} [{shorthash}]', shortname
        
        models = []
        for filename in model_list:
            h = model_hash(filename)
            title, short_model_name = modeltitle(filename, h)
            models.append(title)
        
        return models

def install_whisper():
    from launch import is_installed, run
    if not is_installed("whipser"):
        python = sys.executable
        run(f'"{python}" -m pip install -U git+https://github.com/jhj0517/jhj0517-whisper.git', desc="Installing whisper", errdesc=f"\n\nCouldn't install whisper, the python is \n{python}\n\n")

def download_whispermodel():
    import whisper
    if (len(list_models(whipser_models_path)) == 0):
        print("Whisper-Audio-To-Image : No Whipser models found, downloading...")
        load_file_from_url(whisper._MODELS[DEFAULT_MODEL_SIZE_NAME], whipser_models_path)
