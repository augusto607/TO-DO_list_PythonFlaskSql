# TO-DO List with Python and Flask framework

###### Is important to have knowledge about MySQL, Flask, Python and HTML for replicate this project
##  Instructions for help to replicated or deploy this project

1. Install and configuring virtual enviroment:
   - create a virtualenv with the name: venv
   - create a project with the name: todo
  
<br />

2. Install in the virtual env(this list is in the file requirements.txt):
   - click = 7.1.2
   - Flask = 1.1.2
   - itsdangerous = 1.1.0
   - Jinja2 = 2.11.2
   - MarkupSafe = 1.1.1
   - mysql-connector-python = 8.0.22
   - pip = 20.2.3
   - protobuf = 3.14.0
   - setuptools = 49.2.1
   - six = 1.15.0
   - Werkzeug = 1.0.1

<br />

3. For this project you need install and conf a MySQL database:
   - After, in your operating system you should config the followings variables of environment:
        - export FLASK_DATABASE_HOST='localhost'
        - export FLASK_DATABASE_PASSWORD='key_of_your_db_user'
        - export FLASK_DATABASE_USER='your_db_user'
        - export FLASK_DATABASE='name_of_db_created'

<br />

4. Define the variable of environment for FLASK_APP:
    - export FLASK_APP=todo

<br />

5. Configure the variable of environment for run flask in develop mode:
   - export FLASK_ENV=development

<br />

#### In this point you could replicate this project in your local environment, considering your previous knowledge about Python, MySQL, Flask and HTML