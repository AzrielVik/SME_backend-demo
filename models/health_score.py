from app.config.appwrite import databases, DATABASE_ID
import uuid
from datetime import datetime

COLLECTION_ID = "health_scores"

class HealthScore:
    def __init__(
        self,
        sme_id,
        period_type,
        period_label,
        score,
        status  # "healthy" | "moderate" | "risky"
    ):
        self.id = str(uuid.uuid4())
        self.sme_id = sme_id
        self.period_type = period_type
        self.period_label = period_label
        self.score = score
        self.status = status
        self.created_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return self.__dict__

    def save(self):
        return databases.create_document(
            DATABASE_ID,
            COLLECTION_ID,
            self.id,
            self.to_dict()
        )
