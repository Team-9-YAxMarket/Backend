# Yandex Hackathon Team 9

## Состав команды Backend разработки

 - Марк Крылов
 - Иван Резниченко

## Краткое описание Архитектуры проекта
Проект построен по сервисной архитектуре (Service-based architecture style) —
набор сервисов с общей базой данных.

Каждый сервис построен по трёхуровневой архитектуре (layered architecture style)
и состоит из: 
1. слой представления (директория `/api`): получение и валидация данных,
   преобразование форматов при формировании ответов.
2. слой бизнес-логики (директория `/service`): отвечает за исполнения требований, 
   диктуемых заказчиком, для получения/сохранения данных использует слой данных.
3. слой данных (директория `/repository`): отвечает за получение/сохранение данных
   в базе данных или сторонних сервисах

В проекте у нас есть следующие сервисы:

#### ordering_service
Сервис, отвечающий за прием информации о заказе, обогащение данных о товарах из базы
данных склада, запрос в сервис ml модели и передачу в сервис формирования заказа полной
информации о заказе и рекомендуемой упаковке.

Сервис предоставляет следующий endpoint:
 - `POST /order/`- принимает список sku (товаров) и их количество в заказе.
   **Это основная точка входа**.

#### packing_service
Сервис, отвечающий за бизнес-процесс работы пользователя (упаковщика).

Сервис предоставляет следующие endpoint-ы:
- `POST /order/` — создание заказа (используется сервисом _ordering_service_)
- `PATCH /order/{order_id}` — обновления информации о заказе (используется сервисом _ordering_service_)
- `GET /carton/` — информация о названии и штрих-коде упаковки (используется frontend-ом)
- `POST /session/` — создания сессии работы пользователя (используется frontend-ом)
- `PATCH /session/` — закрытие сессии работы пользователя (используется frontend-ом)

#### warehouse_service
Сервис отвечающий за базу данных склада. Это имитация (mock) сервисов Яндекса.

Сервис предоставляет следующие endpoint-ы:
- `GET /check_skus` — получение информации о характеристиках товаров (sku)
- `GET /check_skus/status`— получение информации о наличии товаров (sku) на складе
- `GET /check_carton` — получение информации о характеристиках и наличии упаковки
  на складе
	
## Инструкция по запуску проекта
```bash
git clone https://github.com/Team-9-YAxMarket/backend/
cd backend
docker compose --file infra-hackathon/docker-compose.yml up --detach --remove-orphans
```

#### Переменные окружения
Для работы приложения необходимы следующие переменные окружения
(необходимо создать файл `.env` в директории `infra-hackathon`)
```dotenv
# Общие настройки
DB_HOST=db      # имя хоста (контейнера) базы данных
DB_PORT=5432    # порт, на которм работает база данных
# Настройки контейнера базы данных
POSTGRES_DB=postgres        # имя базы данных по умолчанию
POSTGRES_USER=postgres      # имя суперпользователя postgres
POSTGRES_PASSWORD=postgres  # пароль суперпользователя
# Настройки, общие для всех контейнеров приложений
DEBUG=False
ROOT_PATH=/api/v1/      # также используется в конфигурационном файле nginx
# Настройки приложения packing-service
PACKING_ROOT_PATH=${ROOT_PATH}                  # root_path
PACKING_APP_DB_NAME=packing                     # имя базы данных сервиса
PACKING_APP_DB_USER=packing_user                # имя пользователя БД сервиса
PACKING_APP_DB_PASSWORD='Very$ecretPassw0rd'    # Пароль пользователя БД
# Настройки приложения ml-model-service
ML_ROOT_PATH=${ROOT_PATH}                  # root_path
# Настройки приложения warehouse-service
WAREHOUSE_ROOT_PATH=${ROOT_PATH}                # root_path
WAREHOUSE_APP_DB_NAME=warehouse                 # имя базы данных сервиса
WAREHOUSE_APP_DB_USER=warehouse_user            # имя пользователя БД сервиса
WAREHOUSE_APP_DB_PASSWORD='Very$ecretPassw0rd'  # Пароль пользователя БД
```

## Стек технологий, использованных в проекте
* python 3.10
* httpx
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