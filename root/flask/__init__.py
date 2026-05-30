import os
from flask import Flask
from root.flask.extensions import database, bcrypt, csrf
from root.flask.routes import mask_data


def create_app():
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder='../templates',
                static_folder='../static')
    uri = os.environ.get("DATABASE_URL")
    app.jinja_env.filters['mask_data'] = mask_data
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = uri or f"sqlite:///{os.path.join(app.instance_path, 'banco_de_dados.db')}"
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "uma-chave-muito-segura-e-longa-maior-ainda")


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "development-key")

    database.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    from root.flask.routes import bp
    app.register_blueprint(bp)


    return app
