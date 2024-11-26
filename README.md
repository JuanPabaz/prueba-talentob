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

# Ejecuta el servidor de desarrollo
python manage.py runserver
```
### Crea un super usuario (admin)
```bash
python manage.py createsuperuser
```
# Diagrama ER
![Diagrama](Diagrama_Talento_B.jpg)

# Base de datos desplegada en AWS
Para el proyecto se desplegó una instancia RDS de AWS para la base de datos en PostgreSQL, esta ya contiene unos datos de prueba de ser necesarios.
#### Url: db-auditoria.cf6g4y8okctp.us-east-1.rds.amazonaws.com
#### Usuario: postgres
#### Contraseña: pruebatalentobaws
#### Base de datos: auditoria_db
# Usuario de prueba de la base de datos AWS
#### Usuario: pruebatalentob
#### Contraseña: talentob2024