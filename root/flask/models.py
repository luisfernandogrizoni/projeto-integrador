from datetime import datetime
from root.flask import database

class Senha(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data_hora = database.Column(database.DateTime, default=datetime.now, nullable=False)
    finalidade = database.Column(database.String(250))
    senha = database.Column(database.String)