import gradio as gr
from gradio_highlightedtextbox import HighlightedTextbox

def set_highlighted():
    return HighlightedTextbox(
        value=[("Non è qualcosa di cui vergognarsi: non è diverso dalle paure e", None), ("odie", "Potential issue"), ("personali", None), ("di altre cose", "Potential issue"), ("che", None), ("molta gente ha", "Potential issue"), (".", None)],
        interactive=True, label="Output", show_legend=True, show_label=False, legend_label="Test:", show_legend_label=True
    )

with gr.Blocks() as demo:
    with gr.Row():
        gr.Textbox(" It is not something to be ashamed of: it is no different from the personal fears and dislikes of other things that very many people have.", interactive=False)
        high = HighlightedTextbox(
            interactive=True, label="Input", show_legend=True, show_label=False, legend_label="Legend:", show_legend_label=True
        )
    button = gr.Button("Submit")
    button.click(fn=set_highlighted, inputs=[], outputs=high)
    

demo.launch()