# course_deploy
Usage: deploy.py [-h] [-f | -t] [-d] [--html] [-s STEP] md_file


| Обязательный аргумент: | Зачем он                                                 |
|------------------------|----------------------------------------------------------|
| md_file                | имя файла с текстом урока и вопросами в формате markdown |

| Опциональный аргумент: | Зачем он                                                                                                       |
|------------------------|----------------------------------------------------------------------------------------------------------------|
| -h, --help             | узнать как использовать программу                                                                              |
| -f, --full             | загрузить шаги всех типов                                                                                      |
| -t, --text             | загрузить только текстовые шаги                                                                                |
| -d, --debug            | загрузить весь урок одним шагом                                                                                |
| --html                 | загрузить урок в html файл, а не на сайт                                                                       |
| -s STEP, --step STEP   | обновить только шаг под номером STEP (нумерация начинается с 1), также поддерживается отрицательная индексация |



## Полжите свои аутентификационные данные в файл auth_data.py

Как написано в этом файле.
Пожалуйста, не комитьте файл с ВАШИМИ аутентификационными данными в открытый репозиторий.

## Структура файла в формате markdown

1 урок пишется в 1 файл в формате markdown (todo: уточнить поддерживаемый диалект и расширения).

Заголовком 1 уровня пишется название урока.

Далее идет служебная информация для скриптов. Куда именно выкладывать данный файл.
```cpp
lesson = 239930
```
/home/farid/deploy/deploy_explore
Далее идет информация об уроке (в stepik не используется).

Далее каждый заголовок 2 уровня начинает шаг. После \#\# через пробел можно указать тип шага:
```cpp
## TYPE пробел заголовок
```
TYPE может быть следующим:
* TEXT или отсутствует - это обычный шаг с методическими материалами;

* PROBLEM - указание на вставку задачи, на следующей строке - название директории с задачей в формате `problem = sum_1`

* QUIZ - вопрос в формате [AIKEN](https://docs.moodle.org/37/en/Aiken_format);
  * По умолчанию предлагаемые ответы перемешиваются. Чтобы зафиксировать порядок ответов напишите на строке `SHUFFLE: False` (или `True`, без учета регистра) до строки с `ANSWER`.
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
    (учитывается регистр, ответом может быть слово, словосочетание или предложене, но кол-во пробелов не учитывается).

* VIDEO - далее идет урл на видео в формате `video=https://d3c33hcgiwev3.cloudfront.net/KYDrAeHNEeiAgQrXx6bp4g.processed/full/360p/index.mp4?Expires=1563753600&Signature=V1YOioA-2y8C52Sf-tHLBnBxfAfu3lP2gUV4eajalMH-lA-uJC1xWPfbfBFOy90BHfoSqxk7raYONL0FlrF18NDaTxLkrKZ~~GB4QD5YxNCEPqug2HQQf4itZkf0M4GkwgPWZX9~QXkJjgX9x0LyhflLCgfCxCrZhY8AnpwgPes_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A`


