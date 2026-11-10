# poncho-digital

## Descripción del Proyecto:

"Poncho Digital" es un prototipo de aplicación web desarrollado para el Ministerio de Cultura de la Provincia. Su objetivo es brindar información actualizada sobre los artesanos y productores de la feria artesanal de la Fiesta Nacional e Internacional del Poncho. El sistema permite la gestión de stands, el registro de artesanos, la publicación de productos y la visualización de un mapa de la feria para mejorar la experiencia de los visitantes.

## Integrantes del Equipo:

De acuerdo con las pautas establecidas para la conformación de equipos, los integrantes del presente proyecto son:

- **[Bordón Guanco, Airton Joel]** - M.U.N°: [02010]
- **[Rios Ruiz, Lourdes Florencia]** - M.U.N°: [01658]
- **[Sedan Caniza , Franco Mariano]** - M.U.N°: [01930]
- **[Wu Sosa, Marcelo Exequiel]** - M.U.N°: [01555]

## Tecnologías y Librerías (Stack Tecnológico)

- **Backend:** Framework Django (Versión 6.1).
- **Base de Datos:** PostgreSQL (Versión 18.6).
- **Frontend:** HTML5, CSS3, JavaScript y Bootstrap.

## Requisitos Previos

- Python 3.14.0 instalado.
- PostgreSQL instalado y en ejecución.
- Git.

## Formas de Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/wusito/poncho-digital.git
cd poncho-digital
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv poncho-digital
```

Actívalo según la terminal usada:

```powershell
# Windows (PowerShell)
poncho-digital\Scripts\activate
```

```bash
# macOS/Linux
source poncho-digital/bin/activate
```

### 3. Instalar Django y las dependencias

Con el entorno virtual activado, ejecutar:

```bash
pip install django psycopg2-binary
pip install python-dotenv
pip install Pillow
pip install openpyxl
```

### 4. Configurar el archivo `.env`

Crear un archivo `.env` en la raíz del proyecto con los datos de conexión a
PostgreSQL:

```env
DB_NAME=nombre_de_la_base
DB_USER=usuario_de_postgres
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
```

Reemplazar los valores de ejemplo por los de tu instalación.

### 5. Preparar la base de datos

Para crear la base de datos, aplicar las migraciones, crear un usuario administrador
y configurar roles y permisos, sigue la [guía de PostgreSQL](./db/README.md).

### 6. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```
