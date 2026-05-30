from flask import Blueprint, render_template, flash, request, url_for, redirect
import secrets
import string
from datetime import datetime

from root.flask import database
from root.flask.forms import Form
from root.flask.models import Senha

bp = Blueprint('main', __name__)

def mask_data(valor):
    """Filtro para converter datetime do banco para DD/MM/YYYY"""
    if not valor:
        return "-"

    return valor.strftime('%d/%m/%Y')


@bp.route("/", methods=["GET", "POST"])
def inicio():
    form = Form()

    if form.validate_on_submit():
        tamanho = form.tamanho.data
        finalidade = form.finalidade.data

        alfabeto = string.ascii_letters + string.digits + string.punctuation
        senha_gerada = ''.join(secrets.choice(alfabeto) for _ in range(tamanho))

        try:
            nova_senha = Senha(
                data_hora=datetime.now(),
                finalidade=finalidade,
                senha=senha_gerada
            )

            database.session.add(nova_senha)
            database.session.commit()

            flash('Senha gerada!', 'success')
            return redirect(url_for('main.inicio'))

        except Exception as e:
            database.session.rollback()
            flash(f'Ocorreu um erro interno: {str(e)}. Tente novamente.', 'danger')

    senhas = database.session.query(Senha).order_by(Senha.data_hora.desc()).all()
    finalidade = database.session.query(Senha.finalidade).all()

    return render_template("inicio.html", form=form, senhas=senhas, finalidade=finalidade)