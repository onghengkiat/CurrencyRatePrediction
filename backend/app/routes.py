from app import app
from flask import request, jsonify
from app.util import cors_allow, missing_param_handler
import pandas as pd

@app.route("/dashboard")
@cors_allow
@missing_param_handler
def get_dashboard():
    # df = pd.read_csv("")
    return jsonify({"message":"Something wrong occurs"}), 400
