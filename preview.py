import os

from termcolor import colored
from progress.bar import IncrementalBar

import utils.commander as commander
import utils.ffmpeg as ffmpeg
import utils.glob as glob
import utils.utils as utils


def process_previews(args, video_files):
    temp_folder_path = glob.join_path(glob.get_cwd(), "temp")
    glob.delete_folder(temp_folder_path)
    glob.create_folder(temp_folder_path)

    glob.create_folder(args.out)

    is_invalid_duration = False

    if (len(video_files)):
        for index, video_file in enumerate(video_files):
            file_name = glob.get_file_name(video_file)
            file_extension = glob.get_file_name(video_file, "ext")
            relative_path = f"{file_name}.{file_extension}" if os.path.relpath(video_file, args.path) == "." else os.path.relpath(video_file, args.path)
            video_duration = ffmpeg.get_video_duration(video_file)

            expected_preview_duration = round(args.segments * args.sduration)
            if (expected_preview_duration < round(video_duration)):
                ratio = round(video_duration/args.segments, 3)
                temp_file_contents = ""

                video_segment_prog = IncrementalBar(utils.wrap_text(relative_path), max=round(args.segments) + 1, suffix='%(percent)d%%')

                count = 0
                while count < round(args.segments):
                    if count == 0:
                        video_segment_prog.update()  # prints the progress bar even before finishing this loop event
                    start_time = args.skip if count == 0 else round(count*ratio, 3)
                    ffmpeg.generate_preview_chunck(video_file, start_time, args, index, count)
                    temp_file_contents += f"file '{index}-{count}.mp4'\n"
                    video_segment_prog.next()
                    count += 1

                temp_file_path = glob.join_path(temp_folder_path, f"{index}.txt")
                with open(temp_file_path, "w") as file:
                    file.write(temp_file_contents)

                ffmpeg.generate_preview(temp_file_path, f"{glob.join_path(args.out, f"{file_name} preview")}", args)
                video_segment_prog.next()
                video_segment_prog.finish()
            else:
                if video_duration > 0:
                    print(colored(f"skiped [Invalid duration ({round(video_duration)}:{expected_preview_duration})]: ", "yellow"), relative_path)
                else:
                    print(colored(f"skiped [Unavailable duration]", "yellow"), relative_path)

                is_invalid_duration = True
    else:
        print(colored("No videos found in the specified folder", "red"))

    if is_invalid_duration:
        print()
        print(colored("Warning codes:", "yellow"))
        print(colored("    1.Unavailable duration: Can't fetch the video duration", "yellow"))
        print(colored("    2.Invalid duration (video duration:expected preview duration): Estimated preview video is equal or longer than the actual video", "yellow"))

    glob.delete_folder(temp_folder_path)


if __name__ == "__main__":
    args = commander.init()
    commander.log_args(args)

    video_files = glob.get_all_video_files(args.path)
    if video_files == False:
        commander.exit_program()
    else:
        process_previews(args, video_files)

    commander.exit_program()
