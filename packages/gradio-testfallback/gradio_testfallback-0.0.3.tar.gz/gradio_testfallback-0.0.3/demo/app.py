import gradio as gr
from gradio_testfallback import TestFallback


with gr.Blocks() as demo:
    gr.Markdown(
        "# Change the value (keep it JSON) and the front-end will update automatically."
    )
    TestFallback(value={"message": "Hello from Gradio!"}, label="Static")


if __name__ == "__main__":
    demo.launch()
