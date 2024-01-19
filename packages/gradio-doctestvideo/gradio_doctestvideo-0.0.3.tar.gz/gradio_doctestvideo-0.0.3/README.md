
# `gradio_doctestvideo`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  

Python library for easily interacting with trained machine learning models

## Installation
    
```bash 
pip install gradio_doctestvideo
```

## Usage

```python

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

```

## `DocTestVideo`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
str
    | Path
    | tuple[str | Path, str | Path | None]
    | Callable
    | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A path or URL for the default value that DocTestVideo component is going to take. Can also be a tuple consisting of (video filepath, subtitle filepath). If a subtitle file is provided, it should be of type .srt or .vtt. Or can be callable, in which case the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>format</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Format of video format to be returned by component, such as 'avi' or 'mp4'. Use 'mp4' to ensure browser playability. If set to None, video will keep uploaded format.</td>
</tr>

<tr>
<td align="left"><code>sources</code></td>
<td align="left" style="width: 25%;">

```python
list[Literal["upload", "webcam"]] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A list of sources permitted for video. "upload" creates a box where user can drop an video file, "webcam" allows user to record a video from their webcam. If None, defaults to ["upload, "webcam"].</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The height of the displayed video, specified in pixels if a number is passed, or in CSS units if a string is passed.</td>
</tr>

<tr>
<td align="left"><code>width</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The width of the displayed video, specified in pixels if a number is passed, or in CSS units if a string is passed.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will place the component in a container - providing some extra padding around the border.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will allow users to upload a video; if False, can only be used to display videos. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>mirror_webcam</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True webcam will be mirrored. Default is True.</td>
</tr>

<tr>
<td align="left"><code>include_audio</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Whether the component should record/retain the audio track for a video. By default, audio is excluded for webcam videos and included for uploaded videos.</td>
</tr>

<tr>
<td align="left"><code>autoplay</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">Whether to automatically play the video when the component is used as an output. Note: browsers will not autoplay video files if the user has not interacted with the page yet.</td>
</tr>

<tr>
<td align="left"><code>show_share_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.</td>
</tr>

<tr>
<td align="left"><code>min_length</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The minimum length of video (in seconds) that the user can pass into the prediction function. If None, there is no minimum length.</td>
</tr>

<tr>
<td align="left"><code>max_length</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The maximum length of video (in seconds) that the user can pass into the prediction function. If None, there is no maximum length.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the DocTestVideo changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `clear` | This listener is triggered when the user clears the DocTestVideo using the X button for the component. |
| `start_recording` | This listener is triggered when the user starts recording with the DocTestVideo. |
| `stop_recording` | This listener is triggered when the user stops recording with the DocTestVideo. |
| `stop` | This listener is triggered when the user reaches the end of the media playing in the DocTestVideo. |
| `play` | This listener is triggered when the user plays the media in the DocTestVideo. |
| `pause` | This listener is triggered when the media in the DocTestVideo stops for any reason. |
| `end` | This listener is triggered when the user reaches the end of the media playing in the DocTestVideo. |
| `upload` | This listener is triggered when the user uploads a file into the DocTestVideo. |



### User function



 ```python
 def predict(
     value: str | None
 ) -> str | Path | tuple[str | Path, str | Path | None] | None:
     return value
 ```
 
