import json
import re
from enum import Enum

import stepik as api
from md_utils import html

from st_types.st_basic import Step, StepType

from pprint import pprint, pformat

import logging
logger = logging.getLogger('deploy_scripts')


class StepNumber(Step):
    DATA_TEMPLATE = {
        'stepSource': {
            'block': {
                'name': 'number',
                'text': 'Enter the answer',  # task text in html
                'source': {
                    'options': [],  # add answer variants here, use option_template
                    'sample_size': 0,  # len of 'options' list
                    'is_options_feedback': False
                }
            },
            'lesson': None,
            'position': None
        }
    }

    OPTION_TEMPLATE = {'answer': '4', 'max_error': '0'}

    def __init__(self):
        super().__init__()
        self.options = []
        self.name = 'number'
        self.step_type = StepType.PROBLEM

    def add_answer(self, exp, var):
        op = dict(StepNumber.OPTION_TEMPLATE)
        op['answer'] = str(exp)
        op['max_error'] = str(var)
        self.options.append(op)

    def dict(self):
        d = super().dict()
        d['stepSource']['block']['source']['options'] = self.options
        d['stepSource']['block']['source']['sample_size'] = len(self.options)
        return d

    def html(self, position=None):
        if position is None:
            position = ''
        else:
            position = str(position)
        HTML = '''
<h2>PROBLEM {}</h2>
{question}
{answers} 
'''
        question = self.text
        answers = '\n'.join(
            [f'{num+1}) {opt}' for num, opt in enumerate(self.options)])

        return HTML.format(position, question=question, answers=answers)

    @staticmethod
    def num_from_md(md_lines):
        st = StepNumber()

        class Status(Enum):
            QUESTION = 0
            ANSWER = 1

        md_part = []
        status = Status.QUESTION

        for line in md_lines:
            m = re.match(r"\s*ANSWER[:]*\s*(\d+)\s*\+?-?\s*(\d*)\s*", line)
            if m:
                exp = int(m.group(1))
                var = int(m.group(2)) if m.group(2) != '' else 0

                if status == Status.QUESTION:
                    # first answer begin, question end
                    status = Status.ANSWER
                    st.text = html(md_part)
                    st.add_answer(exp, var)
                elif status == Status.ANSWER:
                    # next variant, commit previous variant
                    st.add_answer(exp, var)
            else:
                m_answer = re.match(r'\s*END\s*', line)
                if m_answer and status == Status.ANSWER:
                    # end of question
                    return st
                else:
                    # continue a question or answer
                    md_part.append(line)

        return st
