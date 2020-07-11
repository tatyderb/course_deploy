# course_deploy
Usage:
deploy.py md_file

md_file - имя файла с текстом урока и вопросами в формате markdown

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

Далее идет информация об уроке (в stepik не используется).

Далее каждый заголовок 2 уровня начинает шаг. После \#\# через пробел можно указать тип шага:
```cpp
## TYPE пробел заголовок
```
TYPE может быть следующим:
* TEXT или отсутствует - это обычный шаг с методическими материалами;
* PROBLEM - указание на вставку задачи, на следующей строке - название директории с задачей в формате `problem = sum_1`
* QUIZ - вопрос в формате [AIKEN](https://docs.moodle.org/37/en/Aiken_format);
* VIDEO - далее идет урл на видео в формате `video=https://d3c33hcgiwev3.cloudfront.net/KYDrAeHNEeiAgQrXx6bp4g.processed/full/360p/index.mp4?Expires=1563753600&Signature=V1YOioA-2y8C52Sf-tHLBnBxfAfu3lP2gUV4eajalMH-lA-uJC1xWPfbfBFOy90BHfoSqxk7raYONL0FlrF18NDaTxLkrKZ~~GB4QD5YxNCEPqug2HQQf4itZkf0M4GkwgPWZX9~QXkJjgX9x0LyhflLCgfCxCrZhY8AnpwgPes_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A`

