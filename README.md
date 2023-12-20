# Batch Preview Generator

Generates preview videos and GIFs from a video using FFmpeg CLI in batch.

## Installation

Download and install the [latest version](https://github.com/Tetrax-10/batch-preview-generator/releases/latest) from the releases page. Done 🎉.

If you dont have [FFmpeg](https://ffmpeg.org/) installed then download the FFmpeg included version.

## Demo

##### [PSY - GANGNAM STYLE](https://www.youtube.com/watch?v=9bZkp7q19f0) music video to this 15 seconds preview 👇

![demo preview](./assets/demo.gif)

Run `preview` in terminal without any arguments to initiate interactive prompts.

![demo terminal](./assets/demo.png)

</br>

## CLI docs

You can use this as a CLI by just giving a valid argument(s).

The above **Gangnam Style** gif can be create with this command.

```sh
preview -o "D:\My Projects\batch-preview-generator\assets" -s 15 -sk 7 -g
```

##### args

<table>
  <tr align="center">
    <td><b>args</b></td>
    <td><b>Full args</b></td>
    <td><b>Description</b></td>
    <td><b>Default</b></td>
    <td><b>Type</b></td>
  </tr>
  <tr align="center">
    <td>-p</td>
    <td>--path</td>
    <td align="left">Path of the video or folder for batch processing</td>
    <td>CWD</td>
    <td>string</td>
  </tr>
  <tr align="center">
    <td>-o</td>
    <td>--out</td>
    <td align="left">Output folder for generated previews</td>
    <td>CWD</td>
    <td>string</td>
  </tr>
  <tr align="center">
    <td>-r</td>
    <td>--resolution</td>
    <td align="left">Preview video resolution</td>
    <td>360</td>
    <td>int</td>
  </tr>
  <tr align="center">
    <td>-s</td>
    <td>--segments</td>
    <td align="left">No. of segments in a preview video (<a href="#FAQ">more info</a>)</td>
    <td>10 (check code)</td>
    <td>int</td>
  </tr>
  <tr align="center">
    <td>-sd</td>
    <td>--sduration</td>
    <td align="left">Duration of a segment</td>
    <td>1.0 (0.1 - n.n)</td>
    <td>float</td>
  </tr>
  <tr align="center">
    <td>-sk</td>
    <td>--skip</td>
    <td align="left">Skips the first n seconds of a video, mainly used to skip intros and filler. For movies, set this value higher according to the intro duration</td>
    <td>20</td>
    <td>int</td>
  </tr>
  <tr align="center">
    <td>-sp</td>
    <td>--samepath</td>
    <td align="left">When passing this argument, the output folder is set to the input folder</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-a</td>
    <td>--audio</td>
    <td align="left">Previews will be generated with audio</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-g</td>
    <td>--gif</td>
    <td align="left">Previews will be generated in the GIF format (takes more time & space)</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-f</td>
    <td>--fps</td>
    <td align="left">Preview video FPS</td>
    <td>mp4:24/gif:10</td>
    <td>int</td>
  </tr>
  <tr align="center">
    <td>-cli</td>
    <td>--cli</td>
    <td align="left">Run as a CLI without changing default arguments. If no arguments are provided, the program will act in prompt mode. To overcome that, you can use this flag</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-h</td>
    <td>--help</td>
    <td align="left">Lists all commands with its description</td>
    <th colspan="2">present or not</th>
  </tr>
</table>

If you want to run this as a CLI but without changing or providing default arguments just run

```sh
preview -cli
```

</br>

## FAQ

##### 1. What are segments `-s`, `--segments`?

Segments are small videos extracted from the input video with a duration specified by `--sduration`. For example, if you set `--segments` to **10** and `--sduration` to **2**, each segment will be **2** seconds long. Therefore, the total duration of the preview will be **20** seconds, as **10** segments each contribute **2** seconds.

##### 2. From which part of the video are the segments extracted?

Let's say you set `--segments` to **3** and `--sduration` to **5**. In this scenario, the input video is evenly split into **3** parts, and the first **5** seconds from each part are extracted for previews. Subsequently, these segments are concatenated and converted into a single video or gif. Thus the resulting preview will be of **5x3 = 15 seconds**.

The red parts are extracted for previews

![segments](./assets/segments.png)

</br>

## Development

##### Environment setup

```powershell
git clone https://github.com/Tetrax-10/batch-preview-generator
cd batch-preview-generator
pip install termcolor progress pyreadline3 pyinstaller
```

##### Run

```powershell
python script.py <args>
```

##### Build executable

```powershell
pyinstaller preview.spec
```

Make sure to add your "dist" folder to the PATH so that when you run preview, it refers to your "dist" executable. Additionally, also ensure that the path of the installed "preview.exe" is removed during development.

### Support

Like This Tool? Gimme Some ❤️ by Liking this Repository.