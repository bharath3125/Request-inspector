from flask import Blueprint

proxy_bp = Blueprint("proxy", __name__)

@proxy_bp.route("/proxy")
def proxy():
    return "Proxy layer ready (future extension)"
  
