# archivo schema.py que contiene las consultas sql

# el script lo escribimos en forma de lista
instructions = [
    # primero desactivamos la validacion que nos impide borrar tablas con llaves foraneas
    'SET FOREIGN_KEY_CHECKS=0;',
    
    # eliminamos las tablas todo y user si es que existen
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS user;',
    
    # activamos nuevamente la validacion de eliminacion de tablas con llaves foraneas
    'SET FOREIGN_KEY_CHECKS=1;',
    
    # creacion de la tabla user
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """,
    
    # creacion de la tabla todo
    """
        CREATE TABLE todo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (created_by) REFERENCES user (id)
        )
    """
]