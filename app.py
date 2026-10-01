# ================================================================
# app.py — Narvi Collector Scale Models
# Semana 15: PostgreSQL + Render + CRUD completo + Login
# ================================================================

import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from conexion.conexion import get_db
from models import Usuario
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'narvi-secret-key-2026')

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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.get_by_usuario(form.usuario.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Bienvenido, ' + user.usuario + '!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form, **contexto())


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = UsuarioForm()
    if form.validate_on_submit():
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        existe = cursor.fetchone()
        if existe:
            flash('El nombre de usuario ya existe.', 'danger')
            cursor.close()
            conn.close()
        else:
            password_hash = generate_password_hash(form.password.data)
            cursor.execute(
                'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
                (form.usuario.data, password_hash)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Usuario registrado. Ahora puedes iniciar sesion.', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html', form=form, **contexto())


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


# ================================================================
# MODULO PRODUCTOS — CRUD completo con PostgreSQL
# ================================================================

@app.route('/productos')
@login_required
def productos():
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos ORDER BY id DESC')
    productos_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos_db, **contexto())


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, categoria, precio, stock)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.nombre.data, form.descripcion.data, form.categoria.data,
              form.precio.data, form.stock.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto registrado correctamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html',
        form=form, titulo='Nuevo Producto', **contexto())


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn   = get_db()
    cursor = conn.cursor()
    form   = ProductoForm()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('productos'))
        form.nombre.data      = producto[1]
        form.descripcion.data = producto[2]
        form.categoria.data   = producto[3]
        form.precio.data      = producto[4]
        form.stock.data       = producto[5]
        return render_template('formulario_producto.html',
            form=form, titulo='Editar Producto', **contexto())
    if form.validate_on_submit():
        cursor.execute('''
            UPDATE productos SET nombre=%s, descripcion=%s, categoria=%s,
            precio=%s, stock=%s WHERE id=%s
        ''', (form.nombre.data, form.descripcion.data, form.categoria.data,
              form.precio.data, form.stock.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos'))
    cursor.close()
    conn.close()
    return render_template('formulario_producto.html',
        form=form, titulo='Editar Producto', **contexto())


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos'))


# ================================================================
# MODULO CLIENTES — CRUD con PostgreSQL
# ================================================================

@app.route('/clientes')
@login_required
def clientes():
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_db, **contexto())


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, correo, telefono, ciudad, tipo)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.nombre.data, form.correo.data, form.telefono.data,
              form.ciudad.data, form.tipo.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html',
        form=form, titulo='Nuevo Cliente', **contexto())


@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    conn   = get_db()
    cursor = conn.cursor()
    form   = ClienteForm()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
        cliente = cursor.fetchone()
        cursor.close()
        conn.close()
        if not cliente:
            flash('Cliente no encontrado.', 'danger')
            return redirect(url_for('clientes'))
        form.nombre.data   = cliente[1]
        form.correo.data   = cliente[2]
        form.telefono.data = cliente[3]
        form.ciudad.data   = cliente[4]
        form.tipo.data     = cliente[5]
        return render_template('formulario_cliente.html',
            form=form, titulo='Editar Cliente', **contexto())
    if form.validate_on_submit():
        cursor.execute('''
            UPDATE clientes SET nombre=%s, correo=%s, telefono=%s,
            ciudad=%s, tipo=%s WHERE id=%s
        ''', (form.nombre.data, form.correo.data, form.telefono.data,
              form.ciudad.data, form.tipo.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))
    cursor.close()
    conn.close()
    return render_template('formulario_cliente.html',
        form=form, titulo='Editar Cliente', **contexto())


@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes'))


# ================================================================
# MODULO PROVEEDORES — CRUD con PostgreSQL
# ================================================================

@app.route('/proveedores')
@login_required
def proveedores():
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores ORDER BY id DESC')
    proveedores_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores_db, **contexto())


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedores (empresa, contacto, correo, telefono, categoria, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (form.empresa.data, form.contacto.data, form.correo.data,
              form.telefono.data, form.categoria.data, form.estado.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html',
        form=form, titulo='Nuevo Proveedor', **contexto())


@app.route('/proveedores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor eliminado correctamente.', 'success')
    return redirect(url_for('proveedores'))


# ================================================================
# MODULO FACTURACION — CRUD con PostgreSQL y JOIN
# ================================================================

@app.route('/facturacion')
@login_required
def facturacion():
    conn   = get_db()
    cursor = conn.cursor()
    # JOIN entre facturas y clientes
    cursor.execute('''
        SELECT f.id, f.cliente, f.fecha, f.producto,
               f.cantidad, f.total, f.estado,
               c.nombre as nombre_cliente
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id
        ORDER BY f.id DESC
    ''')
    facturas_db   = cursor.fetchall()
    total_general = sum(f[5] for f in facturas_db)
    cursor.close()
    conn.close()
    return render_template('facturacion.html',
        facturas=facturas_db,
        total_general=total_general,
        **contexto()
    )


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
def nueva_factura():
    form = FacturacionForm()
    if form.validate_on_submit():
        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (id_cliente, cliente, fecha, producto, cantidad, total, estado)
            VALUES (%s, %s, CURRENT_DATE, %s, %s, %s, %s)
        ''', (1, form.cliente.data, form.producto.data,
              form.cantidad.data, form.total.data, form.estado.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html',
        form=form, titulo='Nueva Factura', **contexto())


@app.route('/facturacion/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_factura(id):
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Factura eliminada correctamente.', 'success')
    return redirect(url_for('facturacion'))


if __name__ == '__main__':
    app.run(debug=True)
