
import gradio as gr
from app import demo as app
import os

_docs = {'TestAnnImage': {'description': 'Displays a base image and colored subsections on top of that image. Subsections can take the from of rectangles (e.g. object detection) or masks (e.g. image segmentation).\n', 'members': {'__init__': {'value': {'type': 'tuple[\n        numpy.ndarray | PIL.Image.Image | str,\n        list[\n            tuple[\n                numpy.ndarray | tuple[int, int, int, int],\n                str,\n            ]\n        ],\n    ]\n    | None', 'default': 'None', 'description': 'Tuple of base image and list of (subsection, label) pairs.'}, 'show_legend': {'type': 'bool', 'default': 'True', 'description': 'If True, will show a legend of the subsections.'}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': 'The height of the image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'width': {'type': 'int | str | None', 'default': 'None', 'description': 'The width of the image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'color_map': {'type': 'dict[str, str] | None', 'default': 'None', 'description': 'A dictionary mapping labels to colors. The colors must be specified as hex codes.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}}, 'postprocess': {'value': {'type': 'tuple[\n        numpy.ndarray | PIL.Image.Image | str,\n        list[\n            tuple[\n                numpy.ndarray | tuple[int, int, int, int],\n                str,\n            ]\n        ],\n    ]\n    | None', 'description': 'Tuple of base image and list of subsections, with each subsection a two-part tuple where the first element is a 4 element bounding box or a 0-1 confidence mask, and the second element is the label.'}}, 'preprocess': {'return': {'type': 'AnnotatedImageData | None', 'description': None}, 'value': None}}, 'events': {'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the TestAnnImage. Uses event data gradio.SelectData to carry `value` referring to the label of the TestAnnImage, and `selected` to refer to state of the TestAnnImage. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {'AnnotatedImageData': {'source': 'class AnnotatedImageData(GradioModel):\n    image: FileData\n    annotations: List[Annotation]', 'refs': ['Annotation']}, 'Annotation': {'source': 'class Annotation(GradioModel):\n    image: FileData\n    label: str'}}, 'user_fn_refs': {'TestAnnImage': ['AnnotatedImageData']}}}
    
abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_testannimage`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%206.50.0%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_testannimage
```

## Usage

```python
import gradio as gr
from gradio_testannimage import TestAnnImage


with gr.Blocks() as demo:
    with gr.Row():
        TestAnnImage(label="Blank"),  # blank component
        TestAnnImage(label="Populated"),  # populated component


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `TestAnnImage`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["TestAnnImage"]["members"]["__init__"], linkify=['AnnotatedImageData', 'Annotation'])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["TestAnnImage"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function. 
- When used as an output, the component only impacts the return signature of the user function. 

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Should return, tuple of base image and list of subsections, with each subsection a two-part tuple where the first element is a 4 element bounding box or a 0-1 confidence mask, and the second element is the label.

 ```python
def predict(
    value: AnnotatedImageData | None
) -> tuple[
        numpy.ndarray | PIL.Image.Image | str,
        list[
            tuple[
                numpy.ndarray | tuple[int, int, int, int],
                str,
            ]
        ],
    ]
    | None:
    return value
```
""", elem_classes=["md-custom", "TestAnnImage-user-fn"], header_links=True)




    code_AnnotatedImageData = gr.Markdown("""
## `AnnotatedImageData`
```python
class AnnotatedImageData(GradioModel):
    image: FileData
    annotations: List[Annotation]
```""", elem_classes=["md-custom", "AnnotatedImageData"], header_links=True)

    code_Annotation = gr.Markdown("""
## `Annotation`
```python
class Annotation(GradioModel):
    image: FileData
    label: str
```""", elem_classes=["md-custom", "Annotation"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
            AnnotatedImageData: ['Annotation'], 
            Annotation: [], };
    const user_fn_refs = {
          TestAnnImage: ['AnnotatedImageData'], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
        
        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
