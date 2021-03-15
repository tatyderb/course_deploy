# Благодарности

Этого бы кода не было, если бы не ответы от [Илья Ставиди](https://stepik.org/users/59311452) на наши вопросы.

# Убиваем конечные пробелы на всех строках

[Отсюда](https://stepik.org/lesson/244445/step/6?unit=490603)
```python
def check(reply, clue):
    # return reply.strip() == clue.strip()
    return (
        "\n".join(x.strip() for x in reply.strip().splitlines()) ==
        '\n'.join(y.strip() for y in clue.strip().splitlines()))
```    

# открытые и закрытые тесты

[Отсюда](https://stepik.org/lesson/394668/step/2?discussion=3510325&unit=383635)

```python
# This is a sample Code Challenge
# Learn more: https://stepik.org/lesson/9173
# Ask your questions via support@stepik.org

def generate():
    opened_samples = ("232\n83", '14\n50', '212\n8506', )
    closed_samples = ("25\n12", '45\n4', '60\n21', )
    hidden_samples = ("123\n45", '67\n89', )
    return (
        [(x, (x, solve(x))) for x in opened_samples] + 
        [(x, ('', solve(x))) for x in closed_samples] + 
        [(x, (None, solve(x))) for x in hidden_samples])

def check(reply, xclue):
    if type(xclue) == str:
        if reply.strip() == xclue.strip():
            return True
        else:
            return False, (
                '\nУпс, упал тест.\n' +
                f'\nОжидался ответ:\n{clue}\n\nПолучен ответ:\n{reply}\n')
    else:
        dataset = xclue[0]
        clue = xclue[1]
        if reply.strip() == clue.strip():
            return True, "Всё правильно!"
        else:
            return False if dataset is None else (False, (
                '\nУпс, упал тест.\n' +
                (f'\nИсходные данные:\n{dataset}\n' if dataset else '') +
                f'\nОжидался ответ:\n{clue}\n\nПолучен ответ:\n{reply}\n'))

def solve(dataset):
    a, b = dataset.split()
    return str(int(a) + int(b))
```    

Напомню:

* сначала запускаются тесты со вкладки Тестовые данные, 
* затем сгенерированные тесты,
* а под занавес ещё и загруженные в zip-файле (если они есть).

В этом задании первый тест указано на вкладке, генерируемые видны в тексте функции генерации, а также подгружен zip-файл с парочкой тривиальных тестов.

Для проверки падения первого теста используйте код:

```python
a, b = int(input()), int(input())
print(a - b)
```

Для проверки падения открытых тестов используйте предложенный код:

```python
a, b = int(input()), int(input())
if (a, b) == (11, 8):
    print(19)
else:
    print(a - b)
```

Для проверки падения закрытых тестов используйте код:

```python
a, b = int(input()), int(input())
if (a, b) in ((11, 8), (232, 83), (14, 50), (212, 8506), ):
    print(a + b)
else:
    print(a - b)
```

Для проверки падения теста из списка скрытых используйте код:


```python
a, b = int(input()), int(input())
if (a, b) in ((11, 8), (232, 83), (14, 50), (212, 8506), (25, 12), (45, 4), (60, 21), ):
    print(a + b)
else:
    print(a - b)
```

Для проверки прохождения всех тестов используйте код:

```python
a, b = int(input()), int(input())
print(a + b)
```

Чтобы прекрасный ответ не печатался как

```cpp
Passed test #2. Всё правильно!
Passed test #3. Всё правильно!
Passed test #4. Всё правильно!
Passed test #5. Всё правильно!
Passed test #6. Всё правильно!
Passed test #7. Всё правильно!
```

а проходил как обычно, делайте так:

```python
        return True  # , "Всё правильно!"
```

**Обратите внимание, что для тестов, указанных вручную на вкладке Тестовые данные, а также загруженных в виде zip-архива, не удаётся вывести исходные данные, а только ожидаемый и полученный ответы, поскольку при таком подходе исходные данные для них недоступны.**

[дока степика](https://stepik.org/lesson/59057/step/3?unit=36621)

Также крайне желательно первый тест (тот самый, который виден курсантам) указывать на вкладке Тестовые данные, чтобы реакция на него была стандартной, иначе вся информация оказывается продублирована, например, таким образом:

```cpp
Failed test #1 of 10. 
Упс, упал тест.

Исходные данные:
232
83

Ожидался ответ:
315

Получен ответ:
149


This is a sample test from the problem statement!

Test input:
232
83
Correct output:
315

Your code output:
149
```
Понятно, что этот код можно дорабатывать ещё долго и затейливо, тут вы ограничены только полётом своей фантазии.


