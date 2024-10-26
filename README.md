## how to build
для того, что бы собрать и запустить этот сервис необходим docker engine и docker compose

### 1. необходимо клонировать этот репозиторий:
git clone https://github.com/Grivvus/semantic_analyse_service.git

### 2. заходим в папку проекта
cd semantic_analyse_service

### 3. собираем и запускаем контейнеры:
#### a) docker-compose -f compose_build.yaml up --build
лучший вариант, собирать контейнер с сервисом из Dockerfile'а, который лежит в проекте
#### б) docker-compose up --build
можно скачать собранное изображения контейнера из docker hub'а
