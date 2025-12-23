from app.config.appwrite import databases, DATABASE_ID

def sme_exists(sme_id):
    try:
        databases.get_document(DATABASE_ID, "smes", sme_id)
        return True
    except:
        return False
