# Narvi — entrega del proyecto

## Funcionalidades

- Autenticación con Flask-Login, contraseñas con hash y formularios CSRF.
- Crear, listar, editar y eliminar productos, clientes, proveedores y facturas.
- Relaciones: proveedores ← productos ← facturas → clientes. Usuarios administra el acceso.
- Las facturas seleccionan clientes y productos existentes, usan el precio del producto sin IVA y calculan subtotal + IVA del 15 % con redondeo a dos decimales.
- Número interno único FAC-000001 derivado de la secuencia de la base de datos. No es un comprobante electrónico autorizado por el SRI.
- Pagada y Pendiente descuentan inventario. Anulada no descuenta; al anular o eliminar se devuelven las unidades anteriormente descontadas. Editar aplica solo la diferencia, incluso al cambiar de producto.
- Bloqueo de filas en PostgreSQL para evitar ventas simultáneas por encima del stock. El servidor valida cantidades, precios y relaciones.
- Los registros históricos conservan sus importes; los que carecen de producto relacionado se señalan para revisión y no descuentan stock retroactivamente.
- El formulario del inicio dirige al módulo persistente. El catálogo y el diseño premium se conservan.
- Contacto abre la aplicación de correo; no afirma que un mensaje se envió automáticamente.

## Ejecución

Instalar `requirements.txt` y configurar `DATABASE_URL` y `SECRET_KEY` mediante variables de entorno. No guardar contraseñas en archivos del repositorio.

En Render: `gunicorn app:app --bind 0.0.0.0:$PORT`.
La inicialización crea tablas faltantes y añade columnas nuevas a facturas, sin borrar registros.

## Pruebas

Ejecutar `python tests/test_flows.py` con `TEST_DATABASE_URL` apuntando a PostgreSQL. La cuenta necesita crear esquemas. Cada ejecución crea un esquema temporal exclusivo, prueba allí y lo elimina al finalizar; no utiliza las tablas de producción.

Cobertura: login, contraseña incorrecta, registro duplicado, hash, protección CSRF, acceso anónimo, CRUD de cuatro módulos, integridad referencial, entradas inválidas, contador persistente, migración repetible, subtotal e IVA, stock insuficiente, edición, anulación repetida, devolución de stock y dos ventas concurrentes.

## Demostración

1. Iniciar sesión y registrar un proveedor y un cliente de demostración.
2. Registrar un producto a $12,50 sin IVA y stock 5, asociado al proveedor.
3. Crear una factura por 2 unidades: subtotal $25,00; IVA $3,75; total $28,75. Quedan 3 unidades.
4. Intentar vender 4: debe mostrar «Stock insuficiente» y conservar el stock.
5. Editar la factura a 3 unidades: quedan 2. Anular: vuelven las 5.
6. Probar edición en clientes y proveedores, y eliminación de registros sin relaciones.
7. Cerrar sesión y comprobar que los módulos requieren autenticación.

## Datos existentes

Los clientes y productos de las facturas anteriores deben revisarse por su propietario cuando estén marcados; no se adivinan asociaciones. Antes de usar el sistema fuera de la demostración académica, configurar credenciales nuevas si alguna contraseña estuvo previamente publicada en el historial del repositorio.
