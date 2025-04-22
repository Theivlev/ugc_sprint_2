from http import HTTPStatus

import sentry_sdk
from src.api.analytics_api import bp as analytics_bp
from src.core.config import sentry_settings
from src.core.logger import request_id_var

from flask import Flask, jsonify, request

sentry_sdk.init(dsn=sentry_settings.dsn, traces_sample_rate=1.0)

app = Flask(__name__)
app.register_blueprint(analytics_bp)


@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        return jsonify({"detail": "X-Request-Id is required"}), HTTPStatus.BAD_REQUEST
    request_id_var.set(request_id)


@app.after_request
def after_request(response):
    request_id = request_id_var.get()
    if request_id:
        response.headers["X-Request-Id"] = request_id
    request_id_var.set(None)
    return response


if __name__ == "__main__":
    app.run()
