import os.path as op
import json
import re
from pyparsing import Word, printables, ZeroOrMore, srange
from enum import Enum

import stepik as api
from md_utils import html

from st_types.st_basic import Step, StepType, WRD

from pprint import pprint, pformat

import logging

logger = logging.getLogger('deploy_scripts')


class StepTask(Step):
    """DATA_TEMPLATE = \
        {
            'stepSource':
                {
                    'block':
                        {
                            'name': 'code',
                            'text': 'Напишите программу для сложения двух чисел',  # task text in html
                            'source':
                                {
                                    'code': # This is a sample Code Challenge\n
                                    # Learn more: https://stepik.org/lesson/9173\n
                                    # Ask your questions via support@stepik.org\n
                                    \n
                                    def generate():\n
                                        return []\n
                                    \n
                                    def check(reply, clue):\n
                                        return reply.strip() == clue.strip()\n
                                    \n
                                    # def solve(dataset):\n
                                    #     a, b = dataset.split()\n
                                    #     return str(int(a) + int(b))\n,

                                    'execution_memory_limit': 256,
                                    'execution_time_limit': 5,
                                    'is_memory_limit_scaled': True,
                                    'is_run_user_code_allowed': True,
                                    'is_time_limit_scaled': True,
                                    'manual_memory_limits': [],
                                    'manual_time_limits': [],
                                    'samples_count': 1,
                                    'templates_data': '',
                                    'test_archive': [],
                                    'test_cases': [['8 11\n', '19\n']]
                                },
                        },
                    'lesson': None,
                    'position': None
                },
        }"""

    DATA_TEMPLATE = \
        {
            'stepSource':
                {
                    'block':
                        {
                            'name': 'code',
                            'options': None,
                            'source':
                                {
                                    'code': '',
                                    'execution_memory_limit': 256,
                                    'execution_time_limit': 5,
                                    'is_memory_limit_scaled': True,
                                    'is_run_user_code_allowed': True,
                                    'is_time_limit_scaled': True,
                                    'manual_memory_limits': [],
                                    'manual_time_limits': [],
                                    'samples_count': 1,
                                    'templates_data': '',
                                    'test_archive': [],
                                    'test_cases': [['8 11\n', '19\n']]
                                },
                            'text': 'Вы можете изменить условие задания в этом ' +
                                    'поле и указать настройки ниже. <br><br> ' +
                                    'Напишите программу, которая считает сумму ' +
                                    'двух чисел.',
                            'video': None
                        },
                    'cost': 10,
                    'lesson': None,
                    'position': None
                }
        }

    default_code = '# This is a sample Code Challenge\n' + \
                   '# Learn more: https://stepik.org/lesson/9173\n' + \
                   '# Ask your questions via support@stepik.org\n\n' + \
                   'def generate():\n' + \
                   '    return []\n\n' + \
                   'def check(reply, clue):\n' + \
                   '    return reply.strip() == clue.strip()\n\n' + \
                   '# def solve(dataset):\n' + \
                   '#     a, b = dataset.split()\n' + \
                   '#     return str(int(a) + int(b))'

    default_text = '<p>Вы можете изменить условие задания в этом поле и указать настройки ниже. <br><br> ' + \
                   'Напишите программу, которая считает сумму двух чисел.</p>'

    def __init__(self):
        super().__init__()
        self.text = '<p>Напишите программу для сложения двух чисел.</p>'
        self.code = ''
        self.name = 'code'
        self.test_cases = [['8 11\n', '19\n']]
        self.step_type = StepType.TASK

    def dict(self):
        d = super().dict()

        d['stepSource']['block']['text'] = self.text if self.text != '' else StepTask.default_text
        d['stepSource']['block']['source']['code'] = self.code if self.code != '' else StepTask.default_code
        d['stepSource']['block']['source']['test_cases'] = self.test_cases
        d['stepSource']['block']['source']['samples_count'] = len(self.test_cases)
        return d

    def html(self, position=None):
        if position is None:
            position = ''
        else:
            position = str(position)

        HTML = '''
<h2>TASK {}</h2>
{question}
TESTS:
{tests}
CODE:
{code}
'''
        tests = '\n'.join(['<br>' + str(num + 1) + ')\n<p>in: ' + tst[0] + '</p>\n<p>out: ' + tst[1] + '</p>'
                           for num, tst in enumerate(self.test_cases)])

        code = ('<pre><code>' + self.code + '</code></pre>') if self.code != ''\
            else ('<pre><code>' + StepTask.default_code + '</code></pre>')
        question = self.text if self.text != '' else StepTask.default_text

        return HTML.format(position, question=question, tests=tests, code=code)

    def add_sample(self, str_in, str_out):
        sample = [str_in, str_out]
        self.test_cases.append(sample)

    @staticmethod
    def task_from_md(md_lines):
        st = StepTask()
        """md_part = []

        WRDs = ZeroOrMore(WRD)
        ans_template = 'ANSWER:' + WRDs

        for line in md_lines:
            ans = None

            if line.startswith('ANSWER:'):
                ans = ans_template.parseString(line)
                st.pattern = ' '.join(ans[1:])

            if ans is not None:
                st.text = html(md_part)
                return st
            else:
                # continue a question or answer
                md_part.append(line)"""

        return st
