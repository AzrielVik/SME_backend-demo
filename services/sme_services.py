from config.appwrite import databases, DATABASE_ID
from models.sme import SME_COLLECTION
import uuid
from datetime import datetime

def create_sme(business_name, owner_name, user_id):
    return databases.create_document(
        database_id=DATABASE_ID,
        collection_id=SME_COLLECTION,
        document_id=str(uuid.uuid4()),
        data={
            "business_name": business_name,
            "owner_name": owner_name,
            "created_by": user_id,
            "created_at": datetime.utcnow().isoformat()
        }
    )
