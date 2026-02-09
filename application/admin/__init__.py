from flask import Blueprint

# Vi skapar blueprinten
admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# --- DET HÄR ÄR DEN VIKTIGASTE RADEN ---
# Om denna saknas ser inte Flask dina routes!
from application.admin import routes