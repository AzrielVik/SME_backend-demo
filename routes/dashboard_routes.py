from flask import Blueprint, jsonify
from app.config.appwrite import databases, DATABASE_ID

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/summary/<sme_id>")
def dashboard_summary(sme_id):
    scores = databases.list_documents(
        DATABASE_ID,
        "health_scores"
    )
    return jsonify({
        "success": True,
        "data": scores["documents"]
    })
