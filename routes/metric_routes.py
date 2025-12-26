from flask import Blueprint, jsonify, request
from services.metric_service import calculate_metrics

metric_bp = Blueprint("metrics", __name__, url_prefix="/metrics")


@metric_bp.route("/preview", methods=["POST"])
def preview_metrics():
    """
    Preview endpoint.
    Accepts a list of transactions from the frontend
    and returns calculated metrics WITHOUT saving anything.
    """

    try:
        payload = request.get_json()

        if not payload or "transactions" not in payload:
            return jsonify({
                "success": False,
                "error": "Missing transactions payload"
            }), 400

        transactions = payload["transactions"]

        metrics = calculate_metrics(transactions)

        return jsonify({
            "success": True,
            "data": metrics
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
