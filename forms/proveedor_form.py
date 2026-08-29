# ================================================================
# forms/proveedor_form.py
# Formulario de proveedores con Flask-WTF y WTForms
# ================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Email

class ProveedorForm(FlaskForm):
    """
    Formulario para registrar y editar proveedores.
    Hereda de FlaskForm para incluir protección CSRF.
    """

    empresa = StringField('Nombre de la empresa', validators=[
        DataRequired(message='El nombre de la empresa es obligatorio.'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')
    ])

    contacto = StringField('Nombre del contacto', validators=[
        DataRequired(message='El contacto es obligatorio.'),
        Length(min=3, max=100, message='El contacto debe tener entre 3 y 100 caracteres.')
    ])

    correo = StringField('Correo electrónico', validators=[
        DataRequired(message='El correo es obligatorio.'),
        Email(message='Ingresa un correo electrónico válido.')
    ])

    telefono = StringField('Teléfono', validators=[
        DataRequired(message='El teléfono es obligatorio.'),
        Length(min=7, max=20, message='El teléfono debe tener entre 7 y 20 caracteres.')
    ])

    categoria = SelectField('Categoría', validators=[
        DataRequired(message='Selecciona una categoría.')
    ], choices=[
        ('', '-- Selecciona una categoría --'),
        ('Kits y materiales', 'Kits y materiales'),
        ('Materiales 3D', 'Materiales 3D'),
        ('Pinturas y barnices', 'Pinturas y barnices'),
        ('Figuras importadas', 'Figuras importadas'),
        ('Herramientas', 'Herramientas'),
    ])

    estado = SelectField('Estado', validators=[
        DataRequired(message='Selecciona el estado.')
    ], choices=[
        ('', '-- Selecciona el estado --'),
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ])