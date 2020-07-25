import logging
from md_utils import html
from pyparsing import OneOrMore

from st_types.st_basic import Step, StepType, WRD

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
            'position': None
        }
    }

    def __init__(self):
        super().__init__()
        self.pattern = ''
        self.name = 'string'
        self.step_type = StepType.STRING

    def dict(self):
        d = super().dict()
        d['stepSource']['block']['source']['pattern'] = self.pattern
        d['stepSource']['block']['text'] = self.text
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

    @staticmethod
    def str_from_md(md_lines):
        st = StepString()
        md_part = []

        WRDs = OneOrMore(WRD)
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
                md_part.append(line)

        return st




"""
        for line in md_lines:
            m = re.match(r"\s*PATTERN[:]\s*(.*)\s*", line)
            if m:
                pattern = m.group(1)

                if status == Status.QUESTION:
                    # answer begin, question end
                    status = Status.ANSWER
                    st.text = html(md_part)
                    st.pattern = pattern
                elif status == Status.ANSWER:
                    st.pattern = pattern
            elif status == Status.ANSWER:
                # end of question
                return st
            else:
                # continue a question or answer
                md_part.append(line)

        return st
"""


"""
    def str_from_md(md_lines):
        st = StepString()

        class Status(Enum):
            QUESTION = 0
            FLAGS = 1
            ANSWER = 2

        md_part = []
        status = Status.QUESTION

        for line in md_lines:
            # Is it SHUFFLE option?
            m = re.match(r'FLAGS:\s*(SUBSTR)?\s*(CASE)?\s*', line)
            if m:
                if m.group(1) is not None:
                    st.DATA_TEMPLATE['stepSource']['block']['source']['match_substring'] = True
                elif m.group(2) is not None:
                    st.DATA_TEMPLATE['stepSource']['block']['source']['case_sensitive'] = True
                continue
            else:
                mp = re.match(r'FLAGS:\s*(.*)\s*', line)
                if mp and status == Status.VARIANT:
                    # end of question
                    st.add_option(md_part)
                    logger.debug(f'group1 = {m_answer.group(1)}')
                    letters = [s.strip() for s in m_answer.group(1).split(',')]
                    logger.debug(f'letters={letters}')
                    st.is_multiple_choice = len(letters) > 1
                    for letter in letters:
                        ind = letter_seq.index(letter)
                        st.options[ind]['is_correct'] = True
                    return st
                else:
                    # continue a question or answer
                    md_part.append(line)

            else:
                m_answer = re.match(r'\s*ANSWER[:]*\s*([A-Z, ]+)\s*', line)
                if m_answer and status == Status.VARIANT:
                    # end of question
                    st.add_option(md_part)
                    logger.debug(f'group1 = {m_answer.group(1)}')
                    letters = [s.strip() for s in m_answer.group(1).split(',')]
                    logger.debug(f'letters={letters}')
                    st.is_multiple_choice = len(letters) > 1
                    for letter in letters:
                        ind = letter_seq.index(letter)
                        st.options[ind]['is_correct'] = True
                    return st
                else:
                    # continue a question or answer
                    md_part.append(line)

        return st"""