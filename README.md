- dependencies
  - python: v3.11
  - conda: v24.1.2

```shell
# 가상 환경 생성
conda env create --file environment.yml

# 가상 환경 적용
conda activate wubuProject

# 가상 환경 적용 해제
conda deactivate

# 가상 환경 정보 저장
conda env export --name wubuProject > environment.yml
```


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
