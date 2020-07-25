import json
import logging
from md_utils import html
from pyparsing import Word, alphas

import stepik as api


logger = logging.getLogger('deploy_scripts')


class StepType:
    TEXT = 1
    QUESTION = 2
    PROBLEM = 4
    VIDEO = 8
    NUMBER = 16
    STRING = 32
    SKIP = 0
    FULL = TEXT | QUESTION | PROBLEM | VIDEO | NUMBER | STRING


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
        self.id = 0  # step_id, use in update and delete, filled by create method
        self.name = 'text'  # todo: various types (text, question, video, task)
        self.lesson_id = 0  # todo: lesson_id, should be filled, need for create and update requests
        self.position = 0  # step position in lesson, from 1
        self.text = ''
        self.step_type = StepType.TEXT

    def __repr__(self):
        return repr(self.dict())

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def html(self, position=None):
        """ Call if convert steps into HTML file"""
        if position is None:
            position = ''
        else:
            position = str(position)

        HTML = '''
<h2>TEXT {}</h2>
{text}
'''
        text = ''.join(self.text)

        return HTML.format(position, text=text)

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
        logger.debug('=======================')
        self.id = src['id']
        self.lesson_id = src['lesson']
        self.position = src['position']
        self.text = src['block']['text']
        logger.debug('-----------------------')
        logger.debug(self)

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
            logger.error('Expected step header format "## [QUIZ] text"')
            logger.error(f"now: {lines[0]}")
            return None

        if stype == 'QUIZ':
            st = StepMultipleChoice.from_aiken(lines[1:])
        elif stype == 'NUMBER':
            st = StepNumber.num_from_md(lines[1:])
        else:  # Text
            st = Step()
            st.text = html(lines)
        return st

    @staticmethod
    def get(step_id):
        """create Step using GET request /api/step-sources/{step_id} """
        json_st = api.fetch_object('step-source', step_id)

        step = Step()
        step.from_json(json_st)
        return step

    def create(self):
        """create step with data using POST request to /api/step-sources"""
        logger.debug(json.dumps(self.dict(), indent=4))
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



def bool_check(param_name, line):
    template = param_name + ':' + Word(alphas)
    if line == template:
        sh = template.parseString(line)

        if sh[1].lower() == 'true':
            return True
        elif sh[1].lower() == 'false':
            return False
        else:
            logger.warning(f'Unknown value' + param_name + ': [{sh[1]}]')
            return False
    else:
        return False
      
kir_letter = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_'
WRD = Word(printables + kir_letter + srange(['а-я_']) + srange(['А-Я_']))
