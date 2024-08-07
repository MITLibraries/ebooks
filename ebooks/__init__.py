import os

from flask import Flask
from flask_talisman import Talisman
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def create_app():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN") or None, integrations=[FlaskIntegration()]
    )

    app = Flask(__name__, instance_relative_config=True)

    flask_env = os.getenv("FLASK_ENV", default="production")
    if flask_env == "development":
        app.config.from_object("ebooks.config.DevelopmentConfig")
    elif flask_env == "testing":
        app.config.from_object("ebooks.config.TestingConfig")
    else:
        app.config.from_object("ebooks.config.Config")

    from ebooks import auth, item

    app.register_blueprint(auth.bp)
    app.register_blueprint(item.bp)

    csp = {
        "default-src": [
            "'self'",
            "*.mit.edu",
            "*.mitlibrary.net",
            "*.bootstrapcdn.com",
            "*.cloudflare.com",
            "*.google-analytics.com",
            "*.googleapis.com",
            "*.gstatic.com",
            "*.jquery.com",
        ]
    }
    nonce_list = ["default-src", "script-src"]

    Talisman(
        app, content_security_policy=csp, content_security_policy_nonce_in=nonce_list
    )

    return app
