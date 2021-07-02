import argparse
import sys

from stitch import resample
from stitch import concatenate

def get_args():

    parser = argparse.ArgumentParser()
    parser.set_defaults(which="all")

    subparsers = parser.add_subparsers()

    concatenate = subparsers.add_parser("concatenate")
    concatenate.set_defaults(which="concatenate")

    concatenate.add_argument("-i", "--input", required = True, action="append", help = "Videos that will be concatenated.")
    concatenate.add_argument("-o", "--output", required = True, help = "Output concatenated video.")

    resample = subparsers.add_parser("resample")
    resample.set_defaults(which="resample")

    resample.add_argument("-i", "--videoFileIn", required = True, help = "Input file name for video to be resampled.")
    resample.add_argument("-o", "--videoFileOut", required = True, help = "Output file name for resampled video.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    return args

def main():
    
    args = get_args()
    
    if args.which == "concatenate":
        concatenate(args.input, args.output)
    elif args.which == "resample":
        resample(args.input, args.output)
    
if __name__ == "__main__":
    main()
