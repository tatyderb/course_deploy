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
from step import Step, StepType

from enum import Enum
import json
import os
import os.path as op
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


def parse_lesson(lines, debug_format=False):
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
            if debug_format:
                commit_whole_file_as_1_step(steps, lesson_id, lines)

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


def deploy_to_stepik(steps, lesson_id, st_num = 0, allow_step_types = StepType.FULL):
    """Upload steps to site into lesson_id by update site steps, create or delete steps if needed."""
    step_ids = Step.get_step_ids_for_lesson(lesson_id)
    len_data = len(steps)
    len_site = len(step_ids)


    # update existing step when used "--step"
    if st_num != 0:
        st_num = st_num - 1 if st_num > 0 else len_data + st_num

        steps[st_num].id = step_ids[st_num]
        if steps[st_num].step_type & allow_step_types:
            print('UPDATE', steps[st_num])
            steps[st_num].update()
        else:
            print(f'SKIP UPDATE hstep={st.id} position={st.position}')
        return


    for step_id, step in zip(step_ids, steps):
        step.id = step_id
        if step.step_type & allow_step_types:
            print('UPDATE', step)
            step.update()
        else:
            print(f'SKIP UPDATE hstep={st.id} position={st.position}')
        

    # create (add) new steps if needed
    if len_site < len_data:
        for step in steps[len_site:]:
            if step.step_type & allow_step_types:
                step.create()
                print('CREATE', step)
            else:
                print(f'SKIP CREATE step={st.id} position={st.position}')
            

    # delete obligatory steps if needed
    elif len_site > len_data:
        for step_id in step_ids[len_data:]:
            if step.step_type & allow_step_types:
                print('DELETE', step_id)
                Step.delete_by_id(step_id)
            else:
                print(f'SKIP DELETE step={st.id} position={st.position}')
            

def print_to_html_file(md_filename, steps, allow_step_types = StepType.FULL):
    """
    print text as html into ./html directory
    """
    dir_part, file_part = op.split(md_filename)
    dir_part = op.join(dir_part, 'html')
    if not os.path.exists(dir_part):
        os.mkdir(dir_part)
    md_file, md_ext = op.splitext(file_part)
    filename = op.join(dir_part, md_file+'.html')
    print(f'Save HTML into {filename}')
    print('steps =', len(steps))
    
    with open (filename, 'w', encoding='utf-8') as fout:
        for sti, st in enumerate(steps):
            if st.step_type & allow_step_types:
                # fout.write(st.text)
                print(f'SAVE HTML step={st.id} position={st.position}')
                fout.write(st.html(sti+1))
            else:
                print(f'SKIP HTML step={st.id} position={st.position}')


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
    parser.add_argument('--step', type=int, default=0, help='deploy only the step which number you entered')
    args = parser.parse_args()

    print('FILE =', args.markdown_filename)
    if args.html:
        print ('--html')
    if args.debug:
        print ('--debug')
        
    if args.full:
        print('deploy full')
        deployed_step_types = StepType.FULL
    elif args.text:
        print('deploy TEXT only')
        deployed_step_types |= StepType.TEXT
    else:
        print('deploy all by default')
        deployed_step_types = StepType.FULL
    
    with open(args.markdown_filename, encoding='utf-8') as fin:
        # First step - all other steps as one page if mode = DEBUG
        steps, lesson_header, lesson_id, lesson_text = parse_lesson(list(fin), args.debug)
        
    
    # only convert to html, no deploy to site
    if args.html:
        print_to_html_file(args.markdown_filename, steps, allow_step_types=deployed_step_types)
    else:
        deploy_to_stepik(steps, lesson_id, st_num=args.step, allow_step_types=deployed_step_types)


if __name__ == '__main__':
    main()