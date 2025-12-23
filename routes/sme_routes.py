from flask import Blueprint, request
from services.sme_service import create_sme

sme_bp = Blueprint("sme", __name__)

@sme_bp.route("/create", methods=["POST"])
def create():
    data = request.json

    sme = create_sme(
        business_name=data["businessName"],
        owner_name=data["ownerName"],
        user_id=data["userId"]
    )

    return {
        "success": True,
        "data": sme
    }
