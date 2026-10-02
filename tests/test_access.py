import sys, unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import conexion.conexion
conn=MagicMock(); conn.cursor.return_value.fetchone.return_value=(8,)
with patch.object(conexion.conexion,'get_db',return_value=conn):
 import app as m
from werkzeug.security import generate_password_hash
admin=m.Usuario(1,'admin',generate_password_hash('test-only'))
other=m.Usuario(2,'visitante',generate_password_hash('test-only'))
m.app.config.update(TESTING=True,SECRET_KEY='test-only',WTF_CSRF_ENABLED=False)
class Access(unittest.TestCase):
 def setUp(self): self.c=m.app.test_client()
 def test_public_navigation(self):
  html=self.c.get('/').text
  for text in ['Quiénes somos','Catálogo','Contacto']: self.assertIn(text,html)
  for text in ['Registrarse','Gestión de Productos','/clientes','/facturacion']: self.assertNotIn(text,html)
 def test_private_routes_require_login(self):
  for path in ['/dashboard','/productos','/clientes','/proveedores','/facturacion','/facturacion/nuevo','/productos/editar/1']:
   response=self.c.get(path);self.assertEqual(response.status_code,302);self.assertIn('/login',response.location)
 def test_registration_closed(self):
  for method in [self.c.get,self.c.post]: self.assertEqual(method('/registro').status_code,403)
 def test_existing_unauthorized_session(self):
  with patch.object(m.Usuario,'get_by_id',return_value=other):
   with self.c.session_transaction() as s:s['_user_id']='2';s['_fresh']=True
   for path in ['/dashboard','/productos','/clientes','/proveedores','/facturacion']:
    self.assertEqual(self.c.get(path).status_code,403)
   self.assertEqual(self.c.post('/productos/eliminar/1').status_code,403)
 def test_admin_login(self):
  with patch.object(m.Usuario,'get_by_usuario',return_value=admin):
   self.assertEqual(self.c.post('/login',data={'usuario':'admin','password':'test-only'}).status_code,302)
  with patch.object(m.Usuario,'get_by_id',return_value=admin):
   self.assertEqual(self.c.get('/dashboard').status_code,200)
   self.assertIn('Gestión de Productos',self.c.get('/').text)
 def test_non_admin_login_rejected(self):
  with patch.object(m.Usuario,'get_by_usuario',return_value=other):
   response=self.c.post('/login',data={'usuario':'visitante','password':'test-only'})
   self.assertIn('incorrectos',response.text)
   with self.c.session_transaction() as s:self.assertNotIn('_user_id',s)
unittest.main()
