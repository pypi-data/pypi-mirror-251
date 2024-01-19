
import gradio as gr
from gradio_doctestaudio import DocTestAudio


example = DocTestAudio().example_inputs()

demo = gr.Interface(
    lambda x:x,
    DocTestAudio(),  # interactive version of your component
    DocTestAudio(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
