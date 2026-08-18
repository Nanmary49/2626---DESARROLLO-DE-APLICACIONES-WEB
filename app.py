from flask import Flask, render_template

app = Flask(__name__)

productos_demo = [
    {'id': 1, 'nombre': 'Figura Goku Ultra Instinto', 'categoria': 'Figuras Coleccionables', 'precio': 85.00, 'stock': 5},
    {'id': 2, 'nombre': 'Tanque Sherman WWII 1:35', 'categoria': 'Modelos a Escala', 'precio': 120.00, 'stock': 3},
    {'id': 3, 'nombre': 'Impresion 3D Dragon Personalizado', 'categoria': 'Impresiones 3D', 'precio': 60.00, 'stock': 0},
    {'id': 4, 'nombre': 'Figura Naruto Sage Mode', 'categoria': 'Figuras Coleccionables', 'precio': 95.00, 'stock': 2},
    {'id': 5, 'nombre': 'Busto Iron Man Pintado', 'categoria': 'Pintura Profesional', 'precio': 150.00, 'stock': 0},
    {'id': 6, 'nombre': 'Restauracion Figura Vintage', 'categoria': 'Restauracion', 'precio': 45.00, 'stock': 10},
]

clientes_demo = [
    {'id': 1, 'nombre': 'Carlos Mendoza', 'correo': 'carlos@email.com', 'telefono': '+593 98 111 2233', 'ciudad': 'Quito', 'tipo': 'Frecuente'},
    {'id': 2, 'nombre': 'Ana Lucia Torres', 'correo': 'ana@email.com', 'telefono': '+593 99 444 5566', 'ciudad': 'Guayaquil', 'tipo': 'Nuevo'},
    {'id': 3, 'nombre': 'Diego Ramirez', 'correo': 'diego@email.com', 'telefono': '+593 98 777 8899', 'ciudad': 'Cuenca', 'tipo': 'Frecuente'},
    {'id': 4, 'nombre': 'Maria Fernanda Paz', 'correo': 'mfpaz@email.com', 'telefono': '+593 99 000 1122', 'ciudad': 'Ambato', 'tipo': 'Ocasional'},
    {'id': 5, 'nombre': 'Roberto Suarez', 'correo': 'roberto@email.com', 'telefono': '+593 98 333 4455', 'ciudad': 'Quito', 'tipo': 'Frecuente'},
]

proveedores_demo = [
    {'id': 1, 'empresa': 'ModelKit Ecuador', 'contacto': 'Juan Polo', 'correo': 'modelkit@proveedor.com', 'telefono': '+593 2 222 3344', 'categoria': 'Kits y materiales', 'estado': 'Activo'},
    {'id': 2, 'empresa': 'Resinas 3D Latam', 'contacto': 'Sofia Vera', 'correo': 'resinas3d@latam.com', 'telefono': '+593 2 555 6677', 'categoria': 'Materiales 3D', 'estado': 'Activo'},
    {'id': 3, 'empresa': 'Pinturas Artisticas S.A.', 'contacto': 'Marco Rios', 'correo': 'pinturas@arte.com', 'telefono': '+593 2 888 9900', 'categoria': 'Pinturas y barnices', 'estado': 'Activo'},
    {'id': 4, 'empresa': 'ImportFiguras Cia.', 'contacto': 'Laura Gomez', 'correo': 'importfig@cia.com', 'telefono': '+593 2 111 2233', 'categoria': 'Figuras importadas', 'estado': 'Inactivo'},
]

facturas_demo = [
    {'id': 'F-001', 'cliente': 'Carlos Mendoza', 'fecha': '2026-07-15', 'producto': 'Figura Goku Ultra Instinto', 'cantidad': 1, 'total': 85.00, 'estado': 'Pagada'},
    {'id': 'F-002', 'cliente': 'Ana Lucia Torres', 'fecha': '2026-07-18', 'producto': 'Tanque Sherman WWII 1:35', 'cantidad': 1, 'total': 120.00, 'estado': 'Pagada'},
    {'id': 'F-003', 'cliente': 'Diego Ramirez', 'fecha': '2026-07-22', 'producto': 'Impresion 3D Dragon Personalizado', 'cantidad': 2, 'total': 120.00, 'estado': 'Pendiente'},
    {'id': 'F-004', 'cliente': 'Maria Fernanda Paz', 'fecha': '2026-07-25', 'producto': 'Busto Iron Man Pintado', 'cantidad': 1, 'total': 150.00, 'estado': 'Pagada'},
    {'id': 'F-005', 'cliente': 'Roberto Suarez', 'fecha': '2026-07-28', 'producto': 'Figura Naruto Sage Mode', 'cantidad': 1, 'total': 95.00, 'estado': 'Pendiente'},
]

@app.route('/')
def index():
    return render_template('index.html',
        nombre_sistema='Sistema de Gestion de Figuras de Coleccion',
        estudiante='Nancy Campos Basurto',
        asignatura='Desarrollo de Aplicaciones Web',
        anio='2026',
        info_sistema={'descripcion': 'Sistema web para gestion de figuras coleccionables', 'version': '2.0'}
    )

@app.route('/productos')
def productos():
    return render_template('productos.html',
        productos=productos_demo,
        nombre_sistema='Sistema de Gestion de Figuras de Coleccion',
        estudiante='Nancy Campos Basurto',
        asignatura='Desarrollo de Aplicaciones Web',
        anio='2026',
        info_sistema={'descripcion': 'Sistema web para gestion de figuras coleccionables', 'version': '2.0'}
    )

@app.route('/clientes')
def clientes():
    return render_template('clientes.html',
        clientes=clientes_demo,
        nombre_sistema='Sistema de Gestion de Figuras de Coleccion',
        estudiante='Nancy Campos Basurto',
        asignatura='Desarrollo de Aplicaciones Web',
        anio='2026',
        info_sistema={'descripcion': 'Sistema web para gestion de figuras coleccionables', 'version': '2.0'}
    )

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html',
        proveedores=proveedores_demo,
        nombre_sistema='Sistema de Gestion de Figuras de Coleccion',
        estudiante='Nancy Campos Basurto',
        asignatura='Desarrollo de Aplicaciones Web',
        anio='2026',
        info_sistema={'descripcion': 'Sistema web para gestion de figuras coleccionables', 'version': '2.0'}
    )

@app.route('/facturacion')
def facturacion():
    total_general = sum(f['total'] for f in facturas_demo)
    return render_template('facturacion.html',
        facturas=facturas_demo,
        total_general=total_general,
        nombre_sistema='Sistema de Gestion de Figuras de Coleccion',
        estudiante='Nancy Campos Basurto',
        asignatura='Desarrollo de Aplicaciones Web',
        anio='2026',
        info_sistema={'descripcion': 'Sistema web para gestion de figuras coleccionables', 'version': '2.0'}
    )

if __name__ == '__main__':
    app.run(debug=True)