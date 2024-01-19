import gradio as gr
from gradio_testannimage import TestAnnImage


with gr.Blocks() as demo:
    with gr.Row():
        TestAnnImage(label="Blank"),  # blank component
        TestAnnImage(label="Populated"),  # populated component


if __name__ == "__main__":
    demo.launch()
