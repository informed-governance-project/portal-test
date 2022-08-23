from flask import Blueprint
from flask import jsonify

# about_bp
about_bp = Blueprint("about_bp", __name__, url_prefix="/about")


@about_bp.route("/test", methods=["GET"])
def test():
    """Documentation page."""
    return jsonify({"status": "OK"})
