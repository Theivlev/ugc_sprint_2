from src.services.analytics_service import Analytics

from flask import Blueprint

bp = Blueprint("analytics", __name__, url_prefix="/analytics")

bp.add_url_rule("/load-auth-history", view_func=Analytics.load_auth_history, methods=["POST"])

bp.add_url_rule("/load-lead-rating", view_func=Analytics.load_lead_rating, methods=["POST"])
