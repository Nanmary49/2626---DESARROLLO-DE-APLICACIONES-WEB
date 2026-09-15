# ================================================================
# forms/usuario_form.py
# Formulario de registro de usuarios con Flask-WTF
# ================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class UsuarioForm(FlaskForm):
    """
    Formulario de registro de nuevos usuarios.
    Valida usuario, contraseña y confirmación.
    """

    usuario = StringField('Nombre de usuario', validators=[
        DataRequired(message='El nombre de usuario es obligatorio.'),
        Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres.')
    ])

    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria.'),
        Length(min=4, max=100, message='La contraseña debe tener al menos 4 caracteres.')
    ])

    confirmar = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Confirma tu contraseña.'),
        EqualTo('password', message='Las contraseñas no coinciden.')
    ])