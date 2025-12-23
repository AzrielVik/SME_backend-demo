from app.config.appwrite import databases, DATABASE_ID
import uuid
from datetime import datetime

COLLECTION_ID = "health_flags"

class HealthFlag:
    def __init__(self, sme_id, period_label, flag_type, message):
        self.id = str(uuid.uuid4())
        self.sme_id = sme_id
        self.period_label = period_label
        self.flag_type = flag_type  # "warning" | "info"
        self.message = message
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
