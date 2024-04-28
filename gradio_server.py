import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import LOG
from translator import PDFTranslator


def translation(input_file, source_language, target_language):
    LOG.debug(
        f"[Translation Task]\nSource File: {input_file.name}\nSource Language: {source_language}\nTarget Language: {target_language}")
    output_file_path = Translator.translate_pdf(
        input_file.name, source_language=source_language, target_language=target_language)
    return output_file_path


def launch_gradio():
    iface = gr.Interface(
        fn=translation,
        title="ChatGLM4-Translator v1.0 (PDF Ebook Translation Tool)",
        inputs=[
            gr.File(label="Upload PDF File"),
            gr.Textbox(label="Source Language (Default: English)", placeholder="English", value="English"),
            gr.Textbox(label="Target Language (Default: Chinese)", placeholder="Chinese", value="Chinese")
        ],
        outputs=[
            gr.File(label="Download Translated File")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")


def initialize_translator():
    global Translator
    Translator = PDFTranslator("glm-4")


if __name__ == "__main__":
    # Initialize the translator
    initialize_translator()
    # Launch the Gradio service
    launch_gradio()
