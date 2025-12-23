from app.config.appwrite import databases, DATABASE_ID
from datetime import datetime

# Appwrite collection IDs (set these in .env ideally)
MPESA_COLLECTION_ID = "mpesa_transactions"
CASH_COLLECTION_ID = "cash_daily_summary"
METRICS_COLLECTION_ID = "health_metrics"


def calculate_metrics(sme_id: str, period_type: str, period_label: str):
    """
    period_type: daily | weekly | monthly
    period_label: e.g. 2025-01-15 | 2025-W03 | 2025-01
    """

    # -------------------------------
    # 1. Fetch MPESA transactions
    # -------------------------------
    mpesa_docs = databases.list_documents(
        DATABASE_ID,
        MPESA_COLLECTION_ID,
        queries=[
            f'equal("sme_id", "{sme_id}")'
        ]
    )["documents"]

    mpesa_in = sum(
        doc["amount"] for doc in mpesa_docs
        if doc["transaction_type"] == "INFLOW"
    )

    mpesa_out = sum(
        doc["amount"] for doc in mpesa_docs
        if doc["transaction_type"] == "OUTFLOW"
    )

    # -------------------------------
    # 2. Fetch CASH daily summaries
    # -------------------------------
    cash_docs = databases.list_documents(
        DATABASE_ID,
        CASH_COLLECTION_ID,
        queries=[
            f'equal("sme_id", "{sme_id}")'
        ]
    )["documents"]

    cash_in = sum(doc["total_cash_in"] for doc in cash_docs)
    cash_out = sum(doc["total_cash_out"] for doc in cash_docs)

    # -------------------------------
    # 3. Totals
    # -------------------------------
    total_inflow = mpesa_in + cash_in
    total_outflow = mpesa_out + cash_out

    safe_total = total_inflow if total_inflow > 0 else 1

    mpesa_ratio = mpesa_in / safe_total
    cash_ratio = cash_in / safe_total

    # -------------------------------
    # 4. Store health_metrics
    # -------------------------------
    payload = {
        "sme_id": sme_id,
        "period_type": period_type,
        "period_label": period_label,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "mpesa_ratio": round(mpesa_ratio, 2),
        "cash_ratio": round(cash_ratio, 2)
    }

    databases.create_document(
        DATABASE_ID,
        METRICS_COLLECTION_ID,
        document_id="unique()",
        data=payload
    )

    return payload
