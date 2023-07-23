# Тестовое задание: Разработка микросервиса для подготовки дайджестов контента

## Якорь на описание работы сервиса

* [Описание](#описание)

## Цель

Разработайте микросервис, который будет формировать дайджесты контента для пользователей на основе их подписок. Дайджест представляет собой выборку постов из различных источников, на которые подписан пользователь. Вы можете выбрать любую технологию и форматы обмена данными.

## Требования к микросервису

1. Получение запроса на формирование дайджеста: Микросервис должен уметь принимать запросы от основного приложения на формирование дайджеста для пользователя, идентифицируемого по уникальному ID.

2. Определение подписок пользователя: После получения запроса, микросервис должен определить источники, на которые подписан пользователь, используя информацию о подписках пользователя.

3. Сбор постов из подписок: Зная подписки пользователя, микросервис должен собирать посты из этих источников. Подумайте о нём как о "сканере" подписок пользователя в поисках нового контента.

4. Фильтрация постов: Из собранных постов отфильтруйте те, которые не соответствуют интересам пользователя или недостаточно популярны. Микросервис должен использовать определенные критерии для фильтрации.

5. Создание дайджеста: После фильтрации, оставшиеся посты упаковываются в дайджест. Дайджест * это совокупность постов, отобранных для пользователя.

6. Отправка дайджеста: Сформированный дайджест возвращается в главное приложение, которое предоставит его пользователю.

## Структура данных

* Модель User: Хранит данные о пользователе, включая ID и имя.
* Модель Subscription: Содержит информацию о подписках пользователя, включая ID подписки, название источника и ID пользователя.
* Модель Post: Включает информацию о постах из подписок пользователя, включая ID поста, ID подписки, содержание поста и популярность.
* Модель Digest: Содержит информацию о сформированном дайджесте, включая ID дайджеста, список постов и ID пользователя.

## Дополнительные требования (по желанию)

* Использование Docker для создания контейнеризованного микросервиса.
* Использование SQLAlchemy для взаимодействия с базой данных.
* Использование RabbitMQ для асинхронной обработки запросов на формирование дайджеста.
* Написание автоматических тестов для проверки функциональности микросервиса.

## Критерии оценки

* Работоспособность микросервиса.
* Качество кода (организованность, чистота, следование стандартам).
* Соответствие функциональным требованиям.
* Реализация дополнительных требований (если выбраны).

Удачи в выполнении задания!
P.S. Все непонятные моменты интерпретируйте по своему усмотрению.
P.P.S. Спросили про сроки, это задание реально сделать за 2 дня. По факту у нас вышло около 80 строчек без моделей в бд, но, опять таки. Задание на джуниор разработчика, поэтому вы можете выкручиваться или сделать упрощенную версию от этой. Все обсуждаемо, можно даже обсудить сроки, если они будут аргументированы, но давайте в любом случае уважать время друг друга!
P.P.P.S. Вопросы задавать можно.

## Описание

Дайджесты контента на основе подписок, представляет собой выборку постов из различных источников. Выборка производится по подпискам и популярности контента.  
Базу наполняем из этого источника <https://newsapi.org/>  

## Технологии

* Python 3.11
* Docker
* Flask==2.3.2
* Flask-SQLAlchemy==3.0.5
* requests==2.31.0
* loguru==0.7.0
* python-dotenv==1.0.0
* gunicorn==21.2.0
* SQLite
* Makefile
* Black
* Isort

## Запуск

* У вас есть docker, открываем терминал и выполняем:

```zsh
docker run --name flask_test_app -it -p 5000:5000 dimabaril/flask_app
```

* Далее идём по этим ссылкам (цифра в конца адреса это user id, в базе их 5шт., соотв. от 1 до 5 можно играться):  
[http://127.0.0.1:5000/human_readable_digest/3 (человекочитаемый источник)](http://127.0.0.1:5000/human_readable_digest/3)  
[http://127.0.0.1:5000/json_digest/3 (здесь json)](http://127.0.0.1:5000/json_digest/3)  
[http://127.0.0.1:5000/3 (эта ссылка редиректит на json)](http://127.0.0.1:5000/3)  

## Установка

* Далее если хочется поиграться.
* Клонируйте репозиторий и перейдити в него:

```zsh
git clone git@github.com:dimabaril/flask_app.git
cd flask_app
```

* Если хотите понаполнять базу то идём на <https://newsapi.org>, регистрируемся и где то здесь <https://newsapi.org/account> получаем API key (если вам лень регаться то я залил базу на гит ;)
* Создайте файл .env и положите туда ваш API key таки образом

```.env
NEWSAPI_KEY="ваш_апи_кей_с_сайта_newsapi.org"
```

* Для заполнения БД выполните в терминале (сервис созвонится и всё обновит). Праметры запроса вшиты в сервис и они такие:
(выбираем всё) "q": "*", (с даты) "from": "2023-07-21", (сортируем по популярности) "sortBy": "popularity".

```zsh
python populate_database.py
либо
make dbp
```

## Запуск без докеров

```zsh
flask  run
либо
make fr
либо
gunicorn -w 4 -b 0:5000 app:app
либо
make frg
```

в этом месте работают все ссылки которые даны [здесь](#запуск)

## Запуск докером

Собрать образ

```zsh
docker build --tag <имя_образа> .
либо
make build
```

Запустить контейнер

```zsh
docker run --name <имя_контейнера> -it -p 5000:5000 <имя_образа>
либо
make run
```

в этом месте работают все ссылки которые даны в [здесь](#запуск)

```zsh
остановить контейнер:
    make stop
удалить контейнер:
    make rm
удалить образ:
    make rmi
остановить и удалить контейнер и образ:
    make kill
```

## Ограничения

* Апишка отдаёт порезанный контент, всего 200 символов.

## Заключение

Прошу не судить очень строго это моё знакомство с Flask и SQLAlchemy. Это не было лёгкой прогулкой, прям вот совсем, но это было интересно.

## Автор

* Я
