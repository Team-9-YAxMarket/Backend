# Yandex Hackathon Team 9

##  Backend разработчики

Крылов Марк, 
Иван Режниченко

### 
## Краткое описание структуры
Структура проекта состоит из трех сервисов, выполняющих разные задачи.
* warehouse_service - сервис отвечающий за базу данных склада.

* packing_service - сервис отвечающий за прием  полной информации о заказе от склада и  с рекомендацией об упаковке полученной от ml модели.
* ordering_service
-сервис отвечающий за прием информации о заказе, обогащение данных о товарах из базы данных склада, запрос в сервис ml модели и передачу в сервис формирования заказа полной информации о заказе и рекомендуемой упаковке :
 
	>  __`/order/`__  - эндпоинт принимающий sku товаров и их количество в заказе и отдающий обогащенную информацию для формирования заказа.
	
## Инструкция по сборке
###### 
```
git clone https://github.com/Team-9-YAxMarket/backend/
```

```
cd backend/warehouse_service
```
#### Создайте файл .env в директории warehouse_service/
```
nano .env
```
#### Добавьте переменные окружения:

```
WAREHOUSE_APP_DB_NAME = 'Название БД склада'
WAREHOUSE_APP_DB_USER = 'Имя юзера БД склада'
WAREHOUSE_APP_DB_PASSWORD = 'Ваш пароль для пользования БД склада'
DB_HOST = 'хост для базы данных склада'
DB_PORT = 'порт для базы данных склада'
```
```
cd ..
```
```
cd /packing_service
```
#### Создайте файл .env в директории packing_service/
```
nano .env
```
#### Добавьте переменные окружения:

```
PACKING_APP_DB_NAME = 'Название БД склада'
PACKING_APP_DB_USER = 'Имя юзера БД склада'
PACKING_APP_DB_PASSWORD = 'Ваш пароль для пользования БД склада'
DB_HOST = 'хост для базы данных склада'
DB_PORT = 'порт для базы данных склада'
```
```
cd ..
```
```
cd /infra-hackathon
```



#### Запустите сборку контейнеров docker командой:
```
docker-compose up -d
```

#### Выполните миграции:

```
docker-compose exec backend/warehouse_service alembic upgrade 7a6ac8331c5a
docker-compose exec backend/packing_service alembic upgrade 7b33ed336f6e
docker-compose exec backend/packing_service alembic upgrade 7b33ed336f6e
```

## Стек технологий, использованных в проекте
* python 3.10
* fastapi
* fastapi-restful
* pydantic
* alembic
* asyncpg
* aiohttp
* uvicorn
* python-dotenv
* sqlalchemy
* PostgreSQL
## Links

[Сайт развернут по ссылке](http://ivr.sytes.net:9009/)