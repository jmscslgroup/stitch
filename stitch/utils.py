import os
import re
import ffmpeg
import datetime


def info(video):

    name = os.path.basename(video)
    search = r"(\d{4}_\d{4}_\d{6})_(\d{3}).*"
    y_md_hms, index = re.search(search, name).groups()
    dt = datetime.datetime.strptime(y_md_hms, "%Y_%m%d_%H%M%S")
    
    res = {
        "indexstr": index,
        "index": int(index),
        "dt": dt
    }
    return res


def compare(vid1, vid2):
    info1 = info(vid1)
    info2 = info(vid2)

    if not (
        info1["dt"].year == info2["dt"].year
        and info1["dt"].month == info2["dt"].month
    ):
        return False

    first_v, first_i = (
        (vid1, info1) if info1["index"] <= info2["index"] else (vid2, info2)
    )
    second_v, second_i = (
        (vid1, info1) if info1["index"] > info2["index"] else (vid2, info2)
    )

    probe = ffmpeg.probe(first_v)
    vid_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    first_dur = float(vid_stream["duration"])
    first_dur = datetime.timedelta(seconds=first_dur)

    return abs(((first_i["dt"] + first_dur) - second_i["dt"]).total_seconds()) < 5

def create_name(drive):
    drive = sorted(drive)
    inf = info(drive[0])
    indices = [info(f)["indexstr"] for f in drive]
    date = inf["dt"].strftime("%Y%m%d")
    return f"{date}_{'_'.join(indices)}.mp4"


def create_combinations(drive_list):
    drives = []

    for file in drive_list:
        for drive in drives:
            leave = False
            for f in drive:
                if compare(file, f):
                    drive.append(file)
                    leave = True
                    break
            if leave:
                break
        else:
            drives.append([file])

    structure = {create_name(d): d for d in drives}

    return structure