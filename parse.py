"""
Parse markdown file for deploying it step-by-step into lesson.

# Lesson title
lesson=1234
## step1 header
markdown text
## QUIZ
question in AIKEN format
"""

import logging
from pyparsing import Char, Word, CharsNotIn, ZeroOrMore, nums, alphas, alphanums, printables, srange


logger = logging.getLogger('deploy_scripts')

# TODO нужны ли kir_letter вместе с srange(['а-я_']) + srange(['А-Я_']) ?
kir_letter = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_'
WRD = Word(printables + kir_letter + srange(['а-я_']) + srange(['А-Я_']))
WRD_p = Word(alphanums + kir_letter + srange(['а-я_']) + srange(['А-Я_']))

WRDs = ZeroOrMore(WRD)

sharp = Char('#')
not_sh = CharsNotIn('#')


def error(message="Error"):
    raise ValueError(message)


def bool_check(param_name, line):
    """
    Разбирает line по формату 'param_name:true|false', возвращает True или False (case insensitive), в случае ошибки возвращает False
    :param param_name: ключ
    :param line: разбираемая строка
    :return: True или False в разбираемой строке
    """
    # Todo подумать, надо ли в слушае ошибки False или лучше exception
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


def param_set(tokens, param_dict):
    for idx, lex in enumerate(tokens):
        if tokens[idx] == '{{' and tokens[idx + 1] in param_dict and tokens[idx + 2] == '}}':
            tokens[idx] = tokens[idx + 2] = ''
            tokens[idx + 1] = str(param_dict[tokens[idx + 1]])
    return ' '.join(tokens)


def param_substitude(lines, param_dict):
    mask_par = (CharsNotIn('{{}}')[0, ] + '{{' + WRD_p + '}}' + CharsNotIn('{{}}')[0, ])[1, ] + Char('\n')[0, 1]
    # mask_par.setParseAction(param_set)
    mask_par.setParseAction(lambda tokens: param_set(tokens, param_dict))

    for line_to, line in enumerate(lines):
        line = line.rstrip()

        if not line:
            continue

        lines[line_to] = mask_par.transformString(line)

    return lines


def parse_lesson_header(line):
    """
    Разбирает line как начало урока, где
    # заголовок
    , заголовок пока никуда не пишется.
    Возвращает заголовок или пустую строку.
    """

    header_template = sharp + not_sh + WRDs

    if not line == header_template:
        error(f'Expect lesson header # text, now = {line}')

    m = header_template.parseString(line)
    lesson_header = m[1]
    return lesson_header


def is_H2(line):
    """
    Возвращает True если line начало шага, то есть строка вида
    ## TYPE заголовок
    , где TYPE может не быть.
    """
    H2_template = (sharp * 2) + not_sh + WRDs
    return line == H2_template


def parse_lesson_id(line):
    """
    Разбирает строку line вида
    lesson = число
    и возвращает это число.
    """
    id_template = 'lesson' + Char('=') + Word(nums)

    if not line == id_template:
        error(f'Expect lesson id as lesson=number, now = {line}')

    lesson = id_template.parseString(line)
    lesson_id = int(lesson[2])
    return lesson_id


def parse_task_language(line):
    """Разбирает строку вида lang=язык_задач, если язык пустой, возвращает None."""
    lang_template = 'lang' + Char('=') + Word('_'+alphanums)
    lang = None
    if line == lang_template:
        lang_tokens = lang_template.parseString(line)
        logger.info(f'lang_tokens={lang_tokens}')
        lang = lang_tokens[2]
    return lang

