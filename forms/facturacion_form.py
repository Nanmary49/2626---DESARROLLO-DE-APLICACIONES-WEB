from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, NumberRange

class FacturacionForm(FlaskForm):
    id_cliente = SelectField('Cliente registrado', coerce=int, choices=[], validators=[NumberRange(min=1, message='Selecciona un cliente registrado.')])
    id_producto = SelectField('Producto registrado', coerce=int, choices=[], validators=[NumberRange(min=1, message='Selecciona un producto registrado.')])
    cantidad = IntegerField('Cantidad', validators=[InputRequired(), NumberRange(min=1, max=2147483647)])
    estado = SelectField('Estado', choices=[('', '-- Selecciona --'), ('Pagada', 'Pagada'), ('Pendiente', 'Pendiente'), ('Anulada', 'Anulada')], validators=[InputRequired()])
