# ================================================================
# forms/producto_form.py
# Formulario de productos con Flask-WTF y WTForms
# ================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    """
    Formulario para registrar y editar productos.
    Hereda de FlaskForm para incluir protección CSRF.
    """

    nombre = StringField('Nombre del producto', validators=[
        DataRequired(message='El nombre es obligatorio.'),
        Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')
    ])

    descripcion = TextAreaField('Descripción', validators=[
        DataRequired(message='La descripción es obligatoria.'),
        Length(min=10, max=300, message='La descripción debe tener entre 10 y 300 caracteres.')
    ])

    categoria = SelectField('Categoría', validators=[
        DataRequired(message='Selecciona una categoría.')
    ], choices=[
        ('', '-- Selecciona una categoría --'),
        ('Figuras Coleccionables', 'Figuras Coleccionables'),
        ('Modelos a Escala', 'Modelos a Escala'),
        ('Impresiones 3D', 'Impresiones 3D'),
        ('Pintura Profesional', 'Pintura Profesional'),
        ('Restauracion', 'Restauración'),
        ('Articulos Exclusivos', 'Artículos Exclusivos'),
    ])

    precio = DecimalField('Precio ($)', validators=[
        DataRequired(message='El precio es obligatorio.'),
        NumberRange(min=0.01, max=99999999.99, message='El precio debe ser mayor a 0.')
    ])

    stock = IntegerField('Stock disponible', validators=[
        InputRequired(message='El stock es obligatorio.'),
        NumberRange(min=0, max=2147483647, message='El stock no puede ser negativo.')
    ])
    id_proveedor = SelectField('Proveedor', coerce=int, choices=[])
