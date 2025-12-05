# CRUD de Eventos Académicos - Backend

Backend API REST desarrollado con Django y Django REST Framework para el sistema de registro de usuarios de la BUAP. Permite la gestión de Administradores, Alumnos, Maestros y Eventos Académicos.

## Contenido

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)

## Características

- Sistema de autenticación de usuarios
- Registro de Administradores, Alumnos, Maestros y Eventos Académicos
- Gestión de roles y permisos con Django Groups
- API RESTful con Django REST Framework
- Base de datos MySQL
- CORS habilitado para integración con frontend
- Cifrado seguro de contraseñas con PBKDF2
- Soporte para variables de entorno

## Tecnologías

- **Django** 5.0.2
- **Django REST Framework** 3.14.0
- **MySQL** (Base de datos alojada en pythonAnywhere)
- **JWT Authentication** (Tokens de acceso)

## Requisitos Previos

Asegúrate de tener instalado:

- **Python**: 3.12 o superior
- **XAMPP**: 3.3.0. Para el despliegue local
- **pip**: Gestor de paquetes de Python
- **virtualenv** (recomendado): Para crear entornos virtuales

### Verificar instalaciones:

```cmd
python --version
mysql --version
pip --version
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/CrisF4/Registro-Usuarios-BUAP_backend.git
cd Registro-Usuarios-BUAP_backend
```

### 2. Crear y activar entorno virtual

```cmd
python -m venv backend_django
backend_django\Scripts\activate.bat
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

### 1. (LOCAL) Configurar MySQL en MyphpAdmin

Al ejecutar XAMPP, abre el panel de MyphpAdmin y crea una nueva base de datos llamada 'app_escolar_api_db' (puedes cambiar el nombre, pero requerira de modificar el archivo my.cnf).

```ini
[client]
database = nombre_base_datos
user = usuario
password = contraseña
host = localhost
port = 3306
default-character-set = utf8mb4
```

### 2. (REMOTO) Variables de entorno 

Crea un archivo `.env` en la raíz del proyecto:

```env
# Django Settings
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=tu_url_aqui.com, 127.0.0.1

# Database Configuration
DB_HOST=localhost
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_PORT=3306
```

### 3. Aplicar migraciones (LOCAL O REMOTO)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario (REMOTO)

```bash
python manage.py createsuperuser
```

## Uso

### Iniciar el servidor de desarrollo (LOCAL)

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`. Si se ejecuta en remoto (pythonAnywhere), este se iniciara automaticamente.

### Error de CORS
Agrega el dominio del frontend en `ALLOWED_HOSTS` y configura `CORS_ALLOWED_ORIGINS` en `settings.py`
