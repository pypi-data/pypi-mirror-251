#!/usr/bin/env python3.10
import argparse
import os
import pathlib
from .sub_movie_generator import SubMovieGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Foxlator enables automatic subtitle generation based on the audio track and generates a new video file with the created subtitles')

    parser.add_argument('--movie-path',
                        type=pathlib.Path,
                        help='path to the movie',
                        required=True)
    parser.add_argument('--destination',
                        type=pathlib.Path,
                        help='path to destination dir or file',
                        default=os.getcwd())
    parser.add_argument('--model-size',
                        type=str,
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        default='large',
                        help='STT model size')
    parser.add_argument('--language',
                        default=None,
                        type=str,
                        help='Language into which subtitles should be translated. If you do not specify the language will be automatically selected')

    args = parser.parse_args()
    return SubMovieGenerator(args.movie_path, args.model_size, args.language).gen_movie_with_subtitles(args.destination)


if __name__ == "__main__":
    main()
