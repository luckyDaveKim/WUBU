python manage.py makemigrations --settings=wubuProject.settings.settings_local
python manage.py migrate --settings=wubuProject.settings.settings_local
python manage.py runserver --settings=wubuProject.settings.settings_local

python manage.py inspectdb  --settings=wubuProject.settings.settings_local

python3 manage.py shell --settings = 프로젝트 폴더.settings.사용할 파일명
