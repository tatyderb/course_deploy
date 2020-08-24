from md_utils import html

from st_types.st_basic import Step, StepType
from st_types.st_number import StepNumber
from st_types.st_choice import StepMultipleChoice
from st_types.st_string import StepString
from st_types.st_task import StepTask


import logging
logger = logging.getLogger('deploy_scripts')

# token got from stepik.py

# POST and PUT requests for updata and create step with /api/step-sources/{step_id}


def from_lines(lines, task_root=None, task_lang=None):
    """Create Step object from lines of markdown text, first line has
    ## [QUIZ] text
    return Step object
    """
    lines[0] = lines[0].strip()
    # ## text | ## long text | ## QUIZ text
    h2, stype, *a = lines[0].split()
    if h2 != '##':
        logger.error('Expected step header format "## [QUIZ] text"')
        logger.error(f"now: {lines[0]}")
        return None

    if stype == 'QUIZ':
        st = StepMultipleChoice.from_aiken(lines[1:])
    elif stype == 'NUMBER':
        st = StepNumber.num_from_md(lines[1:])
    elif stype == 'STRING':
        st = StepString.str_from_md(lines[1:])
    elif stype == 'TASK':
        st = StepTask.task_from_md(lines[1:], task_root, task_lang)
    else:  # Text
        st = Step()
        st.text = html(lines)
    return st
