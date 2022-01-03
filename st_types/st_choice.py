import logging
from enum import Enum
from pyparsing import ZeroOrMore, OneOrMore, Char, alphas

from md_utils import html
from st_types.st_basic import Step, StepType
from parse import WRD, bool_check

logger = logging.getLogger('deploy_scripts')


class StepMultipleChoice(Step):
    DATA_TEMPLATE = {
        'stepSource': {
            'block': {
                'name': 'choice',
                'text': 'Pick one!',  # question text in html
                'source': {
                    'options': [],  # add answer variants here, use option_template
                    'is_always_correct': False,
                    'is_html_enabled': True,
                    'sample_size': 0,  # len of 'options' list
                    'is_multiple_choice': False,
                    'preserve_order': False,
                    'is_options_feedback': False    # https://github.com/StepicOrg/Stepik-API/issues/67
                }
            },
            'lesson': None,
            'position': None,
            'cost': Step.Cost.DEFAULT
        }
    }
    OPTION_TEMPLATE = {'is_correct': False, 'text': '2+2=3', 'feedback': ''}

    def __init__(self):
        super().__init__()
        self.is_multiple_choice = False
        self.preserve_order = False
        self.options = []
        self.name = 'choice'
        self.step_type = StepType.QUESTION

    def add_option(self, variant_md):
        """
        Add 1 answer variant; correct=False by default
        :param variant_md: - 1 answer variant without leading A) in markdown format
        """
        op = dict(StepMultipleChoice.OPTION_TEMPLATE)
        op['text'] = html(variant_md)
        self.options.append(op)

    def dict(self):
        d = super().dict()
        d['stepSource']['block']['source']['options'] = self.options
        d['stepSource']['block']['source']['sample_size'] = len(self.options)
        d['stepSource']['block']['source']['is_multiple_choice'] = self.is_multiple_choice
        d['stepSource']['block']['source']['preserve_order'] = self.preserve_order
        return d

    def html(self, position=None):
        if position is None:
            position = ''
        else:
            position = str(position)
        HTML = '''
<h2>QUESTION {}</h2>
{question}
{answers}
CORRECT = {corrects}
'''
        question = self.text
        answers = '\n'.join([letter+')\n'+o['text'] for letter, o
                             in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', self.options)])
        corrects = ' '.join([letter for letter, o
                             in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', self.options) if o['is_correct']])
        return HTML.format(position, question=question, answers=answers, corrects=corrects)

    @staticmethod
    def from_aiken(md_lines):
        st = StepMultipleChoice()

        WRDs = ZeroOrMore(WRD)

        opt_template = Char(alphas) + (Char(')') ^ Char('.')) + WRDs
        ans_template = 'ANSWER:' + OneOrMore(Char(alphas) + Char(',')[0, 1])

        class Status(Enum):
            QUESTION = 0
            VARIANT = 1
            ANSWER = 3

        letter_seq = []  # letter sequence from aiken variant, A, B, C, D, etc
        md_part = []
        status = Status.QUESTION
        for line in md_lines:
            # Is it SHUFFLE option?
            """if line.startswith('SHUFFLE:'):
                sh = ('SHUFFLE:' + WRD).parseString(line)

                if sh[1].lower() == 'true':
                    st.preserve_order = False
                elif sh[1].lower() == 'false':
                    st.preserve_order = True
                else:
                    logger.warning(f'Unknown value SHUFFLE: [{sh[1]}]')
                continue"""

            if line.startswith('SHUFFLE:'):
                st.preserve_order = not bool_check('SHUFFLE', line)  # единсвенная проблема в том, что при неправильном написании true или false будет автоматом ставиться true
                continue

            # variant begin by A) or A.
            if line == opt_template:
                opt = opt_template.parseString(line)

                letter = opt[0]
                txt = ' '.join(opt[2:])

                if status == Status.QUESTION:
                    # first answer begin, question end
                    status = Status.VARIANT
                    st.text = html(md_part)
                elif status == Status.VARIANT:
                    # next variant, commit previous variant
                    st.add_option(md_part)
                md_part = [txt]
                letter_seq.append(letter)
            elif line == ans_template and status == Status.VARIANT:
                # end of question
                st.add_option(md_part)

                ans = ans_template.parseString(line)
                ans_str = " ".join(ans[1:])

                logger.debug(f'group1 = {ans_str}')
                letters = [s.strip() for s in ans_str.split(',')]
                logger.debug(f'letters={letters}')
                st.is_multiple_choice = len(letters) > 1
                for letter in letters:
                    ind = letter_seq.index(letter)
                    st.options[ind]['is_correct'] = True
                return st
            else:
                # continue a question or answer
                md_part.append(line)
