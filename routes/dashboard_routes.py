from flask import Blueprint, jsonify
from app.config.appwrite import databases, DATABASE_ID
from services.metric_service import calculate_metrics
from services.scoring_service import generate_score, generate_flags
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/summary/<sme_id>", methods=["GET"])
def dashboard_summary(sme_id):
    """
    Main dashboard orchestrator.
    Pulls transactions, computes metrics, score, flags,
    and returns a single clean payload to the frontend.
    """

    try:
        # ----------------------------
        # 1. Fetch MPESA transactions
        # ----------------------------
        mpesa_docs = databases.list_documents(
            DATABASE_ID,
            "mpesa_transactions",
            queries=[]
        )["documents"]

        mpesa_transactions = [
            {
                "amount": doc["amount"],
                "type": "in" if doc["transaction_type"] == "INFLOW" else "out",
                "source": "mpesa"
            }
            for doc in mpesa_docs
            if doc["sme_id"] == sme_id
        ]

        # ----------------------------
        # 2. Fetch CASH summaries
        # ----------------------------
        cash_docs = databases.list_documents(
            DATABASE_ID,
            "cash_transactions",
            queries=[]
        )["documents"]

        cash_transactions = []
        for doc in cash_docs:
            if doc["sme_id"] == sme_id:
                cash_transactions.append({
                    "amount": doc["total_cash_in"],
                    "type": "in",
                    "source": "cash"
                })
                cash_transactions.append({
                    "amount": doc["total_cash_out"],
                    "type": "out",
                    "source": "cash"
                })

        # ----------------------------
        # 3. Merge transactions
        # ----------------------------
        all_transactions = mpesa_transactions + cash_transactions

        # ----------------------------
        # 4. Calculate metrics
        # ----------------------------
        metrics = calculate_metrics(all_transactions)

        # ----------------------------
        # 5. Generate score + status
        # ----------------------------
        score, status = generate_score(metrics)

        # ----------------------------
        # 6. Generate flags
        # ----------------------------
        flags = generate_flags(metrics)

        # ----------------------------
        # 7. Persist score (optional but recommended)
        # ----------------------------
        databases.create_document(
            DATABASE_ID,
            "health_scores",
            document_id="unique()",
            data={
                "sme_id": sme_id,
                "period_type": "daily",
                "period_label": datetime.utcnow().strftime("%Y-%m-%d"),
                "score": score,
                "status": status
            }
        )

        # ----------------------------
        # 8. Return clean dashboard payload
        # ----------------------------
        return jsonify({
            "success": True,
            "data": {
                "metrics": metrics,
                "health_score": {
                    "score": score,
                    "status": status
                },
                "flags": [
                    {"type": f[0], "message": f[1]} for f in flags
                ]
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
