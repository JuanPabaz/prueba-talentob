# Prueba Talento B - Juan Pablo Giraldo Tamayo
Reto tecnico con Django, PostgreSQL para Talento B 
# Uso del proyecto
Sigue estos comandos para instalar y ejecutar el proyecto:

```bash
# Clona el repositorio
git clone https://github.com/JuanPabaz/prueba-talentob.git

# Entra al directorio del proyecto
cd prueba-talentob

# Crea un entorno virtual
python -m venv venv

# Activa el entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instala las dependencias
pip install -r requirements.txt

# Entra a auditoria
cd auditoria
```
### Crea un archivo .env
```python
SECRET_KEY="Llave secreta"
DEBUG=True
DB_NAME={Nombre base de datos}
DB_USER={Usuario base de datos}
DB_PASSWORD={Contraseña base de datos}
DB_HOST={Host base de datos}
DB_PORT={Puerto base de datos}
```
```bash
# Ejecuta las migraciones
python manage.py migrate

# Ejecuta el dump de datos
python manage.py loaddata data_dump.json 
#Asegurate que el encoding del JSON sea UTF-8 para que funcione el load de los datos


# Ejecuta el servidor de desarrollo
python manage.py runserver
```
### Crea un super usuario (admin)
```bash
python manage.py createsuperuser
```
# Diagrama ER
![Diagrama](Diagrama_Talento_B.jpg)

# Inicio de sesion en la aplicacion
Para iniciar sesion en la aplicacion hay que crear un usuario en el panel de administrador iniciando sesion con el super usuario creado, en esta direccion:

http://127.0.0.1:8000/admin

Ya en el panel se deberá crear un usuario con las credenciales deseadas y despues de crear el usuario hay que crear un auditor, relacionandolo con el usuario recien creado.

Ya podras ingresar a la aplicacion con las credenciales del usuario y asi apareceran los controles asignados al auditor

# Base de datos desplegada en AWS
Para el proyecto se desplegó una instancia RDS de AWS para la base de datos en PostgreSQL, esta ya contiene unos datos de prueba de ser necesarios.
#### Url: db-auditoria.cf6g4y8okctp.us-east-1.rds.amazonaws.com
#### Usuario: postgres
#### Contraseña: pruebatalentobaws
#### Base de datos: auditoria_db
# Usuario de prueba de la base de datos AWS y para el dump de datos en local
#### Usuario: pruebatalentob
#### Contraseña: talentob2024