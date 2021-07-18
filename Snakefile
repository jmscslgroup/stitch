import os
from stitch.utils import create_combinations, info
import ffmpeg

config = {
    "resampled_dir": "resampled",
    "build_dir": "../../publishable-circles",
    "input_dir": "../../private-circles"
}

INPUT_DIR = config['input_dir']
BUILD_DIR = config['build_dir']
RESAMPLED_DIR = config['resampled_dir']

VIDEOS = glob_wildcards(INPUT_DIR + "/{vin,.{17}}/dashcams/{folder}/{year,.{4}}_{monthday,.{4}}_{time,.{6}}_{index,.{3}}.MP4")
PATHS = expand(INPUT_DIR + "/{vin}/dashcams/{folder}/{year}_{monthday}_{time}_{index}.MP4", zip, vin=VIDEOS.vin, folder=VIDEOS.folder, year=VIDEOS.year, monthday=VIDEOS.monthday, time=VIDEOS.time, index=VIDEOS.index)


def remove_bad_videos(paths, remove_from):
    for i, path in enumerate(paths):
        try:
            ffmpeg.probe(path)
            continue
        except:
            for field in remove_from._fields:
                del getattr(remove_from, field)[i]
            i -= 1

remove_bad_videos(PATHS, VIDEOS)

RAW = expand(INPUT_DIR + "/{vin}/dashcams/{folder}/{year}_{monthday}_{time}_{index}.MP4", zip, vin=VIDEOS.vin, folder=VIDEOS.folder, year=VIDEOS.year, monthday=VIDEOS.monthday, time=VIDEOS.time, index=VIDEOS.index)
RESAMPLED = expand(RESAMPLED_DIR + "/{vin}/dashcams/{folder}/{year}_{monthday}_{time}_{index}_rs.mp4", zip, vin=VIDEOS.vin, folder=VIDEOS.folder, year=VIDEOS.year, monthday=VIDEOS.monthday, time=VIDEOS.time, index=VIDEOS.index)

outputs = create_combinations(RAW)

FINAL_OUTPUT, FINAL_INPUT = zip(*outputs.items())

FINAL_OUTPUT = [os.path.join(os.path.dirname(v[0]).replace(INPUT_DIR, BUILD_DIR), k) for k, v in outputs.items()]
outputs = {k: sorted([f.replace(INPUT_DIR, RESAMPLED_DIR).replace(".MP4", "_rs.mp4") for f in v], key=lambda a: info(a)["index"]) for k, v in outputs.items()}

rule all:
   input:
       FINAL_OUTPUT
    

rule resample:
    input:
        INPUT_DIR+"/{vin}/dashcams/{folder}/{year}_{monthday}_{time}_{index}.MP4"
    output:
        RESAMPLED_DIR+"/{vin}/dashcams/{folder}/{year}_{monthday}_{time}_{index}_rs.mp4"
    shell:
        "python -m stitch resample -i {input} -o {output}"

rule concatenate:
    input:
        lambda w: outputs[f"{w.ymd}_{w.indices}.mp4"]
    output:
        BUILD_DIR + "/{vin}/dashcams/{folder}/{ymd}_{indices}.mp4"
    params:
        with_i = lambda w: " ".join([f"-i {i}" for i in outputs[f"{w.ymd}_{w.indices}.mp4"]])
    shell:
        "python -m stitch concatenate {params.with_i} -o {output}"
        
rule clean:
    shell:
        """
        rm -rf {config[intermediate_dir]}
        """