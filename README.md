# UP Revendas

A system for vehicle stores

[![Blog Badge](https://img.shields.io/badge/Cookiecutter%20Django-black?label=built%20with&style=flat&logo=Django&color=12100e)](https://github.com/pydanny/cookiecutter-django/)



| License       | [MIT](https://github.com/MikaelSantilio/proffy-api/blob/master/LICENSE)           |
| ------------- |:-------------:|

This is the back-end of the Proffy application.

It's a RESTful API built with Django + PostgreSQL that 
provide the teachers data to the client server.

Online 🌐: https://proffyapi.herokuapp.com/


## Available endpoints


| Method     | Endpoint            | Request                                             | Response                                 |
| ---------- | ------------------- | --------------------------------------------------- | ---------------------------------------- |
| **`GET`**  | `/api/connections/` | **No Body**                                           | `HTTP_200_OK`<br>**JSON Response**<ul><li>total: `number`</li> </ul> |
| **`POST`** | `/api/connections/` | **JSON Required Fields**<ul><li>proffy_user: `number`</li> </ul>                               | `HTTP_200_OK`<br>**JSON Response**<ul><li>proffy_user: `number`</li> </ul>                                                                                                                                                                                                                               |
| **`GET`**  | `/api/classes/`     | **GET parameters**<ul> <li>subject: `string`</li> <li>week_day: `number`</li><li>time: `string`</li></ul>| `HTTP_200_OK`<br>**JSON Response**<ul><li>`Array`<ul><li>subject: `string`</li><li>cost: `string`</li><li>proffy_user: </li><ul><li>name: `string`</li><li>avatar: `string`</li><li>bio: `string`</li><li>whatsapp: `string`</li></ul></ul></li> </ul>|
| **`POST`** | `/api/classes/`     | **JSON Required Fields**<ul><li>name: `string`</li><li>avatar: `string`</li><li>whatsapp: `string`</li><li>bio: `string`</li><li>subject: `string`</li><li>cost: `number`</li><li>schedule: `Array`<ul><li>week_day: `number`</li><li>start_at: `string`</li><li>end_at: `string`</li></ul></li> </ul>| `HTTP_200_OK`                                                                                     |

## Getting Started

### Prerequisites
To run this project in the development mode, you'll need to have a basic environment with Python 3.8.x installed. To use the database, you'll need to have PostgreSQL installed or running on a container.

### Installing
1. Clone the repository and enter:
```shell
$ git clone https://github.com/MikaelSantilio/proffy-api/

$ cd proffy-api 
```

2. Create a virtualenv:
```shell
$ python3.8 -m venv <virtual env path>
```

3. Activate the virtualenv you have just created:
```shell
$ source <virtual env path>/bin/activate
```

4. Install development requirements:
```shell
$ pip install -r requirements/local.txt
```

5. Set the environment variables:
```shell
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=127.0.0.1,0.0.0.0
export CORS_ORIGIN_WHITELIST=127.0.0.1:3000

export POSTGRES_HOST=<POSTGRES_HOST>
export POSTGRES_PORT=<POSTGRES_PORT>
export POSTGRES_DB=<DB_NAME>
export POSTGRES_USER=<POSTGRES_USER>
export POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
```
> **To help setting up your environment variables, you have a few options**:
> - create an `.env` file in the root of your project and define all the variables you need in it. Then you just need to have `DJANGO_READ_DOT_ENV_FILE=True` in your machine and all the variables will be read.
> - Use a local environment manager like [direnv](https://direnv.net/)

6. Apply migrations:
```shell
$ python manage.py migrate
```

7. Run the development server:
```shell
$ python manage.py runserver 0.0.0.0:8000
```

> More in: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html

## Author

| [<img src="https://avatars1.githubusercontent.com/u/40041499?s=460&u=b484cfea7185c43f1a07cc8ba3a75a82cdc20b27&v=4" width=100><br><sub>@MikaelSantilio</sub>](https://github.com/MikaelSantilio) |
| :---: |

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy up_revendas

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html




Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use `MailHog`_ when generating the project a local SMTP server with a web interface will be available.

#. `Download the latest MailHog release`_ for your OS.

#. Rename the build to ``MailHog``.

#. Copy the file to the project root.

#. Make it executable: ::

    $ chmod +x MailHog

#. Spin up another terminal window and start it there: ::

    ./MailHog

#. Check out `<http://127.0.0.1:8025/>`_ to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

.. _`Download the latest MailHog release`: https://github.com/mailhog/MailHog/releases

.. _mailhog: https://github.com/mailhog/MailHog



Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html




