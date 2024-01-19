
import gradio as gr
from gradio_doctestvideo import DocTestVideo


example = DocTestVideo().example_inputs()

demo = gr.Interface(
    lambda x:x,
    DocTestVideo(),  # interactive version of your component
    DocTestVideo(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
