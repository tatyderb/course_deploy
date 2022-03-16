# Чекеры

lesson = 561914

## TASKINLINE float seq checker DEBUG

**Чекер для float с контролем количества строк**

Напишите программу, которая считает площадь треугольника по (x, y) координатам его вершин. 

Вывести квадрат площади и площадь.

**Этот шаг для отладки скриптов деплоя, для исследования параметров - следующий шаг**.

CODE
from math import sqrt  # функция вычисляет квадратный корень

def dist(x1, y1, x2, y2):
    a = (x1 - x2)
    b = (y1 - y2)
    return sqrt(a*a + b*b)

def area(x1, y1, x2, y2, x3, y3):
    # тут нужно написать код
    a = dist(x1, y1, x2, y2)
    b = dist(x1, y1, x3, y3)
    c = dist(x3, y3, x2, y2)
    p = (a + b + c) / 2
    s2 = (p * (p - a) * (p - b) * (p - c))
    return s2, sqrt(s2)

n = int(input())
x1, y1, x2, y2, x3, y3 = map(float, input().split())
s2, s = area(x1, y1, x2, y2, x3, y3)
print(s2, s, sep=' ')

TEST
1
0 1 0 5 1 2
----
3.9999999999999964 1.9999999999999991
====
2
0 1 0 5 1 2
----
4.01 
1.9999999999999991
====
5
-1.3 5.1 1.7 1.1 1.7 5.1
----
36 
6.000000000000001
====
CONFIG
checker: std_float_seq
additional_params: EPS = 0.1

## SKIP TASKINLINE Ручное исследование

Тут смотрим руками какие части есть.
