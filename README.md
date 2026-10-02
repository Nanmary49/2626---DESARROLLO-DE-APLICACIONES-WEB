# Semana 16 — Proyecto final

## Narvi Collector Scale Models

**Estudiante:** Nancy Campos Basurto  
**Asignatura:** Desarrollo de Aplicaciones Web

[Visitar el sitio publicado](https://two626-desarrollo-de-aplicaciones-web-d9fz.onrender.com/)

Aplicación web para presentar servicios de figuras coleccionables y administrar productos, clientes, proveedores y facturación. La versión final del código se encuentra en la rama `main` de este repositorio.

## Contenidos implementados

| Requisito | Implementación |
| --- | --- |
| Autenticación | Inicio y cierre de sesión con Flask-Login y contraseñas almacenadas mediante hash. |
| Control de acceso | Catálogo público y gestión reservada a cuentas autorizadas; registro público cerrado. |
| CRUD completo | Crear, consultar, editar y eliminar productos, clientes, proveedores y facturas. |
| Tablas relacionadas | Productos → proveedores; facturas → clientes y productos. Tabla de usuarios para autenticación. |
| Interfaz y navegación | Menú público, panel administrativo, catálogo con fotografías y formularios con validación. |
| Facturación e inventario | Numeración interna FAC, subtotal, IVA del 15 %, total y validación de existencias. |

Las facturas pagadas y pendientes descuentan inventario. Al editar se ajustan las unidades y al anular o eliminar se devuelve el stock aplicado. Las operaciones se validan en el servidor y utilizan transacciones y bloqueos para evitar ventas superiores a las existencias.

## Verificación realizada

- Seis pruebas de integración con PostgreSQL aprobadas en un esquema aislado: autenticación y CSRF, CRUD y relaciones, validación de datos, facturación e inventario, ventas simultáneas y conservación de datos durante la migración.
- Seis pruebas específicas de acceso aprobadas con cliente Flask y base de datos simulada tras cerrar el registro público: navegación pública, protección de rutas, registro cerrado, bloqueo de sesiones no autorizadas, acceso administrativo y rechazo de cuentas no autorizadas.
- Comprobación en Render del cálculo de IVA y del rechazo de una cantidad superior al stock.
- Verificación del catálogo con sus fotografías, del registro público bloqueado y del acceso de la cuenta administradora.

Los escenarios de integración se ejecutaron antes del último ajuste de permisos; posteriormente se ejecutaron las pruebas específicas de acceso y las comprobaciones del sitio publicado.

## Guía de revisión

1. Abrir el sitio en una ventana privada para revisar Inicio, Quiénes somos, Catálogo y Contacto.
2. Entrar a Administración e iniciar sesión con una cuenta autorizada. Las credenciales se entregan de forma privada, nunca en este repositorio.
3. Revisar los módulos de productos, clientes, proveedores y facturación.
4. En Nueva factura, seleccionar un cliente y producto; introducir una cantidad y comprobar subtotal, IVA y total.
5. Introducir una cantidad mayor al stock y verificar el mensaje de error.

Para pruebas que creen, editen o eliminen registros, utilizar un entorno de pruebas y datos descartables.

## Tecnología y documentación

Python, Flask, Jinja, Flask-WTF, Flask-Login, PostgreSQL, HTML, CSS, JavaScript y Bootstrap. Despliegue en Render.

- [Guía de instalación, funcionamiento y entrega](ENTREGA.md)
- [Pruebas de integración](tests/test_flows.py)
- [Pruebas de acceso](tests/test_access.py)

La configuración de conexión se proporciona mediante variables de entorno. No publicar contraseñas ni claves.

La numeración FAC es interna: no constituye facturación electrónica autorizada por el SRI. Las facturas históricas sin relación de producto o desglose se conservan y se identifican para revisión.
