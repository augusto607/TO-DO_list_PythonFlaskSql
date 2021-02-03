# archivo db.py para configurar los datos de la db

# importamos el conector de la base de datos
import mysql.connector

# importamos una herramienta llamada click que nos permitira ejecutar comandos en la terminal
import click

# importamos desde flask current_app que mantiene la aplicacion que estamos ejecutando y g que
#es una variable que se encuentra en toda la aplicacion y le podemos asignar otras variables.
from flask import current_app, g

# importamos with_appcontext para que nos de el contexto de la conf de nuestra aplicacion
from flask.cli import with_appcontext

# luego desde nuestro script schema importamos las instrucciones
from .schema import instructions

# definimos una funcion que nos permita obtener la db y el cursor dentro de nuestra app
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
        )
        
        # configuramos el cursor
        g.c = g.db.cursor(dictionary=True)
        
    # retornamos la base de datos y el cursor 
    return g.db, g.c

# definimos una funcion para cerrar la conexion de la db
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# definimos la funcion de init_db
def init_db():
    #importamos la db y el cursor desde la funcion get_db
    db, c = get_db()
    
    # creamos un ciclo para iterar todas las instrucciones definidas en nuestro script .schema
    for i in instructions:
        c.execute(i)
    
    db.commit()
    
# funcion que llama a la logica que contiene el scripts de base de datos
#primero indicamos la configuracion necesaria para que se ejecute en la terminal (con el comando flask init-db)
@click.command('init-db')
#ahora indicamos que utilice el contexto de la aplicacion para que pueda acceder a las variables de configuracion definidas
@with_appcontext
#finalmente definimos la funcion
def init_db_command():
    init_db()
    click.echo('Base de Datos inicializada!...')
        
# definimos una funcion donde pasaremos el argumento de app para decirle que funcion debe ejecutar
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)