# Maze Runner: Write-up

Нас забрасывает в rogue-like игру-лабиринт. На первый взгляд все выглядит просто: есть ограничение в 10 минут, нужно пройти несколько уровней, собрав все флаги. Из нетривиальных вещей — только порталы, которые добавляют к перемещениям некоторую недетерминированность.

А потом на пятом поле начинается жесть: поле 201&times;201 с 400 флагами и десятью порталами.

Автоматизация-с.

## Теоретическая сторона

Для решения лабиринтов есть много алгоритмов. Но в данном случае можно не мудрить и просто рекурсивно обойти все клетки. В псевдокоде:

```python
def walk_starting_from(x, y):
    for adjacent_cell, direction in cells_reachable_from(x, y):
        if has not visited adjacent_cell before:
            press_key(direction)
            walk_starting_from(adjacent_cell)
            press_key(reverse(direction))
```

В реальной реализации придется учитывать, что из клетки `(x, y)` могут быть достижимы не только обычные соседи, но, если в этой клетке расположен портал, и клетка на другой стороне портала (тогда для перехода нужно нажать клавишу `z` — и в обратном направлении тоже). Надо учесть и то, что после того, как подобран последний флаг, кнопки больше нажимать не нужно, ведь произойдет автоматический переход к следующему уровню. Помимо этого в качестве оптимизации можно также не выполнять лишние действия, не приводящие к сбору флага, например, заход в пустой тупик, но это не обязательно.

## Практическая сторона

Весь исходный код сайта расположен в одном файле. Стили нас не очень интересуют, важнее JavaScript.

Первая часть скрипта, по-видимому, отвечает за эффективный вывод графики. Спасибо разработчику, оставившему пару комментариев. Судя по всему, в переменной `currentField` поддерживается карта поля. Эту гипотезу сразу можно проверить через devtools (инструменты разработчика):

![DevTools, currentField](writeup/devtools-current-field.png)

По-видимому, Unicode парсить не придется: запретные для перемещения клетки обозначаются `#`, игрок — `@`, флаг — `.`. Исходный код функции `render` это подтверждает. Порталы обозначаются буквами, например, `A` — портал бирюзового цвета, `C` — желтого, и так далее.

Для взаимодействия используется HTTP с эндпоинтом `POST /api`: в содержимом запроса посылаются нажатые клавиши (стрелки посылаются как `<>^v`), а в ответ приходит JSON с картой поля и некоторой дополнительной информацией об уровне. Последняя важная деталь: из наличия переменной `keyBuffer` и реализации `dumpBuffer`, а также дампа сетевых сообщений, понятно, что можно посылать сразу несколько клавиш.

Теперь не составит труда написать решение на любом языке программирования: необходимо выполнить запрос к `POST /api` с пустым содержимым, решить лабиринт, получить последовательность действий, которую нужно выполнить, и одним запросом отправить ее на `POST /api`, чтобы получить карту следующего уровня, и так далее.

Чтобы не мучиться с собственной реализацией логики лабиринта, можно воспользоваться готовой игрой и написать решение прямо в DevTools. Судя по всему, автор игры это задумывал: в коде есть закомментированный «Automatic mode», который показывает, как получить информацию о поле и посылать команды. Остается заменить неэффективную реализацию (случайное блуждание) на эффективную (рекурсивный обход).

Пример такого решения можно посмотреть в файле [solution.js](solution.js).

После прохождения 30 уровней мы попадаем на уровень без флагов, а флаг написан в описании уровня:

![Final level](writeup/final-level.png)

Флаг: **ugra_listen_to_in_the_dark_by_bmth_2df688190bdc**