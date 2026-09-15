# ================================================================
# app.py — Narvi Collector Scale Models
# Semana 14: Sistema de Login con Flask-Login
# ================================================================

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
app.config['SECRET_KEY'] = 'narvi-secret-key-2026'

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
            'version': '4.0'
        }
    }


# ================================================================
# RUTA PRINCIPAL
# ================================================================
@app.route('/')
def index():
    return render_template('index.html', **contexto())


# ================================================================
# AUTENTICACION — Login, Registro, Logout
# ================================================================

# LOGIN
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


# REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = UsuarioForm()
    if form.validate_on_submit():
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        existe = cursor.fetchone()
        if existe:
            flash('El nombre de usuario ya existe. Elige otro.', 'danger')
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
            flash('Usuario registrado correctamente. Ahora puedes iniciar sesion.', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html', form=form, **contexto())


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada correctamente.', 'info')
    return redirect(url_for('login'))


# DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as total FROM productos')
    total_productos = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) as total FROM clientes')
    total_clientes = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) as total FROM proveedores')
    total_proveedores = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) as total FROM facturas')
    total_facturas = cursor.fetchone()['total']
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
# MODULO PRODUCTOS — Protegido con @login_required
# ================================================================
@app.route('/productos')
@login_required
def productos():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
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
    return render_template('formulario_producto.html', form=form, titulo='Nuevo Producto', **contexto())


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
    form   = ProductoForm()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('productos'))
        form.nombre.data      = producto['nombre']
        form.descripcion.data = producto['descripcion']
        form.categoria.data   = producto['categoria']
        form.precio.data      = producto['precio']
        form.stock.data       = producto['stock']
        return render_template('formulario_producto.html', form=form, titulo='Editar Producto', **contexto())
    if form.validate_on_submit():
        cursor.execute('''
            UPDATE productos SET nombre=%s, descripcion=%s, categoria=%s, precio=%s, stock=%s
            WHERE id=%s
        ''', (form.nombre.data, form.descripcion.data, form.categoria.data,
              form.precio.data, form.stock.data, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos'))
    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', form=form, titulo='Editar Producto', **contexto())


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
# MODULO CLIENTES — Protegido con @login_required
# ================================================================
@app.route('/clientes')
@login_required
def clientes():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
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
    return render_template('formulario_cliente.html', form=form, titulo='Nuevo Cliente', **contexto())


# ================================================================
# MODULO PROVEEDORES — Protegido con @login_required
# ================================================================
@app.route('/proveedores')
@login_required
def proveedores():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
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
    return render_template('formulario_proveedor.html', form=form, titulo='Nuevo Proveedor', **contexto())


# ================================================================
# MODULO FACTURACION — Protegido con @login_required
# ================================================================
@app.route('/facturacion')
@login_required
def facturacion():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT f.*, c.nombre as nombre_cliente
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id
        ORDER BY f.id DESC
    ''')
    facturas_db    = cursor.fetchall()
    total_general  = sum(f['total'] for f in facturas_db)
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
            VALUES (%s, %s, CURDATE(), %s, %s, %s, %s)
        ''', (1, form.cliente.data, form.producto.data,
              form.cantidad.data, form.total.data, form.estado.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form, titulo='Nueva Factura', **contexto())


if __name__ == '__main__':
    app.run(debug=True)