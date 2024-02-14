
## App 추가
```shell
python manage.py startapp {app_name}
```


## DB
### makemigrations
migration 정보를 python 에 구성

#### wubuApp
```shell
python manage.py makemigrations --settings=wubuProject.settings.settings_local wubuApp
```

#### mongoDBApp
```shell
python manage.py makemigrations --settings=wubuProject.settings.settings_local mongoDBApp
```

### migrate
model 정보를 DB 에 업데이트
fake : 마이그 정상으로 된 것으로 속임

#### MariaDB
```shell
python manage.py migrate --settings=wubuProject.settings.settings_local --database=default wubuApp
```

#### MongoDB
```shell
python manage.py migrate --settings=wubuProject.settings.settings_local --database=mongodb mongoDBApp
```
- inspectdb : DB의 정보로 model 정보를 생성해서 CLI로 뿌려줌
```shell
python manage.py inspectdb --settings=wubuProject.settings.settings_local
```

## Run
```shell
python manage.py runserver --settings=wubuProject.settings.settings_local
```

## Install
```shell
python -m pip install django
python -m pip install django-cors-headers
python -m pip install django-pandas
python -m pip install djangorestframework
python -m pip install mysqlclient
python -m pip install djongo
python -m pip install mongoengine
python -m pip install pymongo==3.12.3

brew install pkg-config
brew install mysql-client

python -m pip install python-logstash
```
