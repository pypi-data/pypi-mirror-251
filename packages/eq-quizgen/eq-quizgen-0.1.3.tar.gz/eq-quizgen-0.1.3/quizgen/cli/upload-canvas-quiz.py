import argparse
import os
import sys

import quizgen.converter.canvas
import quizgen.quiz

DEFAULT_BASE_URL = 'https://canvas.ucsc.edu'

def run(args):
    if (not os.path.exists(args.path)):
        raise ValueError(f"Provided path '{args.path}' does not exist.")

    if (not os.path.isfile(args.path)):
        raise ValueError(f"Provided path '{args.path}' is not a file.")

    quiz = quizgen.quiz.Quiz.from_path(args.path)
    canvas_instance = quizgen.converter.canvas.InstanceInfo(args.base_url, args.course_id, args.token)

    converter = quizgen.converter.canvas.CanvasUploader(canvas_instance, force = args.force)
    converter.convert_quiz(quiz)

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description =
        "Parse a quiz and upload the quiz to Canvas.")

    parser.add_argument('path',
        type = str,
        help = 'The path to a quiz json file.')

    parser.add_argument('--course', dest = 'course_id',
        action = 'store', type = str, required = True,
        help = 'Course ID to upload the quiz under.')

    parser.add_argument('--url', dest = 'base_url',
        action = 'store', type = str, default = DEFAULT_BASE_URL,
        help = 'The base URL for the Canvas instance (default: %(default)s).')

    parser.add_argument('--token', dest = 'token',
        action = 'store', type = str, required = True,
        help = 'The authentication token to use with Canvas.')

    parser.add_argument('--force', dest = 'force',
        action = 'store_true', default = False,
        help = 'Override (delete) any exiting quiz with the same name.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
