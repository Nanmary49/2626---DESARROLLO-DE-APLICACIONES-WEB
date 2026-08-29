# ================================================================
# forms/cliente_form.py
# Formulario de clientes con Flask-WTF y WTForms
# ================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    """
    Formulario para registrar y editar clientes.
    Hereda de FlaskForm para incluir protección CSRF.
    """

    nombre = StringField('Nombre completo', validators=[
        DataRequired(message='El nombre es obligatorio.'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')
    ])

    correo = StringField('Correo electrónico', validators=[
        DataRequired(message='El correo es obligatorio.'),
        Email(message='Ingresa un correo electrónico válido.')
    ])

    telefono = StringField('Teléfono', validators=[
        DataRequired(message='El teléfono es obligatorio.'),
        Length(min=7, max=20, message='El teléfono debe tener entre 7 y 20 caracteres.')
    ])

    ciudad = StringField('Ciudad', validators=[
        DataRequired(message='La ciudad es obligatoria.'),
        Length(min=2, max=50, message='La ciudad debe tener entre 2 y 50 caracteres.')
    ])

    tipo = SelectField('Tipo de cliente', validators=[
        DataRequired(message='Selecciona el tipo de cliente.')
    ], choices=[
        ('', '-- Selecciona el tipo --'),
        ('Frecuente', 'Frecuente'),
        ('Nuevo', 'Nuevo'),
        ('Ocasional', 'Ocasional'),
    ])