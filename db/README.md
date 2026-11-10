# PostgreSQL

Esta guía cubre únicamente la preparación de PostgreSQL y la administración de
usuarios y permisos. Para instalar el proyecto y configurar las dependencias y el
archivo `.env`, sigue primero el [README principal](../README.md).

## Preparación de la base de datos

1. Crear la base de datos de PostgreSQL que configuraste en el archivo `.env`.
2. Desde la raíz del proyecto, aplicar las migraciones:

   ```bash
   python manage.py migrate
   ```

3. Crear un superusuario para administrar el sitio y realizar pruebas:

   ```bash
   python manage.py createsuperuser
   ```

## Roles y permisos

Las operaciones del sistema se autorizan con permisos de Django. Un usuario administrador
puede crear grupos, asignarles los permisos correspondientes y asociar usuarios a esos
grupos desde `/admin/` (secciones **Groups** y **Users**). Ser `is_staff` por sí solo no
habilita las funciones de negocio;
los superusuarios conservan el acceso completo propio de Django.

Permisos sugeridos para configurar los roles del proyecto:

- **Gestión de stands:** `stands.view_stand`, `stands.add_stand`, `stands.change_stand`,
  `stands.assign_stand` y `stands.release_stand`.
- **Evaluación de solicitudes:** `artesanos.view_postulanteartesano`,
  `artesanos.change_postulanteartesano`, `artesanos.add_artesano` y
  `stands.assign_stand` para aprobar; el permiso `change_postulanteartesano` habilita
  el rechazo.
- **Artesano:** `productos.view_producto`, `productos.add_producto`,
  `productos.change_producto` y `productos.delete_producto`. El usuario también debe
  tener un perfil de artesano.
- **Reportes:** `artesanos.view_reports`.

Las cuentas de artesano creadas al aprobar una solicitud requieren que un administrador
les asigne el grupo/rol correspondiente desde **Users** para habilitar la gestión del
catálogo.