#!/usr/bin/env python
"""
Main file to deploy markdown file into site

Parse markdown file and deploy it step-by-step into lesson.

# Lesson title
lesson=1234
## step1 header
markdown text
## QUIZ
question in AIKEN format
"""
import md_utils
from step import Step

from enum import Enum
import json
import pprint
import re
import sys

def is_empty_line(line):
    return not line.strip()


def error(message="Error"):
    raise ValueError(message)


def commit_step(steps, lesson_id, lines):
    """Create Step from lines and append to steps list"""
    st = Step.from_lines(lines)
    st.lesson_id = lesson_id
    st.position = len(steps) + 1
    print(st)
    steps.append(st)

def commit_whole_file_as_1_step(steps, lesson_id, lines):
    """All steps in the first step to rereading"""
    st = Step()
    st.text = md_utils.html(lines)
    st.lesson_id = lesson_id
    st.position = len(steps) + 1
    print(st)
    steps.append(st)


def parse_lesson(lines):
    """
    Parse lesson document by format:
    # lesson header
    lesson_id = 123
    lesson text (lesson description in moodle, not used in stepik)
    ## step header
    step text
    ## next step header
    next step text
    :param lines:
    :return: steps=[], lesson_header='', lesson_id=None, lesson_text=''
    """
    class Status(Enum):
        LESSON_HEADER = 1
        LESSON_ID = 2
        LESSON_TEXT = 3
        H2 = 4
        STEP_BODY = 5

    status = Status.LESSON_HEADER
    lesson_header = ''
    lesson_id = None
    lesson_text = ''
    steps = []
    line_from = 0

    for line_to, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue
        if status == Status.LESSON_HEADER:                          # # lesson header
            m = re.match(r'(#[^#])(.*)', line)
            if not m:
                error(f'Expect lesson header # text, status={status}, now = {line}')
            lesson_header = m.group(2)
            print(f'lesson_header = {lesson_header}')
            status = Status.LESSON_ID

        elif status == Status.LESSON_ID:                            # lesson = lesson_id
            m = re.match(r'(\s*lesson\s*=\s*)(\d+)', line)
            if not m:
                error(f'Expect lesson header # text, status={status}, now = {line}')
            lesson_id = int(m.group(2))
            print(f'lesson_id={lesson_id}')
            status = Status.LESSON_TEXT
            line_from = line_to
            # add whole file as the first step:
            # commit_whole_file_as_1_step(steps, lesson_id, lines)

        elif status == Status.LESSON_TEXT:                          # text before first h2
            if re.match(r'##[^#]', line):
                lesson_text = md_utils.html(lines[line_from : line_to])
                status = Status.H2
                line_from = line_to

        elif status == Status.STEP_BODY:
            if re.match(r'##[^#]', line):
                commit_step(steps, lesson_id, lines[line_from : line_to])
                status = Status.H2
                line_from = line_to

        elif status == Status.H2:
            status = Status.STEP_BODY

    commit_step(steps, lesson_id, lines[line_from:])

    return steps, lesson_header, lesson_id, lesson_text


def deploy_to_stepik(steps, lesson_id):
    """Upload steps to site into lesson_id by update site steps, create or delete steps if needed."""
    step_ids = Step.get_step_ids_for_lesson(lesson_id)
    len_data = len(steps)
    len_site = len(step_ids)
    for step_id, step in zip(step_ids, steps):
        step.id = step_id
        print('UPDATE', step)
        step.update()

    # create (add) new steps if needed
    if len_site < len_data:
        for step in steps[len_site:]:
            step.create()
            print('CREATE', step)

    # delete obligatory steps if needed
    elif len_site > len_data:
        for step_id in step_ids[len_data:]:
            print('DELETE', step_id)
            Step.delete_by_id(step_id)

def print_to_html_file(md_filename, steps):
    """
    print text as html into html filename
    """
    filename = md_filename[:-2]+'html'
    print(f'Save HTML into {filename}')
    with open (filename, 'w', encoding='utf-8') as fout:
        for st in steps:
            fout.write(st.text)

def usage():
    print(f'USAGE: {__file__} markdown_filename')


# def main_old_argv():

def main():
    """Read input file, split into steps, upload to site"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy markdown file into site or convert to html for manual deploying')
    parser.add_argument('markdown_filename', metavar='FILE', type=str, help='input markdown file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--full", action="store_true", help='deploy all steps')
    group.add_argument("-t", "--text", action="store_true", help='deploy only text steps')
    parser.add_argument('-d', '--debug', action='store_true', help='deploy all steps in the first one to debug formatting')
    parser.add_argument('--html', action='store_true', help='deploy all steps into 1 HTML file, not to site')
    args = parser.parse_args()

    print('FILE =', args.markdown_filename)
    if args.html:
        print ('--html')
    if args.debug:
        print ('--html')
    if args.full:
        print('deploy full')
    elif args.text:
        print('deploy TEXT only')
    else:
        print('deploy nothing')
    
    '''
    
    with open(sys.argv[1], encoding='utf-8') as fin:
        steps, lesson_header, lesson_id, lesson_text = parse_lesson(list(fin))
        
        #deploy_to_stepik(steps[1:], lesson_id)
        print_to_html_file(sys.argv[1], steps)
    '''

if __name__ == '__main__':
    main()