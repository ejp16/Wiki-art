# Wiki-Art

Este proyecto es una aplicación web llamada **Wiki-Art**, desarrollada con Flask, que permite a los usuarios registrarse, iniciar sesión y publicar reseñas sobre obras de arte. 

### Las principales funcionalidades incluyen

- **Registro e inicio de sesión:** Los usuarios pueden crear una cuenta y autenticarse para acceder a funciones adicionales.
- **Publicación de posts:** Los usuarios autenticados pueden crear nuevos posts sobre obras de arte, subiendo imágenes y proporcionando información como el nombre de la obra, autor, estilo, género y una reseña.
- **Búsqueda avanzada:** En la página principal, los visitantes pueden buscar obras por nombre, estilo y género, mostrando resultados filtrados dinámicamente.
- **Perfil de usuario:** Cada usuario tiene un perfil donde puede ver sus datos y los posts que ha publicado, con la opción de eliminar sus publicaciones.
- **Visualización de posts:** Cada post tiene una página dedicada donde se muestra la imagen, los datos de la obra y la reseña.
- **Validación de datos:** Los formularios están construidos con WTForms, con validaciones en todos los campos.
- **Interfaz amigable:** El sitio utiliza Bootstrap para el diseño y cuenta con mensajes de éxito y error para mejorar la experiencia del usuario.

La estructura del proyecto incluye rutas para la gestión de usuarios y posts, modelos para la base de datos, formularios validados y plantillas HTML organizadas con herencia y macros para reutilización de componentes.

### Pasos para iniciar el proyecto

#### Crear un entorno virtual en Python

    python3 -m venv env

#### Instalar Flask y otras librerías en el entorno virtual con el archivo requirements.txt 

    pip install requirements.txt

#### En el archivo app.py, cambiar la configuración según el motor de base de datos a usar

    app.config['SQLALCHEMY_DATABASE_URI'] = dialect://username:password@host:port/database

#### Con el entorno virtual activado, ejecutar el archivo index.py

    python3 index.py
