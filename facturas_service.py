"""Cálculo monetario y movimientos de inventario dentro de una transacción."""
from decimal import Decimal, ROUND_HALF_UP

IVA = Decimal('0.15')
CENTAVO = Decimal('0.01')


class ErrorFactura(ValueError):
    pass


def guardar(cursor, datos, factura_id=None):
    anterior = None
    if factura_id is not None:
        cursor.execute('SELECT id_producto, cantidad, stock_aplicado, precio_unitario FROM facturas WHERE id=%s FOR UPDATE', (factura_id,))
        anterior = cursor.fetchone()
        if anterior is None:
            raise ErrorFactura('La factura ya no existe.')
    producto_id = datos['id_producto']
    ids = sorted({producto_id} | ({anterior[0]} if anterior and anterior[0] else set()))
    productos = {}
    for id in ids:
        cursor.execute('SELECT nombre, precio, stock FROM productos WHERE id=%s FOR UPDATE', (id,))
        producto = cursor.fetchone()
        if producto is None:
            raise ErrorFactura('El producto ya no existe.')
        productos[id] = producto
    cursor.execute('SELECT nombre FROM clientes WHERE id=%s', (datos['id_cliente'],))
    cliente = cursor.fetchone()
    if cliente is None:
        raise ErrorFactura('Selecciona un cliente registrado.')
    cantidad = datos['cantidad']
    if cantidad < 1:
        raise ErrorFactura('La cantidad debe ser mayor que cero.')
    nombre, precio, disponible = productos[producto_id]
    # Al editar, las unidades de esta factura vuelven a estar disponibles.
    if anterior and anterior[2] and anterior[0] == producto_id:
        disponible += anterior[1]
    aplicar = datos['estado'] != 'Anulada'
    if aplicar and cantidad > disponible:
        raise ErrorFactura(f'Stock insuficiente: hay {disponible} unidades disponibles y solicitaste {cantidad}.')
    if anterior and anterior[0] == producto_id and anterior[3] is not None:
        precio = anterior[3]  # Mantener el precio histórico al editar.
    precio = Decimal(precio).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    subtotal = (precio * cantidad).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    impuesto = (subtotal * IVA).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    total = subtotal + impuesto
    if total > Decimal('99999999.99'):
        raise ErrorFactura('El total supera el importe permitido.')
    if anterior and anterior[2]:
        cursor.execute('UPDATE productos SET stock=stock+%s WHERE id=%s', (anterior[1], anterior[0]))
    if aplicar:
        cursor.execute('UPDATE productos SET stock=stock-%s WHERE id=%s', (cantidad, producto_id))
    valores = (datos['id_cliente'], producto_id, cliente[0], nombre, cantidad, precio, subtotal, impuesto, total, datos['estado'], aplicar)
    if factura_id is None:
        cursor.execute('''INSERT INTO facturas
            (id_cliente,id_producto,cliente,producto,cantidad,precio_unitario,subtotal,iva,total,estado,stock_aplicado,fecha)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE) RETURNING id''', valores)
        factura_id = cursor.fetchone()[0]
    else:
        cursor.execute('''UPDATE facturas SET id_cliente=%s,id_producto=%s,cliente=%s,producto=%s,
            cantidad=%s,precio_unitario=%s,subtotal=%s,iva=%s,total=%s,estado=%s,stock_aplicado=%s WHERE id=%s''', valores + (factura_id,))
    return factura_id


def eliminar(cursor, factura_id):
    cursor.execute('SELECT id_producto,cantidad,stock_aplicado FROM facturas WHERE id=%s FOR UPDATE', (factura_id,))
    factura = cursor.fetchone()
    if factura is None:
        return False
    if factura[2]:
        cursor.execute('UPDATE productos SET stock=stock+%s WHERE id=%s', (factura[1], factura[0]))
    cursor.execute('DELETE FROM facturas WHERE id=%s', (factura_id,))
    return True
