import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        CONFIG = os.path.join(app.instance_path, 'config.json'),
        IMAGE_FOLDER = os.path.join(app.static_folder, 'img'),
        DATABASE = os.path.join(app.instance_path, 'db.sqlite'),
        ADMIN_TOKEN = None,
        TESTING = test_config is not None
    )

    # ensure the instance/images folder exists
    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    if not os.path.isdir(app.config['IMAGE_FOLDER']):
        os.makedirs(app.config['IMAGE_FOLDER'])

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello!'

    # load modules
    from .config import register_config
    register_config(app, test_config)

    from .models.database.base import register_database
    register_database(app)

    from .views.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .views.account import bp as account_bp
    app.register_blueprint(account_bp)

    from .views.bookshelf import bp as bs_bp
    app.register_blueprint(bs_bp)
    app.add_url_rule('/', endpoint='index')

    from .views.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
