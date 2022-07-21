# *Asyncio*

***Получение персонажей вселенных "Здездных воин" из API [SWAPI](https://swapi.dev/api/) и загрузка их в БД Postgresql.***

### *Запуск проекта*:
* *создать виртуальное окружение. в корне проекта ввести команду `python3 -m venv venv`*
* *активировать виртуальное окружение командой `source venv/bin/activate`*
* *установить зависимости `pip install -r requirements.txt`*
* *создать .env файл и занести в него переменные окружения:*
    * *POSTGRES_PASSWORD=password*
    * *POSTGRES_USER=username*
    * *POSTGRES_DB=dbname*
    * *PG_DSN_APG =postgresql+asyncpg://username:password@localhost/dbname*
    * *PG_DSN=postgresql://username:password@localhost/dbname*
* *поднять базу данных: `docker-compose up`*
* *создать миграции `python create_table.py`*
* *внести записи из API в БД `python insert_to_db.py`*
* *получить записи из БД `python fetch_from_db.py`*
