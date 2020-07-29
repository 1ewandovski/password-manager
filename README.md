# password-manager
backend part of course project for is497 in sjtu
# BACKEND

## install django

git clone https://github.com/django/django.git

python -m pip install -e django/

## install related

pip install django-extensions

pip install pyOpenSSL

pip install django-werkzeug-debugger-runserver

pip install django-sslserver

## how to run

http：python manage.py runserver 0.0.0.0:8000

https：python manage.py runsslserver localhost:8000 --certificate localhost.pem --key localhost-key.pem

可以使用mkcert工具生成本地自签名证书，详细使用说明见https://github.com/FiloSottile/mkcert/releases
