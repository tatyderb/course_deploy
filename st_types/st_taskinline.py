from enum import Enum
import logging

from md_utils import html
from st_types.st_task import StepTask
from parse import parse_config


logger = logging.getLogger('deploy_scripts')


def to_text(lines):
    return '\n'.join(lines)


class InputState(Enum):
    Statement = 1   # условие задачи
    TestIn = 2      # тест, input            
    TestOut = 4     # тест, ожидаемый output
    Header = 8      # присоединяемый код до
    Footer = 16     # присоединяемый код после
    Code = 32       # в редакторе питона студентам уже написан этот код
    Config = 64     # мелкие однострочные параметры: checker, score, etc
    # Template = 64   # этот код


class StepTaskInline(StepTask):
    """ Задача описана непосредственно в md файле 
    и не расположена на внешних ресурсах
    Поля - с первой позиции на отдельной строке:
    TEST - начало тестов, формат как в tests
    HEADER - начало header-файла
    FOOTER - начало footer-файла
    TEMPLATE - начало того, что в окошке кода
    #CODE - начало того, что в окошке кода
    """

    def __init__(self, lang):
        super().__init__(lang)
        self.code = StepTask.default_code
        self.template = None
        
    def __dict__(self):
        d = super().dict()
        return d
    
    @staticmethod
    def task_from_md(md_lines, params):
        st = StepTaskInline(params.get('task_lang'))

        mode = InputState.Statement 
        text = []
        for line in md_lines:
            print(line)
            line = line.rstrip()
            cleanup = True
            if line == 'TEST':
                st.end_state(mode, text)
                mode = InputState.TestIn
            elif line == 'HEADER':
                st.end_state(mode, text)
                mode = InputState.Header
            elif line == 'FOOTER':
                st.end_state(mode, text)
                mode = InputState.Footer
            elif line == 'CODE':
                st.end_state(mode, text)
                mode = InputState.Code
            elif line == 'CONFIG':
                st.end_state(mode, text)
                mode = InputState.Config
            #elif line == 'TEMPLATE':
            #    st.end_state(mode, text)
            #    mode = InputState.Template
            elif line.startswith('---') and mode == InputState.TestIn:
                st.end_state(mode, text)
                mode = InputState.TestOut
                print(f'current mode={mode}')
            elif line.startswith('===') and mode == InputState.TestOut:
                st.end_state(mode, text)
                mode = InputState.TestIn
            else:
                text.append(line)
                cleanup = False
            
            if cleanup:
                text = []
        
        if not mode == InputState.TestIn:
            st.end_state(mode, text)

        st.text += st.open_visible_tests(st.config.get('visible_tests'))
        return st
        
    def end_state(self, mode, text):
        print(f'end state mode={mode}')
        if mode == InputState.Statement:
            self.text = html(text)
        elif mode == InputState.TestIn :
            self.test_input = text
        elif mode == InputState.TestOut :
            self.add_sample(to_text(self.test_input), to_text(text))
            print(f'tests = {self.test_cases}')
        elif mode == InputState.Header :
            self.header = to_text(text)
        elif mode == InputState.Footer :
            self.footer = to_text(text)
        elif mode == InputState.Code :
            self.template = to_text(text)
            print(f'template = {self.template}')
        elif mode == InputState.Config:
            d = parse_config(text)
            self.config.update(d)
            print(f'config = {self.config}')
        else:
            logger.warning(f'Unexpected inline task state={mode}')



'''
{
    "stepSource": {
        "reason_of_failure": "",
        "error": {
            "text": "",
            "code": "",
            "params": {}
        },
        "warnings": [],
        "instruction_id": null,
        "has_instruction": false,
        "cost": 10,
        "is_solutions_unlocked": false,
        "solutions_unlocked_attempts": 3,
        "max_submissions_count": 3,
        "has_submissions_restrictions": false,
        "create_date": "2020-09-20T19:50:33.000Z",
        "actions": {
            "edit_instructions": "#",
            "submit": "#"
        },
        "block": {
            "name": "code",
            "text": "<p>Даны координаты 3 вершин треугольника (x1, y1), (x2, y2), (x3, y3).</p>\n<p><strong>Возьмите функцию</strong> <code>dist(x1, y1, x2, y2)</code>, которая вычисляет расстояние между ними по формуле $$c^2 = (x_1 - x_2)^2 + (y_1 - y_2)^2$$ из предыдущей задачи.</p>\n<p><strong>Напишите функцию</strong> <code>area(x1, y1, x2, y2, x3, y3)</code>, которая вычисляет площадь треугольника со сторонами $a, b, c$ по формуле $$s = \\sqrt {p \\cdot (p - a) \\cdot (p - b) \\cdot (p-c)}$$, где $p = (a + b + c) / 2$</p>\n<p><img src=\"http://judge2.vdi.mipt.ru/tasks/func/geron.jpg\" width=\"300\"></p>\n<pre><code class=\"python\">from math import sqrt  # функция вычисляет квадратный корень\n\ndef dist(x1, y1, x2, y2):\n# скопируйте код из предыдущей задачи\n\ndef area(x1, y1, x2, y2, x3, y3):\n# тут нужно написать код\n\nx1, y1, x2, y2, x3, y3 = map(float, input().split())\ns = area(x1, y1, x2, y2, x3, y3)\nprint(s)\n</code></pre>",
            "video": null,
            "options": {
                "execution_time_limit": 5,
                "execution_memory_limit": 256,
                "limits": {
                    "python3": {
                        "time": 15,
                        "memory": 256
                    }
                },
                "code_templates": {
                    "python3": "from math import sqrt\n\ndef dist(x1, y1, x2, y2):\n    dx = x1 - x2\n    dy = y1 - y2\n    return sqrt(dx*dx + dy*dy)\n\ndef area(x1, y1, x2, y2, x3,y3):\n    # тут нужно написать код, воспользуйтесь функцией dist\n\nx1, y1, x2, y2, x3,y3 = map(float, input().split())\ns = area(x1, y1, x2, y2, x3,y3)\nprint(s)"
                },
                "code_templates_header_lines_count": {
                    "python3": 0
                },
                "code_templates_footer_lines_count": {
                    "python3": 0
                },
                "code_templates_options": {},
                "samples": [
                    [
                        "3 0 0 4 0 0",
                        "6.0"
                    ]
                ],
                "is_run_user_code_allowed": true
            },
            "subtitle_files": [],
            "source": {
                "code": "# This is a sample Code Challenge\n# Learn more: https://stepik.org/lesson/9173\n# Ask your questions via support@stepik.org\n\nimport math\n\ndef generate():\n    return [] \n\ndef check(reply, clue):\n    if reply == '':\n        return False\n    reply = float(reply)\n    clue = float(clue)\n    return abs(float(reply) - float(clue)) < 0.01\n    #return replay.strip() == clue.strip()\n\ndef dist(x1, y1, x2, y2):\n    dx = x1 - x2\n    dy = y1 - y2\n    return math.sqrt(dx*dx + dy*dy)\n    \n#def solve(dataset):\n#    x1, y1, x2, y2, x3, y3 = map(float, dataset.split())\n#    a = dist(x1, y1, x2, y2)\n#    b = dist(x1, y1, x3, y3)\n#    c = dist(x2, y2, x3, y3)\n#    p = (a + b + c) / 2\n#    return str(math.sqrt(p*(p-a)*(p-b)*(p-c)))",
                "execution_memory_limit": 256,
                "execution_time_limit": 5,
                "is_memory_limit_scaled": true,
                "is_run_user_code_allowed": true,
                "is_time_limit_scaled": true,
                "manual_memory_limits": [],
                "manual_time_limits": [],
                "samples_count": 1,
                "templates_data": "::python3\nfrom math import sqrt\n\ndef dist(x1, y1, x2, y2):\n    dx = x1 - x2\n    dy = y1 - y2\n    return sqrt(dx*dx + dy*dy)\n        \ndef area(x1, y1, x2, y2, x3,y3):\n    # тут нужно написать код, воспользуйтесь функцией dist\n    \nx1, y1, x2, y2, x3,y3 = map(float, input().split())\ns = area(x1, y1, x2, y2, x3,y3)\nprint(s)\n    \n\n\n\n\n",
                "test_archive": [],
                "test_cases": [
                    [
                        "3 0 0 4 0 0",
                        "6.0"
                    ],
                    [
                        "0 4 3 0 0 0",
                        "6.0"
                    ],
                    [
                        "0 1 0 5 1 2",
                        "1.9999999999999991"
                    ],
                    [
                        "1 2 3 4 5 6",
                        "0.0"
                    ],
                    [
                        "-1.3 5.1 1.7 1.1 1.7 5.1",
                        "6.000000000000001"
                    ]
                ],
                "are_all_tests_scored": false
            },
            "subtitles": {},
            "tests_archive": "/api/step-sources/1576649/tests",
            "feedback_correct": "",
            "feedback_wrong": ""
        },
        "instruction_type": null,
        "lesson_id": "408292",
        "position": 6,
        "status": "ready",
        "instruction": null,
        "lesson": "408292"
    }
}
'''    