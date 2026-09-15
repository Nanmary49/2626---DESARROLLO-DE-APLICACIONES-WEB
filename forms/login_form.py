# ================================================================
# forms/login_form.py
# Formulario de inicio de sesión con Flask-WTF
# ================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """
    Formulario de login.
    Valida usuario y contraseña antes de autenticar.
    """

    usuario = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio.'),
        Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres.')
    ])

    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria.'),
        Length(min=4, max=100, message='La contraseña debe tener al menos 4 caracteres.')
    ])