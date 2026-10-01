# ================================================================
# app.py — Narvi Collector Scale Models
# Semana 15: PostgreSQL + Render + CRUD completo + Login
# ================================================================

import os
from contextlib import contextmanager
import facturas_service
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from conexion.conexion import get_db
from models import Usuario
from forms.login_form import LoginForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'narvi-secret-key-2026')

# Solo las cuentas autorizadas pueden administrar el negocio.
app.config['ADMIN_USERNAMES'] = frozenset(
    name.strip() for name in os.environ.get('ADMIN_USERNAMES', 'admin').split(',') if name.strip()
)

def es_administrador(user):
    return user.is_authenticated and user.usuario in app.config['ADMIN_USERNAMES']

@app.context_processor
def permisos_menu():
    return {'admin_access': es_administrador(current_user)}

@app.before_request
def restringir_gestion():
    # También bloquea sesiones antiguas de cuentas registradas públicamente.
    if request.endpoint not in (None, 'static', 'index', 'login', 'logout', 'registro'):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not es_administrador(current_user):
            return render_template('acceso_restringido.html', **contexto()), 403

# Proteccion CSRF
csrf = CSRFProtect(app)

# Configuracion Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesion para acceder a esta pagina.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id)


# ================================================================
# INICIALIZAR TABLAS EN POSTGRESQL
# Se ejecuta al arrancar la app.
# ================================================================
def init_db():
    conn   = get_db()
    cursor = conn.cursor()

    # Tabla proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id SERIAL PRIMARY KEY,
            empresa VARCHAR(100) NOT NULL,
            contacto VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            estado VARCHAR(20) NOT NULL
        )
    ''')

    # Tabla productos con FK hacia proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            precio NUMERIC(10,2) NOT NULL,
            stock INTEGER NOT NULL,
            id_proveedor INTEGER REFERENCES proveedores(id)
        )
    ''')

    # Tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            ciudad VARCHAR(50) NOT NULL,
            tipo VARCHAR(20) NOT NULL
        )
    ''')

    # Tabla facturas con FK hacia clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id SERIAL PRIMARY KEY,
            id_cliente INTEGER REFERENCES clientes(id),
            cliente VARCHAR(100) NOT NULL,
            fecha DATE NOT NULL,
            producto VARCHAR(100) NOT NULL,
            cantidad INTEGER NOT NULL,
            total NUMERIC(10,2) NOT NULL,
            estado VARCHAR(20) NOT NULL
        )
    ''')

    # Tabla usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')

    # Migración aditiva: preserva los registros históricos sin inventar relaciones.
    cursor.execute("ALTER TABLE facturas ADD COLUMN IF NOT EXISTS id_producto INTEGER REFERENCES productos(id)")
    cursor.execute("ALTER TABLE facturas ADD COLUMN IF NOT EXISTS precio_unitario NUMERIC(10,2)")
    cursor.execute("ALTER TABLE facturas ADD COLUMN IF NOT EXISTS subtotal NUMERIC(10,2)")
    cursor.execute("ALTER TABLE facturas ADD COLUMN IF NOT EXISTS iva NUMERIC(10,2)")
    cursor.execute("ALTER TABLE facturas ADD COLUMN IF NOT EXISTS stock_aplicado BOOLEAN NOT NULL DEFAULT FALSE")
    conn.commit()
    cursor.close()
    conn.close()


# Inicializar base de datos al arrancar
init_db()


# ================================================================
# CONTEXTO GLOBAL
# ================================================================
def contexto():
    return {
        'nombre_sistema': 'Sistema de Gestion de Figuras de Coleccion',
        'estudiante': 'Nancy Campos Basurto',
        'asignatura': 'Desarrollo de Aplicaciones Web',
        'anio': '2026',
        'info_sistema': {
            'descripcion': 'Sistema web para gestion de figuras coleccionables',
            'version': '5.0'
        }
    }


# ================================================================
# RUTA PRINCIPAL
# ================================================================
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM productos')
    total_productos = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return render_template('index.html', total_productos=total_productos, **contexto())


# ================================================================
# AUTENTICACION
# ================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if es_administrador(current_user):
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.get_by_usuario(form.usuario.data)
        if user and check_password_hash(user.password, form.password.data) and es_administrador(user):
            login_user(user)
            flash('Bienvenido, ' + user.usuario + '!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form, **contexto())


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('acceso_restringido.html', **contexto()), 403


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada correctamente.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM productos')
    total_productos = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM clientes')
    total_clientes = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM proveedores')
    total_proveedores = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM facturas')
    total_facturas = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return render_template('dashboard.html',
        total_productos=total_productos,
        total_clientes=total_clientes,
        total_proveedores=total_proveedores,
        total_facturas=total_facturas,
        **contexto()
    )


# CRUD: las tablas y columnas provienen exclusivamente de esta configuración.
MODULOS = {
    'productos': (ProductoForm, 'Producto', ['nombre', 'descripcion', 'categoria', 'precio', 'stock', 'id_proveedor']),
    'clientes': (ClienteForm, 'Cliente', ['nombre', 'correo', 'telefono', 'ciudad', 'tipo']),
    'proveedores': (ProveedorForm, 'Proveedor', ['empresa', 'contacto', 'correo', 'telefono', 'categoria', 'estado']),
    'facturas': (FacturacionForm, 'Factura', ['id_cliente', 'id_producto', 'cantidad', 'estado']),
}

@contextmanager
def transaccion():
    conn = get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def opciones(form, tabla, cursor):
    if tabla == 'productos':
        cursor.execute('SELECT id, empresa FROM proveedores ORDER BY empresa, id')
        form.id_proveedor.choices = [(0, 'Sin proveedor asignado')] + [(x[0], f'{x[1]} (#{x[0]})') for x in cursor.fetchall()]
    elif tabla == 'facturas':
        cursor.execute('SELECT id, nombre FROM clientes ORDER BY nombre, id')
        form.id_cliente.choices = [(0, '-- Selecciona el cliente --')] + [(x[0], f'{x[1]} (#{x[0]})') for x in cursor.fetchall()]
        cursor.execute('SELECT id, nombre, precio, stock FROM productos ORDER BY nombre, id')
        registros = cursor.fetchall()
        form.id_producto.choices = [(0, '-- Selecciona el producto --')] + [(x[0], f'{x[1]} — ${x[2]:.2f} sin IVA — Stock: {x[3]} (#{x[0]})') for x in registros]
        form.precios = {str(x[0]): str(x[2]) for x in registros}


def guardar_formulario(tabla, id=None):
    clase, nombre, columnas = MODULOS[tabla]
    form = clase()
    try:
        with transaccion() as cursor:
            registro = None
            if id is not None:
                cursor.execute(f"SELECT {', '.join(columnas)} FROM {tabla} WHERE id=%s", (id,))
                registro = cursor.fetchone()
                if registro is None:
                    abort(404)
            opciones(form, tabla, cursor)
            if tabla == 'facturas' and id is not None:
                cursor.execute('SELECT id_producto, precio_unitario FROM facturas WHERE id=%s', (id,))
                precio_anterior = cursor.fetchone()
                if precio_anterior[0] and precio_anterior[1] is not None:
                    form.precios[str(precio_anterior[0])] = str(precio_anterior[1])
            if request.method == 'GET' and registro is not None:
                for columna, valor in zip(columnas, registro):
                    getattr(form, columna).data = (valor or 0) if columna.startswith('id_') else valor
            if form.validate_on_submit():
                valores = [getattr(form, c).data for c in columnas]
                if tabla == 'productos':
                    valores[-1] = valores[-1] or None
                campos = list(columnas)
                if tabla == 'facturas':
                    factura_id = facturas_service.guardar(cursor, dict(zip(columnas, valores)), id)
                    flash(f'Factura FAC-{factura_id:06d} guardada. Inventario actualizado.', 'success')
                    return redirect(url_for('facturacion'))
                if id is None:
                    marcas = ', '.join(['%s'] * len(campos))
                    cursor.execute(f"INSERT INTO {tabla} ({', '.join(campos)}) VALUES ({marcas})", tuple(valores))
                else:
                    asignaciones = ', '.join(c + '=%s' for c in campos)
                    cursor.execute(f"UPDATE {tabla} SET {asignaciones} WHERE id=%s", tuple(valores) + (id,))
                flash(nombre + (' actualizado correctamente.' if id is not None else ' registrado correctamente.'), 'success')
                return redirect(url_for('facturacion' if tabla == 'facturas' else tabla))
    except facturas_service.ErrorFactura as error:
        form.cantidad.errors = list(form.cantidad.errors) + [str(error)]
    except ForeignKeyViolation:
        flash('El registro relacionado cambió. Revisa la selección e intenta nuevamente.', 'warning')
        return redirect(request.path)
    return render_template('formulario_crud.html', form=form,
                           titulo=('Editar ' if id is not None else 'Nuevo ') + nombre,
                           modulo='facturacion' if tabla == 'facturas' else tabla, **contexto())


def borrar_registro(tabla, id):
    try:
        with transaccion() as cursor:
            if tabla == 'facturas':
                if not facturas_service.eliminar(cursor, id):
                    abort(404)
            else:
                cursor.execute(f'DELETE FROM {tabla} WHERE id=%s', (id,))
                if cursor.rowcount == 0:
                    abort(404)
        flash('Registro eliminado correctamente.', 'success')
    except ForeignKeyViolation:
        flash('No se puede eliminar: este registro está relacionado con productos o facturas. Conserva su historial o modifica primero la relación.', 'warning')
    return redirect(url_for('facturacion' if tabla == 'facturas' else tabla))


@app.route('/productos')
@login_required
def productos():
    with transaccion() as cursor:
        cursor.execute('SELECT * FROM productos ORDER BY id DESC')
        registros = cursor.fetchall()
    return render_template('productos.html', productos=registros, **contexto())


@app.route('/clientes')
@login_required
def clientes():
    with transaccion() as cursor:
        cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
        registros = cursor.fetchall()
    return render_template('clientes.html', clientes=registros, **contexto())


@app.route('/proveedores')
@login_required
def proveedores():
    with transaccion() as cursor:
        cursor.execute('SELECT * FROM proveedores ORDER BY id DESC')
        registros = cursor.fetchall()
    return render_template('proveedores.html', proveedores=registros, **contexto())


@app.route('/facturacion')
@login_required
def facturacion():
    with transaccion() as cursor:
        cursor.execute("""SELECT f.id, f.cliente, f.fecha, f.producto, f.cantidad,
                          f.total, f.estado, c.nombre, f.id_producto, f.subtotal, f.iva, f.precio_unitario
                          FROM facturas f LEFT JOIN clientes c ON c.id=f.id_cliente
                          ORDER BY f.id DESC""")
        registros = cursor.fetchall()
    return render_template('facturacion.html', facturas=registros,
                           total_general=sum(f[5] for f in registros), **contexto())


# Mantener las URLs y nombres de endpoints existentes.
def registrar_crud(tabla, ruta, singular):
    def nuevo():
        return guardar_formulario(tabla)
    def editar(id):
        return guardar_formulario(tabla, id)
    def eliminar(id):
        return borrar_registro(tabla, id)
    nuevo_endpoint = 'nueva_factura' if tabla == 'facturas' else 'nuevo_' + singular
    app.add_url_rule(ruta + '/nuevo', nuevo_endpoint, login_required(nuevo), methods=['GET', 'POST'])
    app.add_url_rule(ruta + '/editar/<int:id>', 'editar_' + singular, login_required(editar), methods=['GET', 'POST'])
    app.add_url_rule(ruta + '/eliminar/<int:id>', 'eliminar_' + singular, login_required(eliminar), methods=['POST'])


registrar_crud('productos', '/productos', 'producto')
registrar_crud('clientes', '/clientes', 'cliente')
registrar_crud('proveedores', '/proveedores', 'proveedor')
registrar_crud('facturas', '/facturacion', 'factura')


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
