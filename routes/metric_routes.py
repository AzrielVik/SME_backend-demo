from flask import Blueprint, jsonify
from services.metric_service import calculate_metrics

metric_bp = Blueprint("metrics", __name__, url_prefix="/metrics")

@metric_bp.route("/preview", methods=["POST"])
def preview_metrics():
    transactions = []  # frontend sends transactions payload
    metrics = calculate_metrics(transactions)
    return jsonify({"success": True, "data": metrics})
