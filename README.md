# Ugra CTF Quals 2023

[Сайт](https://2023.ugractf.ru) | 14–15 января 2023

## Таски

[Бухгалтерия](tasks/bookkeeping/) (ivanq, stegano 100)  
[Захват трафика](tasks/capture/) (baksist, forensics 100)  
[Антивирус возвращается](tasks/collateral/) (ivanq, ctb 200)  
[Crypdle](tasks/crypdle/) (ivanq, reverse 250)  
[Криптобаш](tasks/cryptoneliner/) (baksist, crypto 200)  
[Глубина](tasks/depth/) (ivanq, ppc 150)  
[Bege](tasks/ecipher/) (gudn, reverse 300)  
[Элементарно](tasks/elementary/) (ivanq, reverse 100)  
[Прямо как у NSA](tasks/espionage/) (ivanq, crypto 150)  
[Старые добрые времена](tasks/goodolddays/) (ivanq, web 200)  
[Голливуд](tasks/hollywood/) (ivanq, ppc 250)  
[Maze Runner](tasks/mazerunner/) (ivanq, ppc 300)  
[PEBCAK](tasks/pebcak/) (ivanq, reverse 150)  
[Мультфильмы](tasks/pity/) (ivanq, misc 150)  
[Доказательство запугиванием](tasks/proofbyintimidation/) (ivanq, ctb 200)  
[Советские вступительные в ясельный класс](tasks/qrec/) (gudn, ppc 400)  
[Qualification](tasks/qualification/) (rozetkin, reverse 200)  
[Безопасность должна быть доступной](tasks/safestr/) (gudn, pwn 100)  
[Кто ищет, тот всегда найдёт](tasks/seeker/) (baksist, osint 200)  
[Snow Crash](tasks/snowcrash/) (ivanq, reverse 300)  
[Музыкальная пятиминутка](tasks/takefive/) (ksixty, stegano 50)  
[Сельский блог](tasks/thevillage2/) (nsychev, web 100)  
[Скорость без границ](tasks/tortoise/) (ivanq, crypto 350)  
[Трисекция](tasks/trisection/) (baksist, web 100)  
[Поле для сдачи флага](tasks/warmup/) (nsychev, misc 10)  
[Водоворот](tasks/whirlpool/) (ivanq, crypto 50)  

## Команда разработки

Олимпиада была подготовлена командой [team Team].

[Никита Сычев](https://github.com/nsychev) — руководитель команды, разработчик тасков и системы регистрации  
[Калан Абе](https://github.com/enhydra) — разработчик сайта  
[Коля Амиантов](https://github.com/abbradar) — инженер по надёжности  
[Ваня Клименко](https://github.com/ksixty) — разработчик тасков, сайта и платформы, дизайнер  
[Иван «Ivanq» Мачуговский](https://github.com/imachug) — разработчик тасков и платформы  
[Даниил Новоселов](https://github.com/gudn) — разработчик тасков  
[Матвей Сердюков](https://github.com/baksist) — разработчик тасков  
[Евгений Черевацкий](https://github.com/rozetkinrobot) — разработчик тасков

## Организаторы

Организаторы Ugra CTF — Югорский НИИ информационных технологий, Департамент информационных технологий и цифрового развития ХМАО–Югры и Департамент образования и науки ХМАО–Югры. Олимпиаду разрабатывает команда [team Team].

## Генерация заданий

Некоторые таски создаются динамически — у каждого участника своя, уникальная версия задания. В таких заданиях вам необходимо запустить генератор — обычно он находится в файле `generate.py` в директории задания. Обычно генератор принимает три аргумента — уникальный идентификатор, директорию для сохранения файлов для участника и названия генерируемых тасков (последний, как правило, не используется). Например, генератор можно запустить так:

```bash
./tasks/hello/generate.py 1337 /tmp/hello
```

Уникальный идентификатор используется для инициализации генератора псевдослучайных чисел, если такой используется. Благодаря этому, повторные запуски генератора выдают одну и ту же версию задания.

Генератор выведет на стандартный поток вывода JSON-объект, содержащий флаг к заданию и информацию для участника, а в директории `/tmp/hello` появятся вложения, если они есть.

## Лицензия

Материалы соревнования можно использовать для тренировок, сборов и других личных целей, но запрещено использовать на своих соревнованиях. Подробнее — [в лицензии](LICENSE).
