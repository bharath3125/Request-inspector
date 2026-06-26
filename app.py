import os
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.hybrid_waf.routes.main import main_bp
from src.hybrid_waf.routes.proxy import proxy_bp

from src.hybrid_waf.utils.signature_checker import check_signature
from src.hybrid_waf.utils.ml_detector import ml_check

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per hour", "100 per minute"],
    storage_uri="memory://"
)

app.register_blueprint(main_bp)
app.register_blueprint(proxy_bp)


@app.before_request
def waf_middleware():

    if not request.headers.get('User-Agent') or not request.headers.get('Host'):
        abort(400, "Missing headers")

    if request.path.startswith("/static"):
        return

    raw_query = request.query_string.decode("utf-8", errors="ignore")
    raw_path = request.path
    body_data = request.get_data(as_text=True) if request.content_length else ""

    combined_input = f"{raw_path} {raw_query} {body_data}"

    sig_result, sig_score = check_signature(combined_input)
    ml_result, ml_score = ml_check(combined_input)

    if sig_result == "malicious" or ml_result == "malicious":
        abort(403, f"Blocked by WAF | ML Score: {ml_score}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
