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
import secret_check
import md_utils
from st_types.steps import Step, StepType, from_lines
from st_types.st_basic import WRD, WRD_p

from pyparsing import Char, Word, CharsNotIn, ZeroOrMore, nums
from enum import Enum

import os
import os.path as op
import logging

logger = None

param_dict = {}


def is_empty_line(line):
    return not line.strip()


def error(message="Error"):
    raise ValueError(message)


def commit_step(steps, lesson_id, lines):
    """Create Step from lines and append to steps list"""
    # st = Step.from_lines(lines)

    if 'task_root' in param_dict:
        st = from_lines(lines, param_dict['task_root'])
    else:
        st = from_lines(lines)

    st.lesson_id = lesson_id
    st.position = len(steps) + 1
    logger.debug(st)
    steps.append(st)


def commit_whole_file_as_1_step(steps, lesson_id, lines):
    """All steps in the first step to rereading"""
    st = Step()
    st.text = md_utils.html(lines)
    st.lesson_id = lesson_id
    st.position = len(steps) + 1
    logger.debug(st)
    steps.append(st)


def read_params(filename):
    if filename is None:
        return

    with open(filename) as config:
        str_list = list(config)

    mask_eq = WRD + Char('=') + WRD

    for line_to, line in enumerate(str_list):
        if line == mask_eq:
            parse_res = mask_eq.parseString(line)
            param_dict[parse_res[0]] = parse_res[2]


def param_set(tokens):
    for idx, lex in enumerate(tokens):
        if tokens[idx] == '{{' and tokens[idx + 1] in param_dict and tokens[idx + 2] == '}}':
            tokens[idx] = tokens[idx + 2] = ''
            tokens[idx + 1] = param_dict[tokens[idx + 1]]
    return ' '.join(tokens)


def param_substitude(lines):
    mask_par = (CharsNotIn('{{}}')[0, ] + '{{' + WRD_p + '}}' + CharsNotIn('{{}}')[0, ])[1, ] + Char('\n')[0, 1]
    mask_par.setParseAction(param_set)

    for line_to, line in enumerate(lines):
        line = line.rstrip()

        if not line:
            continue

        lines[line_to] = mask_par.transformString(line)

    return lines


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
    :param debug_format:
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

    WRDs = ZeroOrMore(WRD)

    sharp = Char('#')
    not_sh = CharsNotIn('#')

    H2_template = (sharp * 2) + not_sh + WRDs
    header_template = sharp + not_sh + WRDs

    for line_to, line in enumerate(lines):
        line = line.rstrip()

        if not line:
            continue

        if status == Status.LESSON_HEADER:                          # # lesson header
            if not line == header_template:
                error(f'Expect lesson header # text, status={status}, now = {line}')

            m = header_template.parseString(line)
            lesson_header = m[1]

            logger.info(f'lesson_header = {lesson_header}')
            status = Status.LESSON_ID

        elif status == Status.LESSON_ID:                            # lesson = lesson_id

            id_template = 'lesson' + Char('=') + Word(nums)

            if not line == id_template:
                error(f'Expect lesson header # text, status={status}, now = {line}')

            lesson = id_template.parseString(line)
            lesson_id = int(lesson[2])

            logger.info(f'lesson_id={lesson_id}')
            status = Status.LESSON_TEXT
            line_from = line_to
            # add whole file as the first step:
            if debug_format:
                commit_whole_file_as_1_step(steps, lesson_id, lines)

        elif status == Status.LESSON_TEXT:                          # text before first h2
            if line == H2_template:
                lesson_text = md_utils.html(lines[line_from: line_to])
                status = Status.H2
                line_from = line_to

        elif status == Status.STEP_BODY:
            if line == H2_template:
                commit_step(steps, lesson_id, lines[line_from: line_to])
                status = Status.H2
                line_from = line_to

        elif status == Status.H2:
            status = Status.STEP_BODY

    commit_step(steps, lesson_id, lines[line_from:])

    return steps, lesson_header, lesson_id, lesson_text


def deploy_to_stepik(steps, lesson_id, st_num=0, allow_step_types=StepType.FULL):
    """Upload steps to site into lesson_id by update site steps, create or delete steps if needed."""
    step_ids = Step.get_step_ids_for_lesson(lesson_id)
    len_data = len(steps)
    len_site = len(step_ids)

    # update existing step when used "--step"
    if st_num != 0:
        ind = st_num - 1 if st_num > 0 else len_data + st_num  # getting index from straight step number or negative st

        if ind >= len_site:
            logger.warning("\nYou can't update step which wasn't uploaded before")
            return

        steps[ind].id = step_ids[ind]
        if steps[ind].step_type & allow_step_types:
            logger.info(f'UPDATE step {ind}')
            logger.info(f'UPDATE {steps[ind]}')
            steps[ind].update()
        else:
            logger.warning(f'SKIP UPDATE hstep={steps[ind].id} position={steps[ind].position}')
        return

    for step_id, step in zip(step_ids, steps):
        step.id = step_id
        if step.step_type & allow_step_types:
            logger.info(f'UPDATE {step_id}')
            logger.debug(f'UPDATE {step}')
            step.update()
        else:
            logger.warning(f'SKIP UPDATE hstep={step.id} position={step.position}')

    # create (add) new steps if needed
    if len_site < len_data:
        for step in steps[len_site:]:
            if step.step_type & allow_step_types:
                step.create()
                logger.info(f'CREATE {step}')
            else:
                logger.warning(f'SKIP CREATE step={step.id} position={step.position}')

    # delete obligatory steps if needed
    elif len_site > len_data:
        for step_id in step_ids[len_data:]:
            if step.step_type & allow_step_types:
                logger.info(f'DELETE {step_id}')
                Step.delete_by_id(step_id)
            else:
                logger.warning(f'SKIP DELETE step={step.id} position={step.position}')
            

def print_to_html_file(md_filename, steps, allow_step_types=StepType.FULL):
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
    
    with open(filename, 'w', encoding='utf-8') as fout:
        fout.write('<meta charset="utf-8">')
        for sti, st in enumerate(steps):
            if st.step_type & allow_step_types:
                # fout.write(st.text)
                print(f'SAVE HTML step={st.id} position={st.position}')
                fout.write(st.html(sti+1))
            else:
                print(f'SKIP HTML step={st.id} position={st.position}')


def setup_logger(loglevel):
    """
    Use own logger for logging into out.log file and console(?)
    """
    global logger
    print(f"Setup LOG LEVEL {loglevel}")
    if logger is not None:
        logger.setLevel(loglevel)
        return
    logger = logging.getLogger('deploy_scripts')
    logger.setLevel(loglevel)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('out.log', mode='w', encoding='utf-8',)
    fh.setLevel(loglevel)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)

    # create formatter and add it to the handlers
    # formatter =
    # logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter(u'%(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def main():
    """Read input file, split into steps, upload to site"""
    import argparse

    parser = argparse.ArgumentParser(description='Deploy markdown file into site or convert to html for manual deploying')
    parser.add_argument('markdown_filename', metavar='FILE', type=str, help='input markdown file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--full', action="store_true", help='deploy all steps')
    group.add_argument('-t', '--text', action="store_true", help='deploy only text steps')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='deploy all steps in the first one to debug formatting')
    parser.add_argument('--html', action='store_true', help='deploy all steps into 1 HTML file, not to site')

    parser.add_argument('-s', '--step', type=int, default=0,
                        help='update only the step N, start N from 1, negative numbers are allowed too')
    parser.add_argument('-c', '--config', type=str, default=None, help='deploy with config file')

    args = parser.parse_args()

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    setup_logger(loglevel)

    logger.info(f'FILE = {args.markdown_filename}')
    if args.html:
        logger.info('--html')
        
    if args.full:
        logger.info('deploy full')
        deployed_step_types = StepType.FULL
    elif args.text:
        logger.info('deploy TEXT only')
        deployed_step_types = StepType.TEXT
    else:
        logger.info('deploy all by default')
        deployed_step_types = StepType.FULL

    read_params(args.config)

    with open(args.markdown_filename, encoding='utf-8') as fin:
        # First step - all other steps as one page if mode = DEBUG
        str_list = param_substitude(list(fin))
        steps, lesson_header, lesson_id, lesson_text = parse_lesson(str_list, args.debug)

    # only convert to html, no deploy to site
    if args.html:
        print_to_html_file(args.markdown_filename, steps, allow_step_types=deployed_step_types)
    else:
        deploy_to_stepik(steps, lesson_id, st_num=args.step, allow_step_types=deployed_step_types)


if __name__ == '__main__':
    main()
