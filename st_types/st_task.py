from pyparsing import Word, OneOrMore, Char, nums
from pathlib import Path

import logging

from st_types.st_basic import Step, StepType, WRD


logger = logging.getLogger('deploy_scripts')


class StepTask(Step):
    DATA_TEMPLATE = \
        {
            'stepSource':
                {
                    'block':
                        {
                            'name': 'code',
                            'options': {},
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
                                    'samples_count': Step.DEAFAULT_TST_NUM,
                                    'templates_data': '',
                                    'test_archive': [],
                                    'test_cases': []
                                },
                            'text': '',
                            'video': None
                        },
                    'cost': Step.Cost.DEFAULT_TASK,
                    'lesson': None,
                    'position': None
                }
        }

    DEFAULT_CODE = '''
# This is a sample Code Challenge
# Learn more: https://stepik.org/lesson/9173
# Ask your questions via support@stepik.org
def generate():
    return []
def check(reply, clue):
    return reply.strip() == clue.strip()
# def solve(dataset):
#     a, b = dataset.split()
#     return str(int(a) + int(b))
'''
    DEFAULT_CODE_VIEW_ALL_TESTS = '''
# This is a sample Code Challenge
# Learn more: https://stepik.org/lesson/9173
# Ask your questions via support@stepik.org
def generate():
    return []
    
def check(reply, clue):
    reply, clue = int(reply), int(clue)
    if reply == clue:
        return True
    feedback = f"You answer was: {reply}. Correct answer was: {clue}"
    return False, feedback  # feedback will be shown to the learner

# def solve(dataset):
#     a, b = dataset.split()
#     return str(int(a) + int(b))
'''
    default_code = DEFAULT_CODE_VIEW_ALL_TESTS

    DEFAULT_GENERATE = '''
def generate():
    return []
    '''
    DEFAULT_SOLVE = '''
# def solve(dataset):
#     a, b = dataset.split()
#     return str(int(a) + int(b))
    '''

    CHECK_STR = '''
def check(reply, clue):
    if reply == '':
        return False
    return reply.strip() == clue.strip()
    '''

    CHECK_INTSEQ_VIEW_ALL_TESTS = '''
def check(reply, clue):
    if reply == '':
        return False
    reply, clue = int(reply), int(clue)
    if reply == clue:
        return True
    feedback = f"You answer was: {reply}. Correct answer was: {clue}"
    return False, feedback  # feedback will be shown to the learner
    '''    

    CHECK_STR_VIEW_ALL_TESTS = '''
def check(reply, clue):
    #if reply == '':
    #    return False
    #reply, clue = int(reply), int(clue)
    #if reply == clue:
    #    return True
    if reply.strip() == clue.strip():
        return True
    feedback = f"You answer was: {reply}. Correct answer was: {clue}"
    return False, feedback  # feedback will be shown to the learner
    '''    
        
    CHECK_FLOAT = '''
def check(reply, clue):
    if reply == '':
        return False
    return abs(float(reply) - float(clue)) < {eps}
    ''' # expected argument eps
    
    #DEFAULT_CHECKER = CHECK_STR_VIEW_ALL_TESTS
    DEFAULT_CHECKER = CHECK_STR_VIEW_ALL_TESTS

    default_text = ('<p>Текст по умолчанию.</p>\n'
                    '<p>Напишите программу для сложения чисел<br>\n'
                    'Вы можете изменить условие задания в этом поле и указать настройки ниже.</p>')

    default_test = ['8 11\n', '19\n']

    Root = Path('examples')

    def __init__(self):
        super().__init__()
        self.cost = Step.Cost.DEFAULT_TASK
        self.text = ''
        self.code = ''
        self.name = 'code'
        self.test_cases = []
        self.samples_count = Step.DEAFAULT_TST_NUM
        self.header = ''
        self.footer = ''
        self.lang = None

        self.generate = ''
        self.checker = ''
        self.solve = ''

        self.params = {
            'name': None,
            'repo': None,
            'statement': None,
            # 'checker': '',
            # 'solution': '',
            # 'generate': '',
            'tests': None,
            'visible_tst_num': None,
            'score': None,
            'lang': None,
            'header': None,
            'footer': None
        }

        self.step_type = StepType.TASK

    def dict(self):
        d = super().dict()

        d['stepSource']['cost'] = self.cost
        d['stepSource']['block']['text'] = self.text
        d['stepSource']['block']['source']['test_cases'] = self.test_cases
        d['stepSource']['block']['source']['samples_count'] = self.samples_count
        
        d['stepSource']['block']['source']['code'] = self.generator_checker_solver()
        d['stepSource']['block']['source']['templates_data'] = self.header_footer()
        d['stepSource']['block']['options']['code_templates'] = self.lang_templates()

        return d

    def generator_checker_solver(self):
        """
        return generator, checker, solver
        """
        generator = self.params.get('generate', StepTask.DEFAULT_GENERATE)
        checker = self.params.get('checker', StepTask.DEFAULT_CHECKER)
        solution = self.params.get('solution', StepTask.DEFAULT_SOLVE)
            
        return '\n'.join([generator, checker, solution])
        
    def lang_templates(self):
        """ 
        return template code in IDE
        """
        return '::{self.lang}\n{self.template}'
        
    def header_footer(self):
        """ 
        return template code in IDE
        "::python3\n::code\n# This is code in lang and templates\n::header\n# This is header\n::footer\n# This is footer\n"
        """
        if not self.lang:
            return ''
        s = f'::{self.lang}\n'
        if self.template:
            s = s + '::code\n' + self.template + '\n'
        if self.header:
            s = s + '::header\n' + self.header + '\n'
        if self.footer:
            s = s + '::footer\n' + self.footer + '\n'
        return s

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
        tests = '\n'.join([f'<br>{str(num + 1)})\n<p> in: {tst[0]}</p> \n<p>out: {tst[1]}</p>'
                           for num, tst in enumerate(self.test_cases)])

        code = f'<pre><code>{self.code}</code></pre>' if self.code != '' \
            else f'<pre><code>{StepTask.default_code}</code></pre>'

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
            logger.debug(f"using repo {self.params['repo']}")
            logger.info('REPO OK')

        if self.params['statement'] is None:
            state_name = repo.name + '.xml'
            state_path = repo / state_name

            if not state_path.exists():
                logger.warning(f"statement file doesn't exist: {state_path}")
                logger.warning(f'default statement will be set')
                self.params['statement'] = None
            else:
                self.params['statement'] = state_name
                logger.debug(f"using statement {self.params['statement']}")
                logger.info('STATEMENT OK')
        else:
            state_path = repo / self.params['statement']

            if not state_path.exists():
                logger.warning(f"statement file doesn't exist: {state_path}")
                logger.warning(f'default statement will be set')
                self.params['statement'] = None
            else:
                logger.debug(f"using statement {self.params['statement']}")
                logger.info('STATEMENT OK')

        # todo: name
        # todo: checker
        # todo: solution

        if self.params['tests'] is None:
            tst_path = repo / 'tests'

            if not tst_path.exists():
                logger.warning(f"tests directory doesn't exist: {tst_path}")

                if self.params['statement'] is None:  # потом тут еще проверка code будет
                    logger.debug("using default tests")
                    logger.info('TESTS OK')
                    self.params['tests'] = None
                else:
                    is_OK = False
                    logger.error('program end...')
                    exit(1)
            else:
                self.params['tests'] = 'tests'
                logger.debug(f"using tests {self.params['tests']}")
                logger.info('TESTS DIR OK')
        elif not ((repo) / self.params['tests']).exists():
            logger.warning(f"tests directory doesn't exist: {(repo) / self.params['tests']}")

            if self.params['statement'] is None:  # потом тут еще проверка code будет
                logger.debug("using default tests")
                logger.info('TESTS OK')
                self.params['tests'] = None
            else:
                logger.error('program end...')
                is_OK = False
                exit(1)
        else:
            logger.debug(f"using tests {self.params['tests']}")
            logger.info('TESTS DIR OK')

        if self.params['score'] is None:
            self.params['score'] = Step.Cost.DEFAULT_TASK
            logger.debug("using default score")
            logger.info('SCORE OK')
        else:
            logger.info('SCORE OK')

        if self.params['visible_tst_num'] is None:
            self.params['visible_tst_num'] = Step.Cost.DEFAULT_TASK
            logger.debug("using default visible tests number")
            logger.info('VISIBLE_TST_NUM OK')
        else:
            logger.info('VISIBLE_TST_NUM OK')

        self.lang = self.params['lang']

        if self.lang is not None:
            if self.params['header'] is not None:
                header_path = repo / self.params['header']
                if header_path.exists():
                    self.header = header_path.read_text()
                else:
                    logger.warning(f"HEADER PATH DOESN'T EXIST: {header_path}")

            if self.params['footer'] is not None:
                footer_path = repo / self.params['footer']
                if footer_path.exists():
                    self.footer = footer_path.read_text()
                else:
                    logger.warning(f"FOOTER PATH DOESN'T EXIST: {footer_path}")
        elif self.params['header'] is not None or self.params['footer'] is not None:
            logger.warning("HEADER/FOOTER WON'T BE INSERTED: YOU HAVE TO SPECIFY TASK LANGUAGE")

        return is_OK

    def set_attrs(self):
        is_OK = self.params_check_and_fill()

        if not is_OK:
            logger.error('Task params are wrong')
            logger.error('program end...')
            exit(1)

        repo = self.params['repo']
        statement = self.params['statement']

        if self.params['statement'] is None:
            self.text = StepTask.default_text
        else:
            logger.debug(f'repo={repo} statement={statement}')
            st = repo / statement
            logger.debug(st)
            xml_text = (repo / statement).read_text(encoding="utf-8")
            s1 = xml_text.find("<description>") + len('<description>')
            s2 = xml_text.find("</description>")
            xml_text = xml_text[s1:s2]
            '''
            description = []
            in_description = False
            for line in xml_text:
                if '</descriprion>' in line:
                    break
                if in_description:
                    description.append(line)
                if '<descriprion>' in line:
                    in_description = True

            self.text = description
            '''
            t = type(xml_text)
            logger.debug(f"type={t} xml={xml_text}")
            self.text = xml_text
        if self.params['tests'] is None:
            self.test_cases.append(StepTask.default_test)
        else:
            self.make_test_list()
        '''
        if self.params['statement'] is None and self.params['tests'] is None:
            self.text = StepTask.default_text
            self.test_cases.append(StepTask.default_test)
        elif self.params['statement'] is None:
            self.text = StepTask.default_text
            self.make_test_list()
        else:
            self.text = (repo / statement).read_text()
            self.make_test_list()
        '''
        # self.code = StepTask.default_code
        self.cost = self.params['score']
        self.samples_count = self.params['visible_tst_num']

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
    def task_from_md(md_lines, root=None, lang=None):
        st = StepTask()

        if root is None:
            root = StepTask.Root
        else:
            root = Path(root)

        if lang is not None:
            st.params['lang'] = lang

        WRDs = OneOrMore(WRD)
        equality = Char('=') + WRDs

        name_template = 'name' + equality
        repo_template = 'repo' + equality
        statement_template = 'statement' + equality
        checker_template = 'checker' + equality
        solution_template = 'solution' + equality
        tests_template = 'tests' + equality
        header_template = 'header' + equality
        footer_template = 'footer' + equality
        score_template = 'score' + Char('=') + Word(nums)
        visible_tst_num_template = 'visible_tst_num' + Char('=') + Word(nums)

        for line in md_lines:
            # print(line)

            if line == repo_template:
                repo = repo_template.parseString(line)[2]
                st.params['repo'] = root / repo
            elif line == score_template:
                score = score_template.parseString(line)[2]
                st.params['score'] = int(score)
            elif line == visible_tst_num_template:
                visible_tst_num = visible_tst_num_template.parseString(line)[2]
                st.params['visible_tst_num'] = int(visible_tst_num)

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
            elif line == header_template:
                header = header_template.parseString(line)[2]
                st.params['header'] = header
            elif line == footer_template:
                footer = footer_template.parseString(line)[2]
                st.params['footer'] = footer

        st.set_attrs()

        return st
