from flask import Blueprint
from flask import jsonify

client_bp = Blueprint("client_bp", __name__, url_prefix="/client")


@client_bp.route("/login", methods=["GET"])
def index():
    return jsonify({"result": "ok"})
