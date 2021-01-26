# UP Revendas

A system for vehicle stores

[![Blog Badge](https://img.shields.io/badge/Cookiecutter%20Django-black?label=built%20with&style=flat&logo=Django&color=12100e)](https://github.com/pydanny/cookiecutter-django/)



| License       | [MIT](https://github.com/MikaelSantilio/proffy-api/blob/master/LICENSE)           |
| ------------- |:-------------:|

## Descrição



Video demonstrativo: link

Online 🌐: https://uprevendas-api.herokuapp.com/api/

## Configurações em Ambiente Local

### Pré-requisitos
Para rodar este projeto no modo de desenvolvimento, você vai precisar de um ambiente com Python 3.8.x
instalado. Para usar o banco de dados, você vai precisar ter o PostgreSQL instalado ou rodando em um container.

### Instalação
1. Clone o repositório e entre na pasta:
```shell
$ git clone https://github.com/MikaelSantilio/uprevendas-api

$ cd uprevendas-api 
```

2. Crie um ambiente virtual:
```shell
$ python3.8 -m venv <virtual env path>
```

3. Ative o ambiente virtual que você acabou de criar:
```shell
$ source <virtual env path>/bin/activate
```

4. Instale os pacotes de desenvolvimento local:
```shell
$ pip install -r requirements/local.txt
```

5. Defina as variáveis de ambiente a seguir:
```shell
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=127.0.0.1,0.0.0.0

export POSTGRES_HOST=<POSTGRES_HOST>
export POSTGRES_PORT=<POSTGRES_PORT>
export POSTGRES_DB=<DB_NAME>
export POSTGRES_USER=<POSTGRES_USER>
export POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
```
> **Para ajudar com as configurações das variáveis de ambiente, você tem algumas opções**:
> - Crie um arquivo `.env` na raíz do seu projeto e defina todas as variáveis necessárias dentro dele. Então você so precisa ter `DJANGO_READ_DOT_ENV_FILE=True` em sua máquina e todas as variáveis serão lidas.
> - Use um gerenciador de ambientes como o [direnv](https://direnv.net/)

6. Execute as migrações:
```shell
$ python manage.py migrate
```

7. Rode o servidor de desenvolvimento:
```shell
$ python manage.py runserver 0.0.0.0:8000
```

> Mais em: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html

## Author

| [<img src="https://avatars1.githubusercontent.com/u/40041499?s=460&u=b484cfea7185c43f1a07cc8ba3a75a82cdc20b27&v=4" width=100><br><sub>@MikaelSantilio</sub>](https://github.com/MikaelSantilio) |
| :---: |
