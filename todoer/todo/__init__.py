# archivo __init__.py que python tomara como modulo

# importamos la libreria os para poder acceder a las variables de entorno y otras cosas del sistema operativo
import os

# luego debemos  importar Flask
from flask import Flask

# creamos una funcion que nos permitira hacer testing y/o crear varias instancias de nuestra aplicacion
def create_app():
    # definimos una constante de app
    app = Flask(__name__)
    
    # utilizamos las variables de entorno para configurar la aplicacion
    app.config.from_mapping(
        # llave para definir las seciones en la aplicacion (cookie que enviamos al usuario)
        SECRET_KEY='mikey',
        # definimos los datos de conexion de la db que estaremos utilizando
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )
    
    # importamos el archivo de db
    from . import db
    
    db.init_app(app)
    
    # suscribimos y/o importamos los blueprints
    from . import auth
    from . import todo
    
    # registramos los blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    
    
    # creamos una ruta de pruebas
    @app.route('/hola')
    def hola():
        return 'Ruta de prueba'
    
    return app

