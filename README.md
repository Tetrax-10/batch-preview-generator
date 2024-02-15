# Batch Preview Generator

**Generates preview videos and GIFs from videos using FFmpeg CLI in batch.**

<img src="https://raw.githubusercontent.com/Tetrax-10/batch-preview-generator/main/assets/banner.png"></img>

## Installation

Download and install the [Latest version](https://github.com/Tetrax-10/batch-preview-generator/releases/latest) from the releases page. Done 🎉.

If you dont have [FFmpeg](https://ffmpeg.org/) installed then download the [FFmpeg included version](https://github.com/Tetrax-10/batch-preview-generator/releases/latest) or download FFmpeg from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z).

## Demo

**[PSY - GANGNAM STYLE](https://www.youtube.com/watch?v=9bZkp7q19f0) music video to this 15 seconds preview 👇**

![demo preview](https://raw.githubusercontent.com/Tetrax-10/batch-preview-generator/main/assets/demo.gif)

</br>

**Run `preview` in terminal without any arguments (flags) to initiate interactive prompts.**

![demo preview](https://raw.githubusercontent.com/Tetrax-10/batch-preview-generator/main/assets/demo.png)
**Note:** This Screenshot reflects initial release and new changes may not be represented.

</br>

## CLI docs

You can use this as a CLI by just giving a valid argument(s).

The above **Gangnam Style** gif can be created with this command.

```powershell
PS Downloads> preview -o "D:\My Projects\batch-preview-generator\assets" -s 15 -sk 7 -g
```

### Arguments

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
    <td align="left">No. of <a href="#1-what-are-segments--s---segments">segments</a> in a preview video</td>
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
    <td>float</td>
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
    <td>-q</td>
    <td>--quality</td>
    <td align="left">Preview video quality (low, normal, high)</td>
    <td>normal</td>
    <td>string</td>
  </tr>
  <tr align="center">
    <td>-c</td>
    <td>--compression</td>
    <td align="left">Preview video compression modes:<br><b>fast</b> but low quality output and bigger file size.<br><b>slow</b> gives good quality and reasonable size but little slower.<br><b>veryslow</b> gives best quality and least file size but its very slow.</td>
    <td>slow</td>
    <td>string</td>
  </tr>
  <tr align="center">
    <td>-cli</td>
    <td>--cli</td>
    <td align="left">Run as a CLI without changing default arguments. If no arguments are provided, the program will act in prompt mode. To prevent that, you can use this flag</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-cuda</td>
    <td>--cuda</td>
    <td align="left">Uses cuda cores for fast processing (Nvidia GPUs only)</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-v</td>
    <td>--version</td>
    <td align="left">Prints version info</td>
    <th colspan="2">present or not</th>
  </tr>
  <tr align="center">
    <td>-h</td>
    <td>--help</td>
    <td align="left">Lists all commands with its description</td>
    <th colspan="2">present or not</th>
  </tr>
</table>

If you want to run this as a CLI without providing or changing default arguments then just run

```sh
preview -cli
```

</br>

## FAQ

### 1. What are segments `-s`, `--segments`?

Segments are small videos extracted from the input video with a duration specified by `--sduration`. For example, if you set `--segments` to **10** and `--sduration` to **2**, each segment will be **2** seconds long. Therefore, the total duration of the preview will be **20** seconds, as **10** segments each contribute **2** seconds.

### 2. From which part of the video are the segments extracted?

Let's say you set `--segments` to **3** and `--sduration` to **5**. In this scenario, the input video is evenly split into **3** parts, and the first **5** seconds from each part are extracted for previews. Subsequently, these segments are concatenated and converted into a single video or gif. Thus the resulting preview will be of **5x3 = 15 seconds**.

The red parts are extracted for previews

![segments](https://raw.githubusercontent.com/Tetrax-10/batch-preview-generator/main/assets/segments.png)

</br>

## Development

##### Environment setup

```sh
git clone https://github.com/Tetrax-10/batch-preview-generator
cd batch-preview-generator
pip install termcolor progress pyreadline3 pyinstaller
```

##### Run

```sh
python preview.py <args>
```

##### Build executable

```sh
pyinstaller preview.spec
```

Make sure to add your "dist" folder to the PATH so that when you run preview, it refers to your "dist" executable. Additionally, also ensure that the path of the installed "preview.exe" is removed during development.

The installer is compiled with the [Inno Setup Compiler](https://jrsoftware.org/isdl.php), and there's no need to perform this step during the development of Batch Preview Generator, as it is only used for distribution

</br>

### Known bugs

1. When this program is installed and uninstalled it leaves this string ";;" in PATH environmental variable, it's not an issue as it doesn't affect the env vars but its a bloat, So please help me fix this as I'm not good with Inno Setup Compiler

### Assist required

1. I don't have an AMD gpu to implement H/W acceleration
2. Help me fix the `known bugs`

</br>

### Support

Like This Tool? Gimme Some ❤️ by Liking this Repository.
