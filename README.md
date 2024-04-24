# Клон игры Bomberman для игры вдвоем по сети.
![Menu screenshot](https://github.com/coffeecoder1337/bombers/blob/master/rdImages/menu.png?raw=true)
![InGame screenshot](https://github.com/coffeecoder1337/bombers/blob/master/rdImages/game.png?raw=true)

## Установка <br>
`git clone https://github.com/coffeecoder1337/bombers` <br>
`cd bombers` <br>
`pip install -r requirements.txt` <br>

## Запуск локально <br>
Для проверки работоспособности проекта (запустить два окна на одном компьютере), нужно запустить файл server.py <br>
`python server.py`

Далее запустить в двух новых терминалах файл main.py <br>
`python main.py`

## Запуск на сервере <br>
Для игры по сети необходимо загрузить файл server.py на удаленный сервер и указать IP этого сервера в файле main.py <br>
`g = Game(host="localhost")` localhost заменить на IP (например, host="172.104.253.171")

# Функционал
На данный момент в игре есть два вида бомб: лазерная и ракетная.
![Laser bomb](https://github.com/coffeecoder1337/bombers/blob/master/images/bombs/bomb_laser.png)
![Rocket bomb](https://github.com/coffeecoder1337/bombers/blob/master/images/bombs/bomb2.png)

Лазерная бомба способна разрушать блоки-препятствия.
![Destructive block](https://github.com/coffeecoder1337/bombers/blob/master/images/blocks/1.png)

# Конструктор уровней
![Level constructor](https://github.com/coffeecoder1337/bombers/blob/master/rdImages/constructor.png?raw=true)
Вы можете создавать собственные уровни с помощью конструктора. Для этого нужно запустить файл constructor.py <br>
`python constructor.py` разместить места появления игроков (красная и синяя моделька), разместить блоки и выйти из конструктора. <br>
Далее необходимо переместить файл `level.txt` в папку `levels` и добавить к имени файла число на 1 больше чем максимальный уровень в папке `levels` <br>
Например, в папке `levels` есть следующие уровни:
- level1.txt
- level2.txt
- level3.txt <br>
Тогда файл нужно переименовать в level4.txt <br>
Уровень выбирается случайно из всех доступных уровней.
