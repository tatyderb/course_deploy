import logging
from pyparsing import Combine, Word, nums

from st_types.st_basic import Step, StepType
from md_utils import html

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
            'position': None,
            'cost': Step.Cost.DEFAULT
        }
    }

    OPTION_TEMPLATE = {'answer': '4', 'max_error': '0'}

    def __init__(self):
        super().__init__()
        self.options = []
        self.name = 'number'
        self.step_type = StepType.NUMBER

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
<h2>NUMBER {}</h2>
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
        md_part = []

        real = Combine(Word(nums) + '.' + Word(nums))
        integer = Word(nums)
        num = real ^ integer
        ans_template = 'ANSWER:' + num + ('+-' + num)[0, 1]

        for line in md_lines:
            ans = None

            if line.startswith('ANSWER:') and '+-' in line:
                ans = ans_template.parseString(line)
                exp = float(ans[1])
                var = float(ans[3])
            elif line.startswith('ANSWER:'):
                ans = ans_template.parseString(line)
                exp = float(ans[1])
                var = 0

            if ans:
                st.text = html(md_part)
                st.add_answer(exp, var)
            else:
                # continue a question or answer
                md_part.append(line)

        return st
