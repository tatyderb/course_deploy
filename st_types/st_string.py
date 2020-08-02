import logging
from pyparsing import OneOrMore

from md_utils import html
from st_types.st_basic import Step, StepType, WRD, bool_check, COST_DEFAULT

logger = logging.getLogger('deploy_scripts')


class StepString(Step):
    DATA_TEMPLATE = {
        'stepSource': {
            'block': {
                'name': 'string',
                'text': 'Напишите "степик"',  # task text in html
                'source': {
                    'pattern': 'степик',  # answer
                    'code': '',

                    'match_substring': False,
                    'case_sensitive': False,
                    'use_re': False,

                    'is_file_disabled': True,
                    'is_text_disabled': False,
                },
                'options': [],
                'sample_size': 0,  # len of 'options' list
                'is_options_feedback': False
            },
            'lesson': None,
            'position': None,
            'cost': COST_DEFAULT
        }
    }

    def __init__(self):
        super().__init__()
        self.step_type = StepType.STRING
        self.name = 'string'
        self.pattern = ''

        self.match_substring = False
        self.case_sensitive = False
        self.use_re = False

    def dict(self):
        d = super().dict()
        d['stepSource']['block']['source']['pattern'] = self.pattern
        d['stepSource']['block']['text'] = self.text

        d['stepSource']['block']['source']['match_substring'] = self.match_substring
        d['stepSource']['block']['source']['case_sensitive'] = self.case_sensitive
        d['stepSource']['block']['source']['use_re'] = self.use_re
        return d

    def html(self, position=None):
        if position is None:
            position = ''
        else:
            position = str(position)
        HTML = '''
<h2>STRING {}</h2>
{question}
ANSWER: {pattern} 
'''
        return HTML.format(position, question=self.text, pattern=self.pattern)

    """@staticmethod
    def bool_check(param_name, line):
        if line.startswith(param_name + ':'):
            sh = (param_name + ':' + Word(alphas)).parseString(line)

            if sh[1].lower() == 'true':
                return True
            elif sh[1].lower() == 'false':
                return False
            else:
                logger.warning(f'Unknown value' + param_name + ': [{sh[1]}]')
                return False"""

    @staticmethod
    def str_from_md(md_lines):
        st = StepString()
        md_part = []

        WRDs = OneOrMore(WRD)
        ans_template = 'ANSWER:' + WRDs

        for line in md_lines:
            ans = None

            if line.startswith('SUBSTR:'):
                st.match_substring = bool_check('SUBSTR', line)
                continue

            if line.startswith('CASESENSE:'):
                st.case_sensitive = bool_check('CASESENSE', line)
                continue

            if line.startswith('USE_RE:'):
                st.use_re = bool_check('USE_RE', line)
                continue

            if line.startswith('ANSWER:'):
                ans = ans_template.parseString(line)
                st.pattern = ' '.join(ans[1:])

            if ans is not None:
                st.text = html(md_part)
                return st
            else:
                # continue a question or answer
                md_part.append(line)

        return st
