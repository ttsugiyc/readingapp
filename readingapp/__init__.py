from flask import Flask


def create_app(test_config=None):
    # create the app
    app = Flask(__name__)

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
