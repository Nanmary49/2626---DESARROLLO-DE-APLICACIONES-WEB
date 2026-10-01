"""Pruebas PostgreSQL aisladas. Requiere TEST_DATABASE_URL; nunca usa tablas públicas."""
import os
import re
import sys
import unittest
import uuid
from pathlib import Path
import psycopg2
from psycopg2 import sql

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
SCHEMA = 'narvi_test_' + uuid.uuid4().hex
DSN = os.environ['TEST_DATABASE_URL']
admin = psycopg2.connect(DSN, sslmode='require')
admin.autocommit = True
with admin.cursor() as c:
    c.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(SCHEMA)))

def isolated_db():
    conn = psycopg2.connect(DSN, sslmode='require')
    with conn.cursor() as c:
        c.execute(sql.SQL('SET search_path TO {}').format(sql.Identifier(SCHEMA)))
    return conn

import conexion.conexion
conexion.conexion.get_db = isolated_db

try:
    import app as module
    module.app.config.update(TESTING=True, SECRET_KEY='only-for-isolated-tests')

    def query(statement, values=()):
        conn = isolated_db()
        try:
            with conn.cursor() as c:
                c.execute(statement, values)
                return c.fetchall() if c.description else None
        finally:
            conn.close()

    class Flows(unittest.TestCase):
        def setUp(self):
            conn = isolated_db()
            with conn.cursor() as c:
                c.execute('TRUNCATE facturas, productos, clientes, proveedores, usuarios RESTART IDENTITY CASCADE')
            conn.commit(); conn.close()
            self.client = module.app.test_client()
            self.register()
            self.login()

        def post(self, path, data):
            page = self.client.get(path)
            self.assertEqual(page.status_code, 200, path)
            token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', page.text).group(1)
            return self.client.post(path, data={**data, 'csrf_token': token}, follow_redirects=True)

        def register(self):
            return self.post('/registro', dict(usuario='tester', password='Testing123!', confirmar='Testing123!'))

        def login(self):
            return self.post('/login', dict(usuario='tester', password='Testing123!'))

        def create(self, path, data, table):
            response = self.post(path, data)
            self.assertEqual(response.status_code, 200)
            rows=query('SELECT id FROM '+table+' ORDER BY id DESC')
            self.assertTrue(rows, response.text)
            return rows[0][0]

        def seed(self):
            proveedor=dict(empresa='Proveedor prueba', contacto='Contacto prueba', correo='p@example.com', telefono='0991234567', categoria='Materiales 3D', estado='Activo')
            pid=self.create('/proveedores/nuevo', proveedor, 'proveedores')
            cliente=dict(nombre='Cliente prueba', correo='c@example.com', telefono='0991234567', ciudad='Quito', tipo='Nuevo')
            cid=self.create('/clientes/nuevo', cliente, 'clientes')
            producto=dict(nombre='Figura prueba', descripcion='Figura de prueba detallada', categoria='Impresiones 3D', precio='12.50', stock='20', id_proveedor=str(pid))
            proid=self.create('/productos/nuevo', producto, 'productos')
            factura=dict(id_cliente=str(cid),id_producto=str(proid),cantidad='2',total='25.00',estado='Pendiente')
            fid=self.create('/facturacion/nuevo',factura,'facturas')
            return [(pid,proveedor,'proveedores','proveedor'),(cid,cliente,'clientes','cliente'),(proid,producto,'productos','producto'),(fid,factura,'facturacion','factura')]

        def delete(self, path, id):
            page=self.client.get('/'+path)
            token=re.search(r'name="csrf_token"[^>]*value="([^"]+)"',page.text).group(1)
            return self.client.post(f'/{path}/eliminar/{id}',data={'csrf_token':token},follow_redirects=True)

        def test_full_crud_and_relationships(self):
            rows=self.seed()
            for id,data,path,singular in rows:
                edit=dict(data)
                field='estado' if path=='facturacion' else ('empresa' if path=='proveedores' else 'nombre')
                edit[field]='Pagada' if path=='facturacion' else 'Registro actualizado'
                response=self.post(f'/{path}/editar/{id}',edit)
                self.assertEqual(response.status_code,200)
                table='facturas' if path=='facturacion' else path
                self.assertEqual(query(f'SELECT COUNT(*) FROM {table}')[0][0],1)
                self.assertEqual(query(f'SELECT {field} FROM {table} WHERE id=%s',(id,))[0][0],edit[field])
            joined=query('SELECT f.id FROM facturas f JOIN clientes c ON c.id=f.id_cliente JOIN productos p ON p.id=f.id_producto JOIN proveedores v ON v.id=p.id_proveedor')
            self.assertEqual(len(joined),1)
            for index in (0,1,2):
                id,_,path,_=rows[index]
                response=self.delete(path,id)
                self.assertIn('No se puede eliminar',response.text)
            for index in (3,2,1,0):
                id,_,path,_=rows[index]
                self.assertEqual(self.delete(path,id).status_code,200)
            for table in ('facturas','productos','clientes','proveedores'):
                self.assertEqual(query('SELECT COUNT(*) FROM '+table)[0][0],0)

        def test_auth_and_csrf(self):
            self.client.get('/logout')
            for route in ('dashboard','productos','clientes','proveedores','facturacion'):
                response=self.client.get('/'+route)
                self.assertEqual(response.status_code,302)
                self.assertIn('/login',response.location)
            wrong=self.post('/login',dict(usuario='tester',password='wrong'))
            self.assertIn('incorrectos',wrong.text)
            self.assertEqual(self.client.post('/login',data={}).status_code,400)
            duplicate=self.register()
            self.assertIn('ya existe',duplicate.text)
            self.assertEqual(query('SELECT COUNT(*) FROM usuarios')[0][0],1)
            self.assertNotEqual(query('SELECT password FROM usuarios')[0][0],'Testing123!')
            self.login()
            self.assertEqual(self.client.post('/productos/eliminar/1').status_code,400)

        def test_invalid_inputs_and_missing_records(self):
            rows=self.seed()
            id,product,_,_=rows[2]
            for value in ('-1','', '2147483648'):
                self.post('/productos/nuevo',{**product,'stock':value})
            self.assertEqual(query('SELECT COUNT(*) FROM productos')[0][0],1)
            _,invoice,_,_=rows[3]
            for changes in ({'id_cliente':'999999'},{'id_producto':'999999'},{'cantidad':'0'},{'cantidad':'-1'},{'cantidad':'9999'},{'estado':'inventado'}):
                self.post('/facturacion/nuevo',{**invoice,**changes})
            self.assertEqual(query('SELECT COUNT(*) FROM facturas')[0][0],1)
            for route in ('productos','clientes','proveedores','facturacion'):
                self.assertEqual(self.client.get(f'/{route}/editar/999999').status_code,404)
            for route in ('/','/dashboard','/productos','/clientes','/proveedores','/facturacion'):
                self.assertEqual(self.client.get(route).status_code,200)
            self.assertNotIn('id="formulario-producto"',self.client.get('/').text)
            self.assertIn('>1</strong>',self.client.get('/').text)

        def test_migration_is_repeatable(self):
            self.seed()
            module.init_db()
            module.init_db()
            self.assertEqual(query('SELECT COUNT(*) FROM facturas')[0][0],1)

        def test_invoice_inventory_tax_and_cancellation(self):
            from decimal import Decimal
            rows=self.seed()
            pid=rows[2][0]; fid=rows[3][0]; data=rows[3][1]
            self.assertEqual(query('SELECT subtotal,iva,total FROM facturas WHERE id=%s',(fid,))[0],(Decimal('25.00'),Decimal('3.75'),Decimal('28.75')))
            self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],18)
            bad=self.post('/facturacion/nuevo',{**data,'cantidad':'19'})
            self.assertIn('Stock insuficiente',bad.text)
            self.assertEqual(query('SELECT COUNT(*) FROM facturas')[0][0],1)
            self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],18)
            self.post(f'/facturacion/editar/{fid}',{**data,'cantidad':'3'})
            self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],17)
            for _ in range(2):
                self.post(f'/facturacion/editar/{fid}',{**data,'cantidad':'3','estado':'Anulada'})
                self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],20)
            self.post(f'/facturacion/editar/{fid}',{**data,'cantidad':'20','estado':'Pagada','total':'0.01'})
            self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],0)
            self.assertEqual(query('SELECT total FROM facturas WHERE id=%s',(fid,))[0][0],Decimal('287.50'))
            self.delete('facturacion',fid)
            self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],20)

        def test_concurrent_sales_do_not_oversell(self):
            from concurrent.futures import ThreadPoolExecutor
            rows=self.seed(); pid=rows[2][0]
            data={'id_cliente':rows[1][0],'id_producto':pid,'cantidad':18,'estado':'Pagada'}
            def sell():
                try:
                    with module.transaccion() as cursor:
                        module.facturas_service.guardar(cursor,data)
                    return True
                except module.facturas_service.ErrorFactura:
                    return False
            with ThreadPoolExecutor(max_workers=2) as pool:
                results=list(pool.map(lambda _:sell(),range(2)))
            self.assertEqual(sorted(results),[False,True])
            self.assertEqual(query('SELECT stock FROM productos WHERE id=%s',(pid,))[0][0],0)

    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Flows))
finally:
    # Solo el esquema temporal creado por este proceso; nunca public.
    with admin.cursor() as c:
        c.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(SCHEMA)))
    admin.close()

if not result.wasSuccessful():
    raise SystemExit(1)
