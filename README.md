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

- **Backend:** Framework Django (Versión X.X).
- **Base de Datos:** PostgreSQL (Versión X.X).
- **Frontend:** HTML5, CSS3, JavaScript y Bootstrap.
- _Para ver el listado completo de dependencias y versiones, consultar el archivo `requirements.txt`._

## Requisitos Previos

- Python 3.x instalado.
- PostgreSQL instalado y en ejecución.
- Git.

## Formas de Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/wusito/poncho-digital.git
cd poncho-digital
```

### Roles y permisos

Las operaciones del sistema se autorizan con permisos de Django. Después de ejecutar
`python manage.py migrate`, un usuario administrador puede crear grupos, asignarles los
permisos correspondientes y asociar usuarios a esos grupos desde `/admin/` (secciones
**Groups** y **Users**). Ser `is_staff` por sí solo no habilita las funciones de negocio;
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
