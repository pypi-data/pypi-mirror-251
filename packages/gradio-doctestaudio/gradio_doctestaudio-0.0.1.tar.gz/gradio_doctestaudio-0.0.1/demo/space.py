
import gradio as gr
from app import demo as app
import os

_docs = {'DocTestAudio': {'description': 'Creates an audio component that can be used to upload/record audio (as an input) or display audio (as an output).', 'members': {'__init__': {'value': {'type': 'str\n    | pathlib.Path\n    | tuple[int, numpy.ndarray]\n    | Callable\n    | None', 'default': 'None', 'description': 'A path, URL, or [sample_rate, numpy array] tuple (sample rate in Hz, audio data as a float or int numpy array) for the default value that DocTestAudio component is going to take. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'sources': {'type': 'list["upload" | "microphone"] | None', 'default': 'None', 'description': 'A list of sources permitted for audio. "upload" creates a box where user can drop an audio file, "microphone" creates a microphone input. The first element in the list will be used as the default source. If None, defaults to ["upload", "microphone"], or ["microphone"] if `streaming` is True.'}, 'type': {'type': '"numpy" | "filepath"', 'default': '"numpy"', 'description': 'The format the audio file is converted to before being passed into the prediction function. "numpy" converts the audio to a tuple consisting of: (int sample rate, numpy.array for the data), "filepath" passes a str path to a temporary file containing the audio.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will allow users to upload and edit an audio file. If False, can only be used to play audio. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'streaming': {'type': 'bool', 'default': 'False', 'description': 'If set to True when used in a `live` interface as an input, will automatically stream webcam feed. When used set as an output, takes audio chunks yield from the backend and combines them into one streaming audio output.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'format': {'type': '"wav" | "mp3"', 'default': '"wav"', 'description': 'The file format to save audio files. Either \'wav\' or \'mp3\'. wav files are lossless but will tend to be larger files. mp3 files tend to be smaller. Default is wav. Applies both when this component is used as an input (when `type` is "format") and when this component is used as an output.'}, 'autoplay': {'type': 'bool', 'default': 'False', 'description': 'Whether to automatically play the audio when the component is used as an output. Note: browsers will not autoplay audio files if the user has not interacted with the page yet.'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}, 'editable': {'type': 'bool', 'default': 'True', 'description': 'If True, allows users to manipulate the audio file (if the component is interactive).'}, 'min_length': {'type': 'int | None', 'default': 'None', 'description': 'The minimum length of audio (in seconds) that the user can pass into the prediction function. If None, there is no minimum length.'}, 'max_length': {'type': 'int | None', 'default': 'None', 'description': 'The maximum length of audio (in seconds) that the user can pass into the prediction function. If None, there is no maximum length.'}, 'waveform_options': {'type': 'WaveformOptions | dict | None', 'default': 'None', 'description': 'A dictionary of options for the waveform display. Options include: waveform_color (str), waveform_progress_color (str), show_controls (bool), skip_length (int). Default is None, which uses the default values for these options.'}}, 'postprocess': {'value': {'type': 'tuple[int, numpy.ndarray]\n    | str\n    | pathlib.Path\n    | bytes\n    | None', 'description': 'audio data in either of the following formats: a tuple of (sample_rate, data), or a string filepath or URL to an audio file, or None.'}}, 'preprocess': {'return': {'type': 'tuple[int, numpy.ndarray] | str | None', 'description': None}, 'value': None}}, 'events': {'stream': {'type': None, 'default': None, 'description': 'This listener is triggered when the user streams the DocTestAudio.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the DocTestAudio changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the DocTestAudio using the X button for the component.'}, 'play': {'type': None, 'default': None, 'description': 'This listener is triggered when the user plays the media in the DocTestAudio.'}, 'pause': {'type': None, 'default': None, 'description': 'This listener is triggered when the media in the DocTestAudio stops for any reason.'}, 'stop': {'type': None, 'default': None, 'description': 'This listener is triggered when the user reaches the end of the media playing in the DocTestAudio.'}, 'start_recording': {'type': None, 'default': None, 'description': 'This listener is triggered when the user starts recording with the DocTestAudio.'}, 'pause_recording': {'type': None, 'default': None, 'description': 'This listener is triggered when the user pauses recording with the DocTestAudio.'}, 'stop_recording': {'type': None, 'default': None, 'description': 'This listener is triggered when the user stops recording with the DocTestAudio.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the DocTestAudio.'}}}, '__meta__': {'additional_interfaces': {'WaveformOptions': {'source': '@dataclasses.dataclass\nclass WaveformOptions:\n    waveform_color: str = "#9ca3af"\n    waveform_progress_color: str = "#f97316"\n    show_recording_waveform: bool = True\n    show_controls: bool = False\n    skip_length: int | float = 5'}}, 'user_fn_refs': {'DocTestAudio': []}}}
    
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
# `gradio_doctestaudio`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_doctestaudio
```

## Usage

```python

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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `DocTestAudio`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["DocTestAudio"]["members"]["__init__"], linkify=['WaveformOptions'])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["DocTestAudio"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function. 
- When used as an output, the component only impacts the return signature of the user function. 

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Should return, audio data in either of the following formats: a tuple of (sample_rate, data), or a string filepath or URL to an audio file, or None.

 ```python
def predict(
    value: tuple[int, numpy.ndarray] | str | None
) -> tuple[int, numpy.ndarray]
    | str
    | pathlib.Path
    | bytes
    | None:
    return value
```
""", elem_classes=["md-custom", "DocTestAudio-user-fn"], header_links=True)




    code_WaveformOptions = gr.Markdown("""
## `WaveformOptions`
```python
@dataclasses.dataclass
class WaveformOptions:
    waveform_color: str = "#9ca3af"
    waveform_progress_color: str = "#f97316"
    show_recording_waveform: bool = True
    show_controls: bool = False
    skip_length: int | float = 5
```""", elem_classes=["md-custom", "WaveformOptions"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
            WaveformOptions: [], };
    const user_fn_refs = {
          DocTestAudio: [], };
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
