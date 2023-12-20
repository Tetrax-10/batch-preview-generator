import sys
import subprocess

from termcolor import colored


def check(cmd):
    output = run_cmd(cmd)
    if ("not recognized" in output.stderr):

        unavailable_tool = ""
        if ("ffmpeg" in output.stderr):
            unavailable_tool = "FFmpeg"
        else:
            unavailable_tool = "FFprobe"

        print(colored(f"{unavailable_tool} not found!", "red"), "\n")
        print(f"Please install {unavailable_tool} or install the Batch Preview Generator (FFmpeg included) version from")
        print(colored("https://github.com/Tetrax-10/batch-preview-generator/releases/latest", "blue"))

        return False

    return True


def run_cmd(cmd):
    output = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return output


def get_video_duration(file):
    ffprobe_cmd = f"ffprobe -v panic -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"{file}\""

    output = run_cmd(ffprobe_cmd).stdout

    if output:
        try:
            return round(float(output), 3)
        except Exception:
            return 0
    else:
        return 0


def generate_preview_chunck(file, start_duration, segments_duration, resolution, audio, gif, index, count):
    audio_settings = "-an"
    if audio and not gif:
        audio_settings = "-c:a aac -b:a 128k"

    ffmpeg_cmd = f"ffmpeg -v panic -y -xerror -ss {start_duration} -i \"{file}\" -t {segments_duration} -max_muxing_queue_size 1024 -c:v libx264 -vf scale=-1:{resolution} -pix_fmt yuv420p -profile:v high -level 4.2 -preset slow -crf 21 -threads 4 -strict -2 {audio_settings} \"temp/{index}-{count}.mp4\""

    run_cmd(ffmpeg_cmd)


def generate_preview(temp_file_path, preview_file_path, resolution, gif):
    ffmpeg_cmd = ""

    if gif:
        ffmpeg_cmd = f"ffmpeg -v panic -f concat -i \"{temp_file_path}\" -y -vf \"fps=10,scale=-1:{resolution}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" -c:v gif -loop 0 \"{preview_file_path}.gif\""
    else:
        ffmpeg_cmd = f"ffmpeg -v panic -f concat -i \"{temp_file_path}\" -y -c:v copy -c:a copy \"{preview_file_path}.mp4\""

    run_cmd(ffmpeg_cmd)
