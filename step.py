import json
import re
from enum import Enum

import stepik as api
from md_utils import html

from pprint import pprint, pformat


# token got from stepik.py

# POST and PUT requests for updata and create step with /api/step-sources/{step_id}

class StepType:
    TEXT = 1
    QUESTION = 2
    PROBLEM = 4
    VIDEO = 8
    SKIP = 0
    FULL = TEXT | QUESTION | PROBLEM | VIDEO


class Step:
    """ 1 step in stepik.org """
    DATA_TEMPLATE = {
        'stepSource': {
            'block': {
                'name': 'text',
                'text': 'new text'  # set new text as html
            },
            'lesson': 0,  # set lesson_id - нет в get
            'position': 1  # set step position in lesson, start with 1.
        }
    }

    def __init__(self):
        """ Dummy step """
        self.id = 0         # step_id, use in update and delete, filled by create method
        self.name = 'text'  # todo: various types (text, question, video, task
        self.lesson_id = 0  # todo: lesson_id, should be filled, need for create and update requests
        self.position = 0   # step position in lesson, from 1
        self.text = ''
        self.step_type = StepType.TEXT

    def __repr__(self):
        return repr(self.dict())

    def __str__(self):
        # return pformat(self.dict())
        return str(self.dict())

    def html(self):
        """ Call if convert step into HTML file"""
        return self.text

    def dict(self):
        """ convert Step() to dictionary for PUT or POST request"""
        d = dict(self.__class__.DATA_TEMPLATE)  # to get template for child classes if needed
        src = d['stepSource']
        src['lesson'] = self.lesson_id
        src['position'] = self.position
        src['block']['text'] = self.text
        src['block']['name'] = self.name
        return d

    def from_json(self, src):
        """ Set attributes from GET json"""
        print('=======================')
        # pprint(src)
        self.id = src['id']
        self.lesson_id = src['lesson']
        self.position = src['position']
        self.text = src['block']['text']
        print('-----------------------')
        print(self)

    @staticmethod
    def from_lines(lines):
        """Create Step object from lines of markdown text, first line has
        ## [QUIZ] text
        return Step object
        """
        lines[0] = lines[0].strip()
        # ## text | ## long text | ## QUIZ text
        h2, stype, *a = lines[0].split()
        if h2 != '##':
            print('Expected step header format "## [QUIZ] text"')
            print(f"now: {lines[0]}")
            return None

        if stype == 'QUIZ':
            st = StepMultipleChoice.from_aiken(lines[1:])
        else:  # Text
            st = Step()
            st.text = html(lines)
        return st

    @staticmethod
    def get(step_id):
        """create Step using GET request /api/step-sources/{step_id} """
        json = api.fetch_object('step-source', step_id)

        step = Step()
        step.from_json(json)
        return step

    def create(self):
        """create step with data using POST request to /api/step-sources"""
        print(json.dumps(self.dict(), indent=4))
        self.id = api.create_object('step-sources', self.dict())
        return self.id

    @staticmethod
    def get_step_ids_for_lesson(lesson_id):
        """return list of step_id for lesson_id by GET request to """
        return [step for lesson in api.fetch_objects('lesson', [lesson_id]) for step in lesson['steps']]

    def update(self, text=None):
        """ update text in the step"""
        self.text = text or self.text
        api.update_object('step-sources', self.id, self.dict())

    @staticmethod
    def delete_by_id(step_id):
        """delete step by DELETE request """
        api.delete_object('step-sources', step_id)

    def delete(self):
        Step.delete_by_id(self.id)
        return self.id

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.dict() == other
        return self.dict() == other.dict()


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
                    'is_options_feedback': False  # https://github.com/StepicOrg/Stepik-API/issues/67
                }
            },
            'lesson': None,
            'position': None
        }
    }
    OPTION_TEMPLATE = {'is_correct': False, 'text': '2+2=3', 'feedback': ''}

    def __init__(self):
        super().__init__()
        self.is_multiple_choice = False
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
        answers = '\n'.join([letter + ')\n' + o['text'] for letter, o in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', self.options)])
        corrects = ' '.join([letter for letter, o in zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', self.options) if o['is_correct']])
        return HTML.format(position, question=question, answers=answers, corrects=corrects)

    @staticmethod
    def from_aiken(md_lines):
        st = StepMultipleChoice()

        class Status(Enum):
            QUESTION = 0
            VARIANT = 1
            ANSWER = 3

        letter_seq = []  # letter sequence from aiken variant, A, B, C, D, etc
        md_part = []
        status = Status.QUESTION
        for line in md_lines:

            # variant begin by A) or A.
            m = re.match(r'(\s*)([A-Z])([.)])(.*)', line)
            if m:
                letter = m.group(2)
                sep = m.group(3)
                txt = m.group(4) + '\n'

                if status == Status.QUESTION:
                    # first answer begin, question end
                    status = Status.VARIANT
                    st.text = html(md_part)
                elif status == Status.VARIANT:
                    # next variant, commit previous variant
                    st.add_option(md_part)
                md_part = [txt]
                letter_seq.append(letter)
            else:
                m_answer = re.match(r'\s*ANSWER[:]*\s*([A-Z])\s*', line)
                if m_answer and status == Status.VARIANT:
                    # end of question
                    st.add_option(md_part)

                    letter = m_answer.group(1)
                    ind = letter_seq.index(letter)
                    st.options[ind]['is_correct'] = True
                    return st
                else:
                    # continue a question or answer
                    md_part.append(line)


class StepNumber(Step):
    DATA_TEMPLATE = {
        'stepSource': {
            'block': {
                'name': 'number',
                'text': 'What is 2 + 2 ?\n',
                'source': {
                    'options': [],
                    'sample_size': 0,
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







'''
put_step_dict = {
	"stepSource": {
		"lesson_id": 239930,                        # set lesson_id - нет в get
		"lesson": 239930,                           # set lesson_id
		"position": 1,                              # set step position in lesson, start with 1.
		"status": "ready",

		"block": {
			"name": "text",
			"text": "<p>Text of step</p>",          # set new text as html
			"video": None,
			"animation": None,
			"options": {},
			"subtitle_files": [],
			"source": {},
			"subtitles": {},
			"tests_archive": None,
			"feedback_correct": "",
			"feedback_wrong": ""
		},

		"actions": {},

		"instruction": None,
		"instruction_type": None,
		"instruction_id": None,                     # нет в get
		"has_instruction": False,                   # нет в get

		"is_solutions_unlocked": False,
		"solutions_unlocked_attempts": 3,
		"max_submissions_count": 3,
		"has_submissions_restrictions": False,

		"create_date": "2019-06-26T05:01:47Z",      # set create date

		"reason_of_failure": "",
		"error": {
			"text": "",
			"code": "",
			"params": {}
		},
		"warnings": [],
		"cost": 0,
	}
}
'''

'''
get_step_dict = {
  "meta": {
    "page": 1,
    "has_next": false,
    "has_previous": false
  },
  "step-sources": [
    {
      "id": 761415,                         # lesson_id в get dict
      "lesson": 239930,
      "position": 1,
      "status": "ready",
      "block": {
        "name": "text",
        "text": "<p>Урок 239930 шаг 1 (761415)</p>",
        "video": null,
        "animation": null,
        "options": {},
        "subtitle_files": [],
        "source": {},
        "subtitles": {},
        "tests_archive": null,
        "feedback_correct": "",
        "feedback_wrong": ""
      },
      "actions": {},
      "progress": "77-761415",      # нет в put
      "subscriptions": [            # нет в put
        "31-77-761415",
        "30-77-761415"
      ],
      "instruction": null,
      "session": null,
      "instruction_type": null,
      "viewed_by": 1,               # нет в put
      "passed_by": 1,               # нет в put
      "correct_ratio": null,        # нет в put
      "worth": 0,                   # нет в put

      "is_solutions_unlocked": false,
      "solutions_unlocked_attempts": 3,
      "max_submissions_count": 3,
      "has_submissions_restrictions": false,

      "create_date": "2019-06-26T05:01:47Z",
      "update_date": "2019-07-09T14:09:28Z",

      "variation": 1,
      "variations_count": 1,
      "discussions_count": 0,
      "discussion_proxy": "77-761415-1",
      "discussion_threads": [
        "77-761415-1"
      ],

      "reason_of_failure": "",
      "error": {
        "text": "",
        "code": "",
        "params": {}
      },
      "warnings": [],
      "cost": 0
    }
  ]
}
'''
