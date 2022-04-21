from flask import Blueprint

proxy_bp = Blueprint("proxy_bp", __name__, url_prefix="/proxy")


def check_login():
    pass


proxy_bp.before_request(check_login)
