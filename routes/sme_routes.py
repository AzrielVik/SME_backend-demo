from flask import Blueprint, request, jsonify
from app.config.appwrite import databases, DATABASE_ID
import uuid
from datetime import datetime

sme_bp = Blueprint("sme", __name__, url_prefix="/smes")


@sme_bp.route("", methods=["POST"])
def create_sme():
    """
    Register a new SME (business).
    This is the FIRST step in the system.
    """

    try:
        data = request.get_json()

        required_fields = ["name", "owner_name", "phone"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing field: {field}"
                }), 400

        sme_id = str(uuid.uuid4())

        document = databases.create_document(
            DATABASE_ID,
            "smes",
            sme_id,
            {
                "name": data["name"],
                "owner_name": data["owner_name"],
                "phone": data["phone"],
                "created_at": datetime.utcnow().isoformat()
            }
        )

        return jsonify({
            "success": True,
            "data": document
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@sme_bp.route("/<sme_id>", methods=["GET"])
def get_sme(sme_id):
    """
    Fetch SME profile by ID
    """

    try:
        document = databases.get_document(
            DATABASE_ID,
            "smes",
            sme_id
        )

        return jsonify({
            "success": True,
            "data": document
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": "SME not found"
        }), 404


@sme_bp.route("", methods=["GET"])
def list_smes():
    """
    List all SMEs (admin / debug / future multi-business dashboards)
    """

    try:
        result = databases.list_documents(
            DATABASE_ID,
            "smes"
        )

        return jsonify({
            "success": True,
            "data": result["documents"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
