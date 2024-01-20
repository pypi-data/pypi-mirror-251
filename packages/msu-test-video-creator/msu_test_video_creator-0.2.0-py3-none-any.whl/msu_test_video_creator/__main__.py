import logging
import sys
import argparse
import yaml
import os.path

from video_creator import VideoCreator
from version import Version


def cli():
    try:
        parser = argparse.ArgumentParser("msu_test_video_creator",
                                         description="Commandline Python application for generating mp4 and wav files for an msu")
        parser.add_argument("-f", "--files", help="The list of PCM files to include", type=str)
        parser.add_argument("-i", "--input", help="Input YAML file with a list of all PCM files to include", type=str)
        parser.add_argument("-o", "--output", help="The output mp4 file to create", type=str)
        parser.add_argument("-v", "--version", help="Get the version number", action='store_true')
        args = parser.parse_args()

        if args.version:
            print("msu_test_video_creator v" + Version.name())
            exit(1)

        if not args.files and not args.input:
            print("usage: msu_test_video_creator [-h] [-f FILES] [i INPUT] [-o OUTPUT] [-v]")
            print("msu_test_video_creator: error: you must include either the argument -f/--files or -i/--input")
            exit(1)

        if not args.output:
            print("usage: msu_test_video_creator [-h] [-f FILES] [i INPUT] [-o OUTPUT] [-v]")
            print("msu_test_video_creator: error: the following arguments are required: -o/--output")
            exit(1)

        if args.files:
            pcm_files = args.files.split(",")
        else:
            if not os.path.isfile(args.input):
                print("error: the input YAML file was not found")
                exit(1)
            with open(args.input, "r") as stream:
                try:
                    pcm_files = yaml.safe_load(stream)['Files']
                except yaml.YAMLError as exc:
                    print("error: could not parse input YAML file")
                    exit(1)

        print(pcm_files)

        creator = VideoCreator(pcm_files, args.output)

        creator.create_video()

        exit(0)

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    cli()
