from pyparsing import Word, OneOrMore, Char, nums
from pathlib import Path
import logging

from st_types.st_basic import Step, StepType, WRD, COST_DEFAULT_TASK


logger = logging.getLogger('deploy_scripts')


class StepTask(Step):
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
                                    'test_cases': []
                                },
                            'text': '',
                            'video': None
                        },
                    'cost': COST_DEFAULT_TASK,
                    'lesson': None,
                    'position': None
                }
        }

    default_code = ('# This is a sample Code Challenge\n'
                    '# Learn more: https://stepik.org/lesson/9173\n'
                    '# Ask your questions via support@stepik.org\n\n'
                    'def generate():\n'
                    '    return []\n\n'
                    'def check(reply, clue):\n'
                    '    return reply.strip() == clue.strip()\n\n'
                    '# def solve(dataset):\n'
                    '#     a, b = dataset.split()\n'
                    '#     return str(int(a) + int(b))')

    default_text = ('<p>Текст по умолчанию.</p>\n'
                    '<p>Напишите программу для сложения чисел<br>\n'
                    'Вы можете изменить условие задания в этом поле и указать настройки ниже.</p>')

    default_test = ['8 11\n', '19\n']

    def __init__(self):
        super().__init__()
        self.cost = COST_DEFAULT_TASK
        self.text = ''
        self.code = ''
        self.name = 'code'
        self.test_cases = []

        self.params = {
            'name': None,
            'repo': None,
            'statement': None,
            'checker': None,
            'solution': None,
            'tests': None,
            'score': None
        }

        self.step_type = StepType.TASK

    def dict(self):
        d = super().dict()

        d['stepSource']['cost'] = self.cost
        d['stepSource']['block']['text'] = self.text
        d['stepSource']['block']['source']['code'] = self.code
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
cost: {cost}<br>
TESTS:
{tests}
CODE:
{code}
'''
        tests = '\n'.join(['<br>{})\n<p> in: {}</p> \n<p>out: {}</p>'.format(str(num + 1), tst[0], tst[1])
                           for num, tst in enumerate(self.test_cases)])

        code = '<pre><code>{}</code></pre>'.format(self.code) if self.code != '' \
            else '<pre><code>{}</code></pre>'.format(StepTask.default_code)

        question = self.text if self.text != '' else StepTask.default_text

        return HTML.format(position, question=question, cost=self.cost, tests=tests, code=code)

    def add_sample(self, str_in, str_out):
        sample = [str_in, str_out]
        self.test_cases.append(sample)

    def params_check_and_fill(self):
        is_OK = True

        if self.params['repo'] is None:
            logger.error("'repo' param wasn't entered")
            logger.error('program end...')
            is_OK = False
            exit(1)
        elif not Path(self.params['repo']).exists():
            logger.error(f"'repo' wrong way: {self.params['repo']}")
            logger.error('program end...')
            is_OK = False
            exit(1)
        else:
            repo = Path(self.params['repo'])
            logger.debug('REPO OK')

        if self.params['statement'] is None:
            state_name = repo.name + '.xml'
            state_path = repo / state_name

            if not state_path.exists():
                logger.warning(f"statement file doesn't exist: {state_path}")
                logger.warning(f'default statement will be set')
                self.params['statement'] = None
            else:
                self.params['statement'] = state_name
                logger.info('STATEMENT OK')
        else:
            state_path = repo / self.params['statement']

            if not state_path.exists():
                logger.warning(f"statement file doesn't exist: {state_path}")
                logger.warning(f'default statement will be set')
                self.params['statement'] = None
            else:
                logger.info('STATEMENT OK')

        # todo: name
        # todo: checker
        # todo: solution

        if self.params['tests'] is None:
            tst_path = repo / 'tests'

            if not tst_path.exists():
                logger.warning(f"tests directory doesn't exist: {tst_path}")

                if self.params['statement'] is None:  # потом тут еще проверка code будет
                    logger.warning(f'default tests will be set')
                    self.params['tests'] = None
                else:
                    is_OK = False
                    logger.error('program end...')
                    exit(1)
            else:
                self.params['tests'] = 'tests'
                logger.debug('TESTS DIR OK')
        elif not ((repo) / self.params['tests']).exists():
            logger.warning(f"tests directory doesn't exist: {(repo) / self.params['tests']}")

            if self.params['statement'] is None:  # потом тут еще проверка code будет
                logger.warning(f'default tests will be set')
                self.params['tests'] = None
            else:
                logger.error('program end...')
                is_OK = False
                exit(1)
        else:
            logger.info('TESTS OK')

        if self.params['score'] is None:
            self.params['score'] = COST_DEFAULT_TASK
            logger.info(f'default tests will be set')
            logger.info('SCORE OK')
        else:
            logger.info('SCORE OK')

        return is_OK

    def set_attrs(self):
        is_OK = self.params_check_and_fill()

        if not is_OK:
            logger.warning('Task params are wrong')
            logger.error('program end...')
            exit(1)

        repo = self.params['repo']
        statement = self.params['statement']

        if self.params['statement'] is None and self.params['tests'] is None:
            self.text = StepTask.default_text
            self.test_cases.append(StepTask.default_test)
        elif self.params['statement'] is None:
            self.text = StepTask.default_text
            self.make_test_list()
        else:
            self.text = (repo / statement).read_text()
            self.make_test_list()

        self.code = StepTask.default_code
        self.cost = self.params['score']

    def make_test_list(self):
        repo = self.params['repo']
        tst_dir = self.params['tests']

        tests = Path(repo) / tst_dir

        for data in Path(tests).glob('*.dat'):
            ans = Path(tests) / (data.stem + '.ans')
            if not ans.exists():
                logger.warning(f'Where is answer {data.stem}??')
            else:
                self.add_sample(data.read_text(), ans.read_text())

    @staticmethod
    def task_from_md(md_lines):
        st = StepTask()

        WRDs = OneOrMore(WRD)
        equality = Char('=') + WRDs

        name_template = 'name' + equality
        repo_template = 'repo' + equality
        statement_template = 'statement' + equality
        checker_template = 'checker' + equality
        solution_template = 'solution' + equality
        tests_template = 'tests' + equality
        score_template = 'score' + Char('=') + Word(nums)

        for line in md_lines:
            # print(line)

            if line == repo_template:
                repo = repo_template.parseString(line)[2]
                st.params['repo'] = Path(repo)
            elif line == score_template:
                score = score_template.parseString(line)[2]
                st.params['score'] = int(score)

            elif line == statement_template:
                statement = statement_template.parseString(line)[2]
                st.params['statement'] = statement
            elif line == name_template:
                name = name_template.parseString(line)[2]
                st.params['name'] = name
            elif line == checker_template:
                checker = checker_template.parseString(line)[2]
                st.params['checker'] = checker
            elif line == solution_template:
                solution = solution_template.parseString(line)[2]
                st.params['solution'] = solution
            elif line == tests_template:
                tests = tests_template.parseString(line)[2]
                st.params['tests'] = tests

        st.set_attrs()

        return st
