# course_deploy

Скрипты для деплоя онлайн-курсов, написанных в формате markdown на stepik.org.

Кроме текстовых шагов поддерживаются разные типы вопросов и задачи. Задачи можно как писать сразу в файле урока, так и ссылаться на задачу, предназначенную для деплоя в системе ejudge.

## Запуск

Usage: deploy.py [-h] [-f | -t] [-d] [--html] [-s STEP] [--lang LANGUAGE] md_file


| Обязательный аргумент:     | Зачем он                                                 |
|----------------------------|----------------------------------------------------------|
| md_file                    | имя файла с текстом урока и вопросами в формате markdown |

| Опциональный аргумент:     | Зачем он                                                                                                       |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| -h, --help                 | узнать как использовать программу                                                                              |
| -f, --full                 | загрузить шаги всех типов                                                                                      |
| -t, --text                 | загрузить только текстовые шаги                                                                                |
| -d, --debug                | загрузить весь урок одним шагом                                                                                |
| --html                     | загрузить урок в html файл, а не на сайт                                                                       |
| -s STEP, --step STEP       | обновить только шаг под номером STEP (нумерация начинается с 1), также поддерживается отрицательная индексация |
| -c CONFIG, --config CONFIG | загрузить, используя данные из конфигурационного файла                                                         |
/ -l LANGUAGE, --lang LANGUAGE | установить для загружаемых задач на программирование язык `::LANGUAGE` |

## Полжите свои аутентификационные данные в файл auth_data.py

Как написано в этом файле.
Пожалуйста, не комитьте файл с ВАШИМИ аутентификационными данными в открытый репозиторий.

## Структура файла в формате markdown

1 урок пишется в 1 файл в формате markdown (todo: уточнить поддерживаемый диалект и расширения).

Заголовком 1 уровня пишется название урока.

Далее идет служебная информация для скриптов. Куда именно выкладывать данный файл.
```cpp
lesson = 239930
lang = c_valgrind
```
* `lang` - (не обязательное) задает поле `::язык` в заданиях типа Code (программа), возможные значения [языка программирования](https://stepik.org/lesson/63139/step/11)

Далее идет информация об уроке (в stepik не используется).

Далее каждый заголовок 2 уровня начинает шаг. После \#\# через пробел можно указать тип шага:
```cpp
## TYPE пробел заголовок
```
TYPE может быть следующим:
* TEXT или отсутствует - это обычный шаг с методическими материалами.

* PROBLEM - указание на вставку задачи, на следующей строке - название директории с задачей в формате `problem = sum_1`.

* QUIZ - вопрос в формате [AIKEN](https://docs.moodle.org/37/en/Aiken_format).
  * По умолчанию предлагаемые ответы перемешиваются. Чтобы зафиксировать порядок ответов 
    напишите на одной строке `SHUFFLE: False` (или `True`, без учета регистра) до строки с `ANSWER`
  * Если нужно задать много правильных ответов, то перечисляем их в любом порядке через запятую `ANSWER: A, D, C`

* NUMBER - вопрос, ответом на который является число (точное или в некотором диапазоне).
  Примеры использования [здесь](https://github.com/tatyderb/course_deploy/blob/master/examples/question_example.md).
  * Ответ записывается в виде: `ANSWER: 12 +- 0.5`, где 12 - среднее, а 0.5 - погрешность
  * Если ответом является точное число: `ANSWER: 12`
  * Правильных может быть несколько, но ученик может ввести только одно число

* STRING - вопрос, ответом на который является слово или строка.
  Примеры использования [здесь](https://github.com/tatyderb/course_deploy/blob/master/examples/question_example.md).
  * Ответ записывается в виде: `ANSWER: Слово`
  * Правильный ответ только один. От ученика требуется полностью совпадающий с паттерном ответ
    (учитывается регистр, ответом может быть слово, словосочетание или предложене, но кол-во пробелов не учитывается)
    
* VIDEO - далее идет урл на видео в формате `video=https://d3c33hcgiwev3.cloudfront.net/KYDrAeHNEeiAgQrXx6bp4g.processed/full/360p/index.mp4?Expires=1563753600&Signature=V1YOioA-2y8C52Sf-tHLBnBxfAfu3lP2gUV4eajalMH-lA-uJC1xWPfbfBFOy90BHfoSqxk7raYONL0FlrF18NDaTxLkrKZ~~GB4QD5YxNCEPqug2HQQf4itZkf0M4GkwgPWZX9~QXkJjgX9x0LyhflLCgfCxCrZhY8AnpwgPes_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A`
    * не реализовано

* TASK - задача по программированию (1 задача в 1 директории, нужно для портирования задач из ejudge или poligon).
  Примеры использования [здесь](https://github.com/tatyderb/course_deploy/blob/master/examples/question_example.md).
  * Путь к директории с задачей, название файла с условием и т.д. указываются в виде: `param = value`.
    По умолчанию указывается относительно директории examples, но может и относительно директории, указанной в конфигурационном файле под именем task_root.
  * Файл с условием в формате xml
  * Тесты представляют собой директорию, где для каждого теста входной поток записан в 001.dat, 
    а ожидаемый выходной в 001.ans и далее для тестов 002, 003 и до конца. 
    Имена dat и ans файлов должны совпадать, нумерация от 001 идет по порядку (без разрывов)
  * Если не будет условия, оно будет заменено на стандартное, 
    если не будет ни условия, ни тестов, то будет загружена стандартная задача
  * У задачи может быть header и footer. Названия файлов указываются с ними напрямую
    и включаются в задачу только при указании языка в конфигурационном файле: `task_lang: c`
  * По умолчанию ученик видит только первый тест. Можно явно указать количество видимых тестов: `visible_tst_num = 4`
  
* TASKINLINE - задача на программирование [пример](https://github.com/tatyderb/course_deploy/tree/master/examples/debug_course/code_one.md)
    * идет ключевое слово раздела, потом информация раздела до следующего раздела или до следующего шага или до конца файла.
    * CODE - этот код будет набран в окне ввода. Полезно, если вы хотите облегчить студенту жизнь.
    * HEADER - код пристыковывается ДО кода студента.
    * FOOTER - код пристыковывается ПОСЛЕ кода студента.
    * TEST - тесты (один или более раз) в формате
    * CONFIG - параметры конфигурации, задаются в виде `параметр : значение` в одну строку, параметры:
        * checker - код для проверки ответов, по умолчанию сравнивает ожидаемый ответ и полученый ответ как текст, с учетом количества строк, но убирая пробельные символы в конце текста, возможны другие чекеры:
            * std_float_seq - последовательность чисел с плавающей точкой, сравнивает с точностю до `EPS = 0.0001`, другую EPS можно задать в дополнительных параметрах
        * additional_params - дополнительные параметры для чекера, солвера, тестов и тп. Задаем в одну строку с \n если нужно несколько строк кода параметров задать.
```
входные данные теста
----
ожидаемые выходные данные теста
====
```    

### Установка языка программирования для задачи на программирование

Если не устанавливать язык, то можно будет сдавать на любом языке, который поддерживает платформа. Это полезно, если у вас курс по алгоритмистике.

Но если вы изучаете конкретный язык, то нужно ограничить язык, который используется для проверки. 
По возрастанию приоритета язык можно задать:

* `python3` - по умолчанию,
* задан в конфигурационном файле в поле `task_lang`,
* задан в аргументах командной строки с ключом `--lang`
* записан в md файле урока, сразу после lesson_id в виде `lang = c_valgrind`

Запись в файле урока самая приоритетная, ибо автор при разработке курса думал, на каких языках его можно проводить.
