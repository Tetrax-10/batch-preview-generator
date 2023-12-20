import argparse
import readline
import os
import glob as globpy

from termcolor import colored

import utils.glob as glob


def init():
    default_path = glob.get_cwd()
    default_out = glob.join_path(glob.get_cwd(), "previews")
    default_resolution = 360
    default_segments = 10
    default_sduration = 1.0
    default_skip_first_n_sec = 20
    default_audio = False
    default_gif = False
    default_gif_fps = 10
    default_fps = 24

    parser = argparse.ArgumentParser(description=f"Generates preview videos and GIFs using FFmpeg CLI in batch. Visit {colored("https://github.com/Tetrax-10/batch-preview-generator", "blue")} to view some examples and docs")
    parser.add_argument("-p", "--path", help="Path of the video or folder for batch processing", type=str, metavar="")
    parser.add_argument("-o", "--out", help="Output folder for generated previews", type=str, metavar="")
    parser.add_argument("-r", "--resolution", help="Preview video resolution", type=int, metavar="")
    parser.add_argument("-s", "--segments", help="No. of segments in a preview video", type=int, metavar="")
    parser.add_argument("-sd", "--sduration", help="Duration of a segment", type=float, metavar="")
    parser.add_argument("-sk", "--skip", help="Skip first n seconds", type=int, metavar="")
    parser.add_argument("-sp", "--samepath", help="The output will be generated in the input path folder", action="store_true")
    parser.add_argument("-a", "--audio", help="Previews will be generated with audio", action="store_true")
    parser.add_argument("-g", "--gif", help="Previews will be generated in the GIF format (takes more time & space)", action="store_true")
    parser.add_argument("-f", "--fps", help="Preview video FPS", type=int, metavar="")
    parser.add_argument("-cli", "--cli", help="Run as a CLI without changing default args", action="store_true")

    args = parser.parse_args()

    if not any(value is not None and value is not False for value in vars(args).values()):
        def pathCompleter(text, state):
            matches = []
            for x in globpy.glob(text + '*'):
                if not os.path.isfile(x):
                    x += "/"
                matches.append(x.replace("\\", "/"))
            return matches[state]

        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(pathCompleter)

        input_path = input(colored(f"Path of the video or folder for batch processing ({colored(default_path, "yellow")}{f"{colored("): ", "blue")}"}", "blue")).strip()
        args.path = glob.get_abs_path(glob.correct_path(input_path)) if input_path != "" else default_path

        input_out = input(colored(f"Output folder ({colored(default_out, "yellow")}{f"{colored("): ", "blue")}"}", "blue")).strip()
        args.out = glob.get_abs_path(glob.correct_path(input_out)) if input_out != "" else default_out

        input_resolution = input(colored(f"Preview resolution ({colored(default_resolution, "yellow")}{f"{colored("): ", "blue")}"}", "blue"))
        args.resolution = int(input_resolution) if input_resolution != "" else default_resolution

        input_segments = input(colored(f"No. of segments ({colored(default_segments, "yellow")}{f"{colored("): ", "blue")}"}", "blue"))
        args.segments = int(input_segments) if input_segments != "" else default_segments

        input_sduration = input(colored(f"Segment duration ({colored(default_sduration, "yellow")}{f"{colored("): ", "blue")}"}", "blue"))
        args.sduration = float(input_sduration) if input_sduration != "" else default_sduration

        input_skip = input(colored(f"Skip first n seconds ({colored(default_skip_first_n_sec, "yellow")}{f"{colored("): ", "blue")}"}", "blue"))
        args.skip = int(input_skip) if input_skip != "" else default_skip_first_n_sec

        input_audio = input(colored(f"Enable audio ({colored("false", "yellow")}{f"{colored("): ", "blue")}"}", "blue")).strip()
        args.audio = True if input_audio == "true" else False

        if not args.audio:
            input_gif = input(colored(f"Gif ({colored("false", "yellow")}{f"{colored("): ", "blue")}"}", "blue")).strip()
            args.gif = True if input_gif == "true" else False

        input_fps = input(colored(f"Preview FPS ({colored(default_gif_fps if args.gif else default_fps, "yellow")}{f"{colored("): ", "blue")}"}", "blue")).strip()
        args.fps = int(input_fps) if input_fps != "" else default_gif_fps if args.gif else default_fps

    else:
        args.path = glob.get_abs_path(glob.correct_path(args.path)) if args.path != None and args.path != "" else default_path
        args.out = glob.get_abs_path(glob.correct_path(args.out)) if args.out != None and args.out != "" else default_out
        args.resolution = args.resolution if args.resolution != None else default_resolution
        args.segments = args.segments if args.segments != None else default_segments
        args.sduration = args.sduration if args.sduration != None else default_sduration
        args.skip = args.skip if args.skip != None else default_skip_first_n_sec
        args.audio = args.audio if args.audio != None else default_audio
        args.gif = args.gif if args.gif != None else default_gif
        args.fps = args.fps if args.fps != None else default_gif_fps if args.gif else default_fps

    if (args.samepath):
        args.out = args.path

    if (args.gif):
        args.audio = False

    return args


def log_args(args):
    print("\n" + colored(f"Input Path:", "blue"), colored(f"{args.path}", "yellow"))
    print(colored(f"Output path:", "blue"), colored(f"{args.out}", "yellow"))
    print(colored(f"Preview Resolution:", "blue"), colored(f"{args.resolution}", "yellow"))
    print(colored(f"No. of Segments:", "blue"), colored(f"{args.segments}", "yellow"))
    print(colored(f"Segment Duration:", "blue"), colored(f"{args.sduration}", "yellow"))
    print(colored(f"Skip first n sec:", "blue"), colored(f"{args.skip}", "yellow"))
    if not args.gif:
        print(colored(f"Enable audio:", "blue"), colored(f"{args.audio}", "yellow"))
    if not args.audio:
        print(colored(f"Gif:", "blue"), colored(f"{args.gif}", "yellow"))
    print(colored(f"Preview FPS:", "blue"), colored(f"{args.fps}", "yellow") + "\n")
