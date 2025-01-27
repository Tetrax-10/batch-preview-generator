import argparse
import readline
import os
import sys
import glob as globpy

from termcolor import colored

import utils.glob as glob
import utils.ffmpeg as ffmpeg

shared = {"args": None}


def init():
    version = "1.3"

    default_path = glob.get_cwd()
    default_out = glob.join_path(glob.get_cwd(), "previews")
    default_resolution = 360
    default_segments = 10
    default_sduration = 1.0
    default_skip_first_n_sec = 20.0
    default_audio = False
    default_gif = False
    default_gif_fps = 15
    default_fps = 24
    default_quality = "normal"
    default_compression = "slow"

    parser = argparse.ArgumentParser(description=f'Generates preview videos and GIFs using FFmpeg CLI in batch. Visit {colored("https://github.com/Tetrax-10/batch-preview-generator#arguments", "blue")} to view detailed docs')
    parser.add_argument("-p", "--path", help="Path of the video or folder for batch processing", type=str, metavar="")
    parser.add_argument("-o", "--out", help="Output folder for generated previews", type=str, metavar="")
    parser.add_argument("-r", "--resolution", help="Preview video resolution", type=int, metavar="")
    parser.add_argument("-s", "--segments", help="No. of segments in a preview video", type=int, metavar="")
    parser.add_argument("-sd", "--sduration", help="Duration of a segment", type=float, metavar="")
    parser.add_argument("-sk", "--skip", help="Skip first n seconds", type=str, metavar="")
    parser.add_argument("-sp", "--samepath", help="The output will be generated in the input path folder", action="store_true")
    parser.add_argument("-a", "--audio", help="Previews will be generated with audio", action="store_true")
    parser.add_argument("-g", "--gif", help="Previews will be generated in the GIF format (takes more time & space)", action="store_true")
    parser.add_argument("-f", "--fps", help="Preview video FPS", type=int, metavar="")
    parser.add_argument("-q", "--quality", help="Preview quality (low/normal/high)", type=str, metavar="")
    parser.add_argument("-c", "--compression", help="Preview compression mode (fast/slow/veryslow)", type=str, metavar="")
    parser.add_argument("-cli", "--cli", help="Run as a CLI without changing default args", action="store_true")
    parser.add_argument("-cuda", "--cuda", help="Hardware acceleration: Uses Nvidia's cuda cores", action="store_true")
    parser.add_argument("-v", "--version", help="Prints version info", action="store_true")

    args = parser.parse_args()

    if any(value is not None and value is not False for value in vars(args).values()):
        args.cli = True

    shared["args"] = vars(args)

    if args.version == True:
        print(version)
        sys.exit()

    if not ffmpeg.check("ffmpeg -version") or not ffmpeg.check("ffprobe -version"):
        exit_program()

    if not any(value is not None and value is not False for value in vars(args).values()):

        def pathCompleter(text, state):
            matches = []
            for x in globpy.glob(text + "*"):
                if not os.path.isfile(x):
                    x += "/"
                matches.append(x.replace("\\", "/"))
            return matches[state]

        try:
            readline.set_completer_delims("\t")
            readline.parse_and_bind("tab: complete")
            readline.set_completer(pathCompleter)

            input_path = input(colored(f'Path of the video or folder ({colored(default_path, "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.path = glob.get_abs_path(glob.correct_path(input_path)) if input_path != "" else default_path

            if glob.is_file(args.path):
                default_out = glob.join_path(glob.get_dirname(args.path), "previews")
            else:
                default_out = glob.join_path(args.path, "previews")
            input_out = input(colored(f'Output folder ({colored(default_out, "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.out = glob.get_abs_path(glob.correct_path(input_out)) if input_out != "" else default_out

            readline.set_completer(None)

            input_resolution = input(colored(f'Resolution ({colored(default_resolution, "yellow")}{colored("): ", "blue")}', "blue"))
            args.resolution = int(input_resolution) if input_resolution != "" else default_resolution

            input_segments = input(colored(f'No. of segments ({colored(default_segments, "yellow")}{colored("): ", "blue")}', "blue"))
            args.segments = int(input_segments) if input_segments != "" else default_segments

            input_sduration = input(colored(f'Segment duration ({colored(default_sduration, "yellow")}{colored("): ", "blue")}', "blue"))
            args.sduration = float(input_sduration) if input_sduration != "" else default_sduration

            input_skip = input(colored(f'Skip first n seconds ({colored(default_skip_first_n_sec, "yellow")}{colored("): ", "blue")}', "blue"))
            args.skip = float(input_skip) if input_skip != "" else default_skip_first_n_sec

            input_audio = input(colored(f'Audio ({colored("false", "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.audio = True if input_audio.lower() == "true" else False

            if not args.audio:
                input_gif = input(colored(f'Gif ({colored("false", "yellow")}{colored("): ", "blue")}', "blue")).strip()
                args.gif = True if input_gif.lower() == "true" else False

            input_fps = input(colored(f'FPS ({colored(default_gif_fps if args.gif else default_fps, "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.fps = int(input_fps) if input_fps != "" else (default_gif_fps if args.gif else default_fps)

            input_quality = input(colored(f'Quality (low/normal/high) ({colored(default_quality, "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.quality = input_quality.lower() if input_quality != "" else default_quality

            input_compression = input(colored(f'Compression mode (fast/slow/veryslow) ({colored(default_compression, "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.compression = input_compression.lower() if input_compression != "" else default_compression

            input_hwacc = input(colored(f'Hardware acceleration (false/cuda) ({colored("false", "yellow")}{colored("): ", "blue")}', "blue")).strip()
            args.cuda = True if input_hwacc.lower() == "cuda" else False

            os.system("cls")
        except Exception as err:
            print()
            if "invalid literal for int()" in str(err):
                print(colored("Invalid input type, That field only accepts numbers", "red"))
            else:
                print(colored("Invalid input type", "red"))

            exit_program()

    else:
        args.path = glob.get_abs_path(glob.correct_path(args.path)) if args.path else default_path
        args.out = glob.correct_path(args.out) if args.out else default_out
        args.resolution = args.resolution if args.resolution else default_resolution
        args.segments = args.segments if args.segments else default_segments
        args.sduration = args.sduration if args.sduration else default_sduration
        args.skip = float(args.skip) if args.skip else default_skip_first_n_sec
        args.audio = args.audio if args.audio else default_audio
        args.gif = args.gif if args.gif else default_gif
        args.fps = args.fps if args.fps else (default_gif_fps if args.gif else default_fps)
        args.quality = args.quality.lower() if args.quality else default_quality
        args.compression = args.compression.lower() if args.compression else default_compression

        print()

    args.version = version

    if args.samepath:
        if default_out != args.out:
            if glob.is_abs(args.out):
                print(colored("Outpath should be a relative path when using --samepath", "red"))
                exit_program()
        else:
            args.out = "."
    else:
        args.out = glob.get_abs_path(args.out)

    if args.gif:
        args.audio = False

    args.quality = "high" if args.quality == "high" else ("low" if args.quality == "low" else default_quality)
    args.compression = "veryslow" if args.compression == "veryslow" else ("fast" if args.compression == "fast" else default_compression)

    shared["args"] = vars(args)
    return args


def log_args(args):
    print(colored("Configuration:", "yellow", attrs=["bold", "underline"]))
    print()
    print(colored("Input Path:", "blue"), colored(args.path, "yellow"))
    print(colored("Output path:", "blue"), colored(args.out, "yellow"))
    print(colored("Resolution:", "blue"), colored(args.resolution, "yellow"))
    print(colored("No. of Segments:", "blue"), colored(args.segments, "yellow"))
    print(colored("Segment Duration:", "blue"), colored(args.sduration, "yellow"))
    print(colored("Skip first n sec:", "blue"), colored(args.skip, "yellow"))
    if not args.gif:
        print(colored("Audio:", "blue"), colored(args.audio, "yellow"))
    if not args.audio:
        print(colored("Gif:", "blue"), colored(args.gif, "yellow"))
    print(colored("FPS:", "blue"), colored(args.fps, "yellow"))
    print(colored("Quality:", "blue"), colored(args.quality, "yellow"))
    print(colored("Compression mode:", "blue"), colored(args.compression, "yellow"))
    print(colored("Hardware acceleration:", "blue"), colored("cuda" if args.cuda else "False", "yellow"))
    print()


def get_args():
    return shared["args"]


def exit_program():
    print()
    if shared["args"]["cli"] != True:
        input(colored("Press enter to exit...", "green"))
    sys.exit()
