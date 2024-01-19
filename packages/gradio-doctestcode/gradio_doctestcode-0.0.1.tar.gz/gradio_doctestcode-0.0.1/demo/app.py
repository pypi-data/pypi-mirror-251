
import gradio as gr
from gradio_doctestcode import DocTestCode


example = DocTestCode().example_inputs()

demo = gr.Interface(
    lambda x:x,
    DocTestCode(),  # interactive version of your component
    DocTestCode(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
