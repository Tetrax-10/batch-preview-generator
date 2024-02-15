import subprocess

from termcolor import colored


def check(cmd):
    output = run_cmd(cmd)
    if "not recognized" in output.stderr:

        unavailable_tool = ""
        if "ffmpeg" in output.stderr:
            unavailable_tool = "FFmpeg"
        else:
            unavailable_tool = "FFprobe"

        print(colored(f"{unavailable_tool} not found!", "red"))
        print()
        print(f"Please install {unavailable_tool} or install the Batch Preview Generator (FFmpeg included) version from")
        print(
            colored(
                "https://github.com/Tetrax-10/batch-preview-generator/releases/latest",
                "blue",
            )
        )

        return False

    return True


def run_cmd(cmd):
    output = subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )
    return output


def get_video_duration(file):
    ffprobe_cmd = f'ffprobe -v panic -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file}"'

    output = run_cmd(ffprobe_cmd).stdout

    if output:
        try:
            return round(float(output), 3)
        except Exception:
            return 0
    else:
        return 0


def get_video_bitrate(file):
    ffprobe_cmd = f'ffprobe -v panic -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 "{file}"'

    output = run_cmd(ffprobe_cmd).stdout.strip()

    if output.isnumeric():
        return output
    else:
        return "3500000"


def generate_preview_chunck(file, start_duration, bitrate, args, temp_path, out_file_name):
    audio_settings = "-c:a aac -b:a 128k" if (args.audio) else "-an"

    crf = "22"
    if args.quality == "high":
        crf = "15"
        bitrate = int(bitrate) * 2.5
    elif args.quality == "low":
        crf = "30"
    else:
        bitrate = int(bitrate) + 500000

    hw_acc_pre_input = ""
    encoder = "libx264"
    scale = "scale"
    pix_fmt = " -pix_fmt yuv420p"
    preset = args.compression

    if args.cuda:
        hw_acc_pre_input = " -hwaccel cuda -hwaccel_output_format cuda"
        encoder = "h264_nvenc"
        scale = "scale_cuda"
        pix_fmt = ""

        bitrate = f" -b:v {bitrate}"
        if args.quality == "low":
            bitrate = ""

        if preset == "veryslow":
            preset = "p7"
        elif preset == "slow":
            preset = "p5"
        elif preset == "fast":
            preset = "p3"
    else:
        bitrate = ""

    ffmpeg_cmd = f'ffmpeg -v panic -y -xerror{hw_acc_pre_input} -ss {start_duration} -i "{file}" -t {args.sduration} -max_muxing_queue_size 1024 -c:v {encoder} -vf {scale}=-1:{args.resolution}{pix_fmt}{bitrate} -profile:v high -level 4.2 -preset {preset} -crf {crf} -r {args.fps} -strict -2 {audio_settings} "{temp_path}/{out_file_name}.mp4"'

    run_cmd(ffmpeg_cmd)


def generate_preview(temp_file_path, preview_file_path, args):
    ffmpeg_cmd = ""

    if args.gif:
        if args.quality == "high":
            ffmpeg_cmd = f'ffmpeg -v panic -y -f concat -i "{temp_file_path}" -max_muxing_queue_size 1024 -threads 4 -vf "fps={args.fps},scale=-2:{args.resolution}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -c:v gif -loop 0 -strict -2 "{preview_file_path}.gif"'
        else:
            ffmpeg_cmd = f'ffmpeg -v panic -y -f concat -i "{temp_file_path}" -max_muxing_queue_size 1024 -threads 4 -vf "fps={args.fps},scale=-2:{args.resolution}:flags=lanczos" -c:v gif -loop 0 -strict -2  "{preview_file_path}.gif"'
    else:
        ffmpeg_cmd = f'ffmpeg -v panic -y -f concat -i "{temp_file_path}" -max_muxing_queue_size 1024 -threads 4 -c:v copy -c:a copy -strict -2 "{preview_file_path}.mp4"'

    run_cmd(ffmpeg_cmd)
