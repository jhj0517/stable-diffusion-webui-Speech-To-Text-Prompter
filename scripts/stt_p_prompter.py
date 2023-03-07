import gradio as gr
from modules import scripts
from scripts.stt_p_setup.insatllation import install_whisper , download_whispermodel
from scripts.stt_p_inference.whisper_inference import WhisperInference

install_whisper()
download_whispermodel()

whisper_inf = WhisperInference()

def on_change_models(model_size):
    translatable_model = ["large","large-v1","large-v2"]
    if model_size not in translatable_model:
        return gr.Checkbox.update(visible=False,value=False,interactive=False)
    else:
        return gr.Checkbox.update(visible=True,value=False,label="Translate to English",interactive=True) 

def run_transcribe(micaudio,
                model_size,
                lang,
                istranslate):
    return whisper_inf.transcribe(micaudio,model_size,lang,istranslate)

class STTPrompter(scripts.Script):
    def title(self):
        return "Speech-To-Text Prompter"
    
    def ui(self, is_img2img):

        with gr.Blocks() as stt_p_ui:
            with gr.Row().style():
                with gr.Column(scale=6): #configs
                    mic_prompt = gr.Microphone(label="Record your voice here",type="filepath", elem_id="stt_p_mic",interactive=True)
                    with gr.Row():
                        dd_models = gr.Dropdown(choices=whisper_inf.available_models, label="Whisper Model", value = "medium")
                        dd_langs = gr.Dropdown(choices=["Automatic Detection"]+whisper_inf.available_langs,value="Automatic Detection",label="Source Language")
                    with gr.Row():
                        cb_translate = gr.Checkbox(value=False,label="Translate to English",interactive=True,visible=False)  
                    with gr.Row():
                        btn_transcribe = gr.Button("Transcribe",elem_id="stt_p_trans",variant="primary")       

                with gr.Column(scale=4): #output   
                    with gr.Row():
                        tb_res = gr.Textbox(label="output",elem_id="stt_p_res",lines=7,interactive=False)
                    with gr.Row():
                        btn_to_prompt = gr.Button("To prompt").style(full_width=False)   
                        btn_to_negprompt = gr.Button("To negative prompt").style(full_width=False)  

            btn_transcribe.click(
                fn=run_transcribe,
                inputs=[mic_prompt,dd_models,dd_langs,cb_translate],
                outputs=[tb_res]
            )

            dd_models.change(
                fn=on_change_models,
                inputs=[dd_models],
                outputs=[cb_translate],
            )

            tabname= "Img2Img" if is_img2img else "Txt2Img"
            
            btn_to_prompt.click(
                fn=None,
                _js=f"update{tabname}Prompt",
                inputs=[tb_res],
                outputs=None
            )

            btn_to_negprompt.click(
                fn=None,
                _js=f"update{tabname}NegPrompt",
                inputs=[tb_res],
                outputs=None
            )

        return [stt_p_ui]
    
