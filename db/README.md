# Carga de datos en PostgreSQL

## Preparación

1. Configura la conexión de Django a PostgreSQL y crea la base de datos.
2. Desde la raíz del proyecto, crea las tablas de Django ejecutando:

   ```bash
   python manage.py migrate
   ```

3. Crea el superusuario para administrar el sitio y realizar pruebas:

   ```bash
   python manage.py createsuperuser
   ```

Los archivos CSV de artesanos y postulantes pueden incluir `usuario_id`. Antes
de importarlos, verifica que existan en la tabla de usuarios las cuentas
correspondientes a esos IDs. Crear el superusuario no crea las demás cuentas
referenciadas por los CSV; el ID de cada usuario debe coincidir con el valor
indicado en el archivo; en su defecto, crear desde el adminitrador de Django los usuarios correspondientes a los artesanos registrados.

## Importación de los CSV

En pgAdmin 4, selecciona la tabla correspondiente y usa **Import/Export Data**
para importar el CSV. Habilita la opción de encabezado (*Header*) y verifica
que el delimitador sea una coma. Importa los archivos en este orden, necesario
para respetar las claves foráneas:

1. `postulantes.csv` en `artesanos_postulanteartesano`.
2. `artesanos.csv` en `artesanos_artesano`.
3. `stands.csv` en `stands_stand`.
4. `productos.csv` en `productos_producto`.

Las tablas deben estar vacías (salvo los registros de usuarios creados
previamente) o los IDs de los CSV podrían entrar en conflicto con registros
existentes. No omitas columnas del CSV, incluido `id`.

## Sincronización de IDs

Después de importar todos los archivos, abre el Query Tool de pgAdmin 4 sobre
la base de datos del proyecto y ejecuta el contenido de
[`query-restart-all-ids.sql`](./query-restart-all-ids.sql). El script ajusta
las secuencias de las columnas identity/serial al último ID cargado; si una
tabla está vacía, deja su secuencia lista para generar el ID 1.
