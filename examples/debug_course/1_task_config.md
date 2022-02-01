# Проверка параметров конфигурации задачи

lesson = 561913

## TASKINLINE Все параметры по умолчанию

В этой задаче все параметры включены по умолчанию.

Список параметров и их значения по умолчанию:

| Параметр в md  | Значение по умолчанию | Что это в stepik | Как посылается |
|----|----|----|----|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |


Печатаем числа от `a` до `b`. Эти числа даны. Печатать все числа в 1 строку через пробел.

В этой задаче уже может быть проблема с тем, что часть печатают в конце дополнительный пробел и ставят или нет `\n`

### Вариант С пробелом в конце (работает)
```python
a, b = map(int, input().split())
for i in range(a, b+1):
    print(i, end=' ')
```
### Вариант без последнего пробела (работает) 
```python
a, b = map(int, input().split())
print(*range(a, b+1))
```
### Вариант по 1 числу на строку (не работает)

```python
a, b = map(int, input().split())
print(*range(a, b+1), sep='\n')
```

### Показываются условия и ожидаемые результаты не только в 1 тесте

```python
print(1, 2, 3)
```

Так как чекерам плохо, когда нет выходных данных, формулируйте задачи так, чтобы они обязательно что-то печатали. Хотя бы `No data`

TEST
1 3
----
1 2 3
====
7 7
----
7
====
10 15
----
10 11 12 13 14 15
====

## TASKINLINE Описано максимальное количество параметров

Печатаем числа от `a` до `b`. Эти числа даны. Печатать все числа в 1 строку через пробел.

### Вариант С пробелом в конце (работает)
```python
a, b = map(int, input().split())
for i in range(a, b+1):
    print(i, end=' ')
```
### Вариант без последнего пробела (работает) 
```python
a, b = map(int, input().split())
print(*range(a, b+1))
```
### Вариант по 1 числу на строку (не работает)

```python
a, b = map(int, input().split())
print(*range(a, b+1), sep='\n')
```

### Показываются условия и ожидаемые результаты не только в 1 тесте

```python
print(1, 2, 3)
```

Так как чекерам плохо, когда нет выходных данных, формулируйте задачи так, чтобы они обязательно что-то печатали. Хотя бы `No data`

CONFIG
# будет показано 2 теста как пример входных и выходных данных
sample_tests = 2 

TEST
1 3
----
1 2 3
====
7 7
----
7
====
10 15
----
10 11 12 13 14 15
====