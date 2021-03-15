import logging
from pyparsing import OneOrMore

from md_utils import html
from st_types.st_basic import Step, StepType, WRD, bool_check

logger = logging.getLogger('deploy_scripts')


class StepFreeResp(Step):
    DATA_TEMPLATE = {
        'stepSource': {
            'block': {
                'name': 'free-answer',
                'text': 'Напишите "степик"',  # task text in html
                "source": {
                    "is_attachments_enabled": True,
                    "is_html_enabled": False,
                    "manual_scoring": False
                },
                'options': []
            },
            'lesson': None,
            'position': None,
            'cost': Step.Cost.DEFAULT_TASK
        }
    }

    def __init__(self):
        super().__init__()
        self.step_type = StepType.FREE_RESP
        self.name = 'free-answer'

    def dict(self):
        d = super().dict()
        d['stepSource']['block']['text'] = self.text
        return d

    def html(self, position=None):
        if position is None:
            position = ''
        else:
            position = str(position)
        HTML = '''
<h2>TASKTEXT {}</h2>
{question}
'''
        return HTML.format(position, question=self.text)


    @staticmethod
    def str_from_md(md_lines):
        st = StepFreeResp()
        st.text = html(md_lines)
        return st
