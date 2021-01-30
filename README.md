# UP Revendas

API de sistema para loja de veículos

[![Blog Badge](https://img.shields.io/badge/Cookiecutter%20Django-black?label=built%20with&style=flat&logo=Django&color=12100e)](https://github.com/pydanny/cookiecutter-django/)



| License       | [MIT](https://github.com/MikaelSantilio/proffy-api/blob/master/LICENSE)           |
| ------------- |:-------------:|


Video demonstrativo 🎞️: https://www.youtube.com/watch?v=iAdb1s6fVd8

Online 🌐: https://uprevendas-api.herokuapp.com/api/

Requests Insominia: link

## Descrição

A API representa um sistema de loja de veículos. As principais entidades são: Carro, Conta bancária, Compra e Venda. As classes de usuários cadastrados no sistema são: Cliente, Funcionário e Gerente. 

Uma compra só pode ser realizada por um usuário Gerente

Para o registro de uma compra é necessário um Fornecedor (Que precisa ser um usuário Cliente), um Comprador (Que precisa ser um usuário Gerente), os dados válidos de um carro, o valor da compra e uma conta bancária com saldo suficiente.

Uma venda só pode ser realizada por um usuário Gerente ou usuário Funcionário

Para o registro de uma Venda é necessário um Vendedor (Que pode ser um usuário Gerente ou Funcionário), um carro disponível no estoque, uma conta bancária, o valor da venda e um Cliente com saldo suficiente.

##  Detalhamento

### HATEOAS

**api/carros/**

Na listagem de carros, se o usuário estiver autenticado e for Gerente os links mostrados
serão de detalhes, edição e exclusão do carro. Senão apenas o link de detalhes será mostrado.

```json
{
    "id": 2,
    "brand": "Fiat",
    "model": "Toro",
    "version": "1.8 16V EVO FLEX ENDURANCE AT6",
    "min_sale_value": 89890.0,
    "links": [
    {
        "type": "GET",
        "rel": "self",
        "uri": "https://uprevendas-api.herokuapp.com/api/carros/2/"
    },
    {
        "type": "GET",
        "rel": "carro_atualizacao",
        "uri": "https://uprevendas-api.herokuapp.com/api/carros/2/"
    },
    {
        "type": "DELETE",
        "rel": "carro_exclusao",
        "uri": "https://uprevendas-api.herokuapp.com/api/carros/2/"
    }
    ]
}
```

**api/contas-bancarias/**

Na listagem de contas bancárias, se o usuário estiver autenticado e for Funcionário os links mostrados
serão de detalhes e de relacionamentos com vendas e com compras. Se for Gerente serão mostrados
além dos links do Funcionário os links de atualização e exclusão da conta bancária.


```json
{
    "id": 1,
    "bank": "Banco do Brasil",
    "balance": 503121.5,
    "links": [
    {
        "type": "GET",
        "rel": "self",
        "uri": "https://uprevendas-api.herokuapp.com/api/contas-bancarias/1/"
    },
    {
        "type": "GET",
        "rel": "conta_compras",
        "uri": "https://uprevendas-api.herokuapp.com/api/comprar/?bank_account=1"
    },
    {
        "type": "GET",
        "rel": "conta_vendas",
        "uri": "https://uprevendas-api.herokuapp.com/api/vender/?bank_account=1"
    },
    {
        "type": "PUT",
        "rel": "conta_atualizacao",
        "uri": "https://uprevendas-api.herokuapp.com/api/contas-bancarias/1/"
    },
    {
        "type": "DELETE",
        "rel": "conta_exclusao",
        "uri": "https://uprevendas-api.herokuapp.com/api/contas-bancarias/1/"
    }
    ]
}
```

**api/perfil/**

Na listagem de usuários, se o usuário que fez a request estiver autenticado e for Funcionário
ou Gerente será mostrado os links de acordo com cada objeto da lista. Se o objeto da lista for
Gerente será mostrado os links para a listagem das compras e para listagem das vendas dele. 

Se for Funcionário será mostrado o link para a listagem das vendas dele. 

Se for um objeto Cliente será  mostrado o link para as compras e vendas que o objeto ele estava envolvido.

```json
{
    "id": 10,
    "username": "adriana.sabrina",
    "email": "adriana.sabrina@gmail.com",
    "is_employee": false,
    "is_customer": true,
    "is_store_manager": false,
    "links": [
    {
        "type": "GET",
        "rel": "cliente_compras",
        "uri": "https://uprevendas-api.herokuapp.com/api/comprar/?provider=10"
    },
    {
        "type": "GET",
        "rel": "cliente_vendas",
        "uri": "https://uprevendas-api.herokuapp.com/api/vender/?customer=10"
    }
    ]
}
```


**api/compra/**

Na listagem de compras, se o usuário estiver autenticado e for Funcionário ou Gerente será mostrado o link de detalhes da compra.

```json
{
    "created_at": "2021-01-28T21:11:07.838353-03:00",
    "value": 260000.0,
    "links": [
    {
        "type": "GET",
        "rel": "self",
        "uri": "https://uprevendas-api.herokuapp.com/api/comprar/1/"
    }
    ]
}
```

**api/venda/**

Na listagem de vendas, se o usuário estiver autenticado e for Funcionário ou Gerente será mostrado o link de detalhes da venda.

```json
{
    "created_at": "2021-01-28T21:40:23.624668-03:00",
    "value": 30000.0,
    "links": [
    {
        "type": "GET",
        "rel": "self",
        "uri": "https://uprevendas-api.herokuapp.com/api/vender/1/"
    }
    ]
}
```


### Permissões

**api/carros**

A listagem de carros é pública assim como a listagem de marcas (carros/marcas), modelos(carros/modelos) e caracteristicas pre-definidas(carros/choices) dos carros a fim da utilização em filtros e formulários.

A criação de marcas e modelos é permitida apenas a usuários do tipo Funcionário ou Gerente e a criação
de carros diretamente por essa rota está permitida apenas ao Gerente.

**api/contas-bancarias**

A listagem de contas bancárias é permitida apenas a usuários do tipo Funcionário ou Gerente. A criação, edição e exclusão de contas está permitida apenas ao Gerente.

**api/compra**

A listagem de compras é permitida apenas a usuários do tipo Funcionário ou Gerente. O registro de compras está permitida apenas ao Gerente.

**api/venda**

A listagem e registro de vendas é permitida apenas a usuários do tipo Funcionário ou Gerente.


### Filtro e ordenação

#### api/carros

Os filtros disponíveis para listagem de carros são:
**'brand', 'model', 'car_type', 'color' e 'transmission'**

As ordenaçoes disponíveis para listagem de carros são:
**'min_sale_value', 'mileage', 'year' e 'version'**

#### api/contas-bancarias

O filtro disponíveil para listagem de contas é: 
**'bank'**

A ordenação disponível para listagem de contas é:
**'balance'**

#### api/compra

Os filtros disponíveis para listagem de compras são:
**'provider', 'car', 'buyer_for' e 'bank_account'**

As ordenaçoes disponíveis para listagem de compras são:
**'value', 'created_at' e 'updated_at'**

#### api/venda

Os filtros disponíveis para listagem de vendas são:
**'customer', 'car', 'seller' e 'bank_account'**

As ordenaçoes disponíveis para listagem de vendas são:
**'value', 'created_at' e 'updated_at'**

#### api/perfil

Os filtros disponíveis para listagem de usuários são:
**'is_employee', 'is_customer', 'is_store_manager' e 'is_seller'**


### Autenticação

Utilizado JWT através da biblioteca [Simple JWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt)

### Paginação e Throttling

A paginição na listagem de objetos foi definida como 5 por página.

A limitação de request para usuários não autenticados é de 100 por dia e para
usuários autenticados é de 1000 por dia.

### Documentação

A documentação utilizada é Swagger, disponível no link:
https://uprevendas-api.herokuapp.com/api/swagger/


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

## Autor

| [<img src="https://avatars1.githubusercontent.com/u/40041499?s=460&u=b484cfea7185c43f1a07cc8ba3a75a82cdc20b27&v=4" width=100><br><sub>@MikaelSantilio</sub>](https://github.com/MikaelSantilio) |
| :---: |
