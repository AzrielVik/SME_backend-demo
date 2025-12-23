from app.config.appwrite import databases, DATABASE_ID
import uuid
from datetime import datetime

COLLECTION_ID = "health_metrics"

class HealthMetric:
    def __init__(
        self,
        sme_id,
        period_type,  # "daily" | "monthly"
        period_label, # "2025-09-18" or "2025-09"
        total_inflow,
        total_outflow,
        mpesa_ratio,
        cash_ratio
    ):
        self.id = str(uuid.uuid4())
        self.sme_id = sme_id
        self.period_type = period_type
        self.period_label = period_label
        self.total_inflow = total_inflow
        self.total_outflow = total_outflow
        self.mpesa_ratio = mpesa_ratio
        self.cash_ratio = cash_ratio
        self.created_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return self.__dict__

    def save(self):
        return databases.create_document(
            database_id=DATABASE_ID,
            collection_id=COLLECTION_ID,
            document_id=self.id,
            data=self.to_dict()
        )
