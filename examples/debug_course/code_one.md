# code

lesson = 383213
lang = c_valgrind

## TASKINLINE

[Ссылка на себя](https://stepik.org/lesson/383213/step/1)

Напишите функцию **func_sum**, которая возвращает сумму аргументов.
```cpp
int func_sum(int x, int y);
```

HEADER
#include <stdio.h>
int func_sum(int x, int y);
int main()
{
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d\n", func_sum(a, b));
    return 0;
}

CODE
int func_sum(int x, int y)
{
    // тут нужно написать код
}
TEST
2 5
----
7
====
-3 1
----
-2
====
