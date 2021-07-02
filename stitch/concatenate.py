import ffmpeg
import tempfile
import os
import argparse
import sys
import shutil


def not_short_check(drives):

    if len(drives) == 1:
        probe = ffmpeg.probe(drives[0])
        vid_info = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        duration = float(vid_info["duration"])

        if duration < 30:
            exit(0)


def trim_files(drives, outputfolder):

    files = drives.copy()

    for i, (f, _) in enumerate(zip(drives, drives[1:])):
        probe = ffmpeg.probe(f)
        vid_info = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        duration = float(vid_info["duration"])

        name = os.path.basename(f)
        outname = os.path.join(outputfolder, name)

        # not using filter trim for faster processing
        ffmpeg.input(f, to=duration - 1).output(outname, c="copy").run(
            overwrite_output=True
        )
        files[i] = outname

    return files


def concatenate(files, output):

    trimmed_dir = "trimmed_" + next(tempfile._get_candidate_names())
    os.mkdir(trimmed_dir)

    not_short_check(files)

    trimmed = trim_files(files, trimmed_dir)

    videolist = f"drive_{next(tempfile._get_candidate_names())}.txt"

    # create temp file with names
    with open(videolist, "w") as tmp:
        for f in trimmed:
            tmp.write(f"file {f}\n")

    # concatenate demuxer
    ffmpeg.input(videolist, format="concat", safe=0).output(output, c="copy").run(
        overwrite_output=True
    )

    os.remove(videolist)
    shutil.rmtree(trimmed_dir)
