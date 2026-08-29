# ================================================================
# forms/facturacion_form.py
# Formulario de facturación con Flask-WTF y WTForms
# ================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class FacturacionForm(FlaskForm):
    """
    Formulario para registrar y editar facturas.
    Hereda de FlaskForm para incluir protección CSRF.
    """

    cliente = StringField('Nombre del cliente', validators=[
        DataRequired(message='El nombre del cliente es obligatorio.'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')
    ])

    producto = StringField('Producto', validators=[
        DataRequired(message='El producto es obligatorio.'),
        Length(min=3, max=100, message='El producto debe tener entre 3 y 100 caracteres.')
    ])

    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message='La cantidad es obligatoria.'),
        NumberRange(min=1, message='La cantidad debe ser mayor a 0.')
    ])

    total = FloatField('Total ($)', validators=[
        DataRequired(message='El total es obligatorio.'),
        NumberRange(min=0.01, message='El total debe ser mayor a 0.')
    ])

    estado = SelectField('Estado', validators=[
        DataRequired(message='Selecciona el estado.')
    ], choices=[
        ('', '-- Selecciona el estado --'),
        ('Pagada', 'Pagada'),
        ('Pendiente', 'Pendiente'),
        ('Anulada', 'Anulada'),
    ])