from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class Form(FlaskForm):

    tamanho = IntegerField('Tamanho da senha:', validators=[DataRequired()])
    finalidade = StringField("Finalidade da senha:", validators=[DataRequired()])

    botao_confirmacao = SubmitField("Gerar")
