import ffmpeg


def resample(input, output):
    ffmpeg.input(input).filter("scale", width="640", height="360").output(output).run()
