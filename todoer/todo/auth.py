# archivo auth.py para las funciones de autenticacion

# importamos el set de funciones functools
import functools

# importaremos una serie de modulos y/o clases de flask
from flask import (
    #para crear blueprints
    Blueprint,
    #para enviar mensajes de manera generica a las plantillas
    flash,
    #para tener una variable global y guardar datos en ella
    g,
    #para renderizar plantillas
    render_template,
    #para recibir datos desde un formulario
    request,
    #para crear url
    url_for,
    #para mantener una referencia del usuario en el contexto actual interactuando con la app
    session,
    #para redireccionar
    redirect
)

# importamos el modulo de seguridad, con la opcion de verificar pass y encriptarlo
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

# importamos desde nuestro modulo de db la conexion
from todo.db import get_db


# creamos el blueprint principal de autenticacion
bp = Blueprint('auth', __name__, url_prefix='/auth')

# agregamos la ruta de register en nuestro blueprint y definimos la funcion de registro
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # validamos en el servidor si el metodo que estamos recibiendo es post
    if request.method == 'POST':
        # sacamos de nuestro formulario el nombre de usuario y la contrasenia
        username = request.form['username']
        password = request.form['password']
        
        # validamos estos datos contra la db
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s', 
            (username,)
        )
        if not username:
            error = 'Username es requerido!'
        if not password:
            error = 'Password es requerido!'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)
            
        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            
            return redirect(url_for('auth.login'))
        
        Flash(error)
        
    return render_template('auth/register.html')


# definimos la funcion de inicio de sesion
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # validamos en el servidor si el metodo que estamos recibiendo es post
    if request.method == 'POST':
        # sacamos de nuestro formulario el nombre de usuario y la contrasenia
        username = request.form['username']
        password = request.form['password']
        
        # nos conectamos para obtener la db y el cursor
        db, c = get_db()
        # definimos un mensaje de error
        error = None
        # buscar el usuario y validar la contrasenia
        c.execute(
            'select * from user where username = %s;',
            (username,)
        )
        # sacamos o tomamos este usuario validado
        user = c.fetchone()
        
        # verificamos la existencia del usuario
        if user is None:
            error = 'Usuario y/o Clave invalida!' #en el mensaje tambien colocamos que la clave puede estar mal por seguridad anti-hacker
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o Clave invalida!' #en el mensaje tambien colocamos que la clave puede estar mal por seguridad anti-hacker
            
        if error is None:
            # limpiamos la sesion
            session.clear()
            # creamos una variable dentro de la sesion para asignale el id del usuario
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
        
        # si el usuario si dio algun error enviamos el mensaje de error
        flash(error)
        
    # si recibimos un metodo get enviamos al usuario al inicio de sesion
    return render_template('auth/login.html')

# fucion decoradora para verificar y obtener el user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', 
            (user_id,)
        )
        g.user = c.fetchone()

# definimos la funcion decoradora de proteccion de los endpoints
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

# definimos la ruta y la funcion del logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))