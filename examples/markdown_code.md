# Отладка отображения примеров кода с объяснениями
lesson=250513

## source + pre в таблице markdown

Рвется на несколько строк `mv one.c two.c`

Команда | Что делали | Команды и ответ консоли
---------------|-------|---------------
  ls |просмотр содержимого каталога *`/home:`* сначала текущего (по умолчанию), затем каталога *`student`* |<source lang="bash">>ls</source></br><source lang="bash">student</source></br><source lang="bash">>ls student<source></br><source lang="bash">workspace</source></br><source lang="bash">></source>
  mkdir | создание нового каталога  myWorkFolder в текущем каталоге и просмотр текущего каталога. Если до этого каталог был пуст, напечатается только название myWorkFolder, если  нет, то в списке будут и другие файлы | <source lang="bash">>mkdir myWorkFolder</source></br><source lang="bash">>ls</source></br><source lang="bash">myWorkFolder</source>
  cd | просмотр текущего каталога </br>переход в каталог myWorkFolder</br>просмотр нового текущего каталога (myWorkFolder)</br>переход на каталог выше (обратно)</br>Просмотр каталога</br> Переход в каталог *`/home`*</br> Переход в `домашний каталог` |<source lang="bash">> ls</source></br><source lang="bash">myWorkFolder</source></br><source lang="bash">>cd myWorkFolder</source></br>>ls </source></br><source lang="bash">myprog.c</source></br><source lang="bash">> cd ..</source></br><source lang="bash">> ls</source></br><source lang="bash">myWorkFolder</source></br><source lang="bash">> cd /home</source></br><source lang="bash">>cd ~</source>
  cp | Копирование файла `myprog.c` в файл `yourprog.c` и просмотр </br>Копирование файла из myWorkFolder в текущий каталог. В текущем каталоге появится файл с таким же именем.</br> Копирование файла otherfile в каталог myWorkFolder. В каталоге myWorkFolder  появится файл с таким же именем | <source lang="bash">>cp myprog.c yourprog.c</source></br><source lang="bash">>ls myprog.c yourprog.c</source></br><source lang="bash">>cp myWorkFolder/myprog.c .</source></br><source lang="bash">>cp  otherfile myWorkFolder/</source>
  mv | Переименование файла *`myprog.c`* в файл *`yourprog.c`* и просмотр </br>Перемещение файла из *`myWorkFolder`* в текущий каталог. В текущем каталоге появится файл с таким же именем, в каталоге myWorkFolder будет удален.</br>Перемещение файла *`otherfile`* в каталог *`myWorkFolder`*. В каталоге myWorkFolder появится файл с таким же именем, в текущем будет удален. |<source lang="bash">>ls</source></br><source lang="bash"> myprog.c</source></br> <source lang="bash"> >mv myprog.c yourprog.c</source></br> <source lang="bash">>ls</source></br> <source lang="bash"> yourprog.c</source></br><pre><source lang="bash">>mv myWorkFolder/myprog.c .</source></pre></br></pre><source lang="bash">>mv otherfile myWorkFolder/</source></pre>

## html table + markdown codeblock

<table>
<tr>
	<td>`ls`
	</td>
	<td>просмотр содержимого каталога *`/home:`* сначала текущего (по умолчанию), затем каталога *`student`*
	</td>
	<td>
```cpp
>ls
student
>ls student
workspace
```	
	</td>
</tr>
<tr>
	<td>mkdir
	</td>
	<td>создание нового каталога  myWorkFolder в текущем каталоге и просмотр текущего каталога. Если до этого каталог был пуст, напечатается только название myWorkFolder, если  нет, то в списке будут и другие файлы
	</td>
	<td>
```cpp
>mkdir myWorkFolder
>ls
myWorkFolder
```	
	</td>
</tr>
<tr>
	<td>cd
	</td>
	<td>просмотр текущего каталога </br>переход в каталог myWorkFolder</br>просмотр нового текущего каталога (myWorkFolder)</br>переход на каталог выше (обратно)</br>Просмотр каталога</br> Переход в каталог *`/home`*</br> Переход в `домашний каталог` 
	</td>
	<td>
```cpp
> ls
myWorkFolder
>cd myWorkFolder
>ls 
myprog.c
> cd ..
> ls
myWorkFolder
> cd /home
>cd ~
```	
	</td>
</tr>
<tr>
	<td>cp
	</td>
	<td>Копирование файла `myprog.c` в файл `yourprog.c` и просмотр </br>Копирование файла из myWorkFolder в текущий каталог. В текущем каталоге появится файл с таким же именем.</br> Копирование файла otherfile в каталог myWorkFolder. В каталоге myWorkFolder  появится файл с таким же именем
	</td>
	<td>
```cpp
>cp myprog.c yourprog.c
>ls 
myprog.c yourprog.c
>cp myWorkFolder/myprog.c .
>cp otherfile myWorkFolder/
```	
	</td>
</tr>
<tr>
	<td>mv
	</td>
	<td>Переименование файла *`myprog.c`* в файл *`yourprog.c`* и просмотр </br>Перемещение файла из *`myWorkFolder`* в текущий каталог. В текущем каталоге появится файл с таким же именем, в каталоге myWorkFolder будет удален.</br>Перемещение файла *`otherfile`* в каталог *`myWorkFolder`*. В каталоге myWorkFolder появится файл с таким же именем, в текущем будет удален.
	</td>
	<td>
```cpp
>ls
myprog.c
>mv myprog.c yourprog.c
>ls
yourprog.c
>mv myWorkFolder/myprog.c .
>mv otherfile myWorkFolder/
```	
	</td>
</tr>
<tr>
	<td>
	</td>
	<td>
	</td>
	<td>
	</td>
</tr>
</table>

## Пытаемся сделать так, чтобы codeblock не переносило на следующую строку

<table>
<tr>
	<td>mv
	</td>
	<td>Переименование файла *`myprog.c`* в файл *`yourprog.c`* и просмотр </br>Перемещение файла из *`myWorkFolder`* в текущий каталог. В текущем каталоге появится файл с таким же именем, в каталоге myWorkFolder будет удален.</br>Перемещение файла *`otherfile`* в каталог *`myWorkFolder`*. В каталоге myWorkFolder появится файл с таким же именем, в текущем будет удален.
	</td>
	<td><code><pre>
&gt; ls
myprog.c
&gt; mv myprog.c yourprog.c
&gt; ls
yourprog.c
&gt; mv myWorkFolder/myprog.c .
&gt; mv otherfile myWorkFolder/
</pre></code></td>
</tr>
</table>

Последняя попытка:
<table>
<tr>
	<td><code><pre>
&gt; ls
myprog.c
&gt; mv myprog.c yourprog.c
&gt; ls
yourprog.c
&gt; mv myWorkFolder/myprog.c .
&gt; mv otherfile myWorkFolder/
</pre></code></td>
	<td>Переименование файла *`myprog.c`* в файл *`yourprog.c`* и просмотр </br>Перемещение файла из *`myWorkFolder`* в текущий каталог. В текущем каталоге появится файл с таким же именем, в каталоге myWorkFolder будет удален.</br>Перемещение файла *`otherfile`* в каталог *`myWorkFolder`*. В каталоге myWorkFolder появится файл с таким же именем, в текущем будет удален.
	</td>
</tr>
</table>

Еще одна:

<table>
<tr>
	<td><code><pre>
&gt; ls
myprog.c
&gt; mv myprog.c yourprog.c
&gt; ls
yourprog.c
</pre></code></td>
	<td>Переименование файла *myprog.c* в файл *yourprog.c* и просмотр 
	</td>
</tr>
<tr>
	<td><code><pre>
&gt; mv myWorkFolder/myprog.c .
</pre></code></td>
	<td>Перемещение файла из *myWorkFolder* в текущий каталог. В текущем каталоге появится файл с таким же именем, в каталоге myWorkFolder будет удален.
	</td>
</tr>
<tr>
	<td><code><pre>
&gt; mv otherfile myWorkFolder/
</pre></code></td>
	<td>Перемещение файла *otherfile* в каталог *myWorkFolder*. В каталоге myWorkFolder появится файл с таким же именем, в текущем будет удален.
	</td>
</tr>
</table>


## Без таблицы

### ls

### ls директория

**Просмотр указанной директории**. Если директория не указана, то текущей директории.

В директории `/home` находится только директория `student`. В ней находится директория `work` и файл `my.c`.

Текущая директория `/home`. Выполним следующие действия

* Просмотр содержимого текущей директории (это `/home`)
```cpp
> ls
student
```

* просмотр содержимого директории `student`
```cpp
> ls student
work my.c 
```

### mkdir директория

**Создать директорию *директория***.

* просмотр текущей (пустой) директории;
* создание директории `myWorkFolder`
* просмотр директории (в ней есть директория myWorkFolder)

```cpp
> ls 

> mkdir myWorkFolder
> ls
myWorkFolder
```

### cd

### cd директория

**Перейти в *директория***. Если директория не указана, перейти в домашний каталог.

* просмотр текущего каталога 
* переход в каталог myWorkFolder
* просмотр нового текущего каталога (myWorkFolder)
* переход на каталог выше (обратно)
* Просмотр каталога
* Переход в каталог `/home`
* Переход в *домашний каталог*

```cpp
> ls
myWorkFolder
>cd myWorkFolder
>ls 
myprog.c
> cd ..
> ls
myWorkFolder
> cd /home
>cd ~
```

### cp откуда куда

**Копировать файл *откуда* в *куда***

* Копирование файла myprog.c в файл yourprog.c и просмотр (есть оба файла).
```cpp
>cp myprog.c yourprog.c
>ls 
myprog.c yourprog.c
```

* Копирование файла из myWorkFolder в текущий каталог. В текущем каталоге появится файл с таким же именем.
```cpp
>cp myWorkFolder/myprog.c .
```

* Копирование файла otherfile в каталог myWorkFolder. В каталоге myWorkFolder появится файл с таким же именем
```cpp
>cp otherfile myWorkFolder/
```

### mv откуда куда

**Копировать файл *откуда* в *куда***. Файл (директория) *откуда* будет удален. Используется для переименования файлов (директорий).

* Переименование файла myprog.c в файл yourprog.c и просмотр (файла с именем `myprog.c` не стало)
```cpp
>ls
myprog.c
>mv myprog.c yourprog.c
>ls
yourprog.c
```

* Перемещение файла из myWorkFolder в текущий каталог. В текущем каталоге появится файл с таким же именем, в каталоге myWorkFolder будет удален.

```cpp
>mv myWorkFolder/myprog.c .
```

* Перемещение файла otherfile в каталог myWorkFolder. В каталоге myWorkFolder появится файл с таким же именем, в текущем будет удален.
```cpp
>mv otherfile myWorkFolder/
```