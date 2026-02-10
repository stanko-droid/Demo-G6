from flask import Blueprint
import os

# Få sökvägen till admin mappen
admin_dir = os.path.dirname(os.path.abspath(__file__))

# Vi skapar blueprinten med rätt template och static folders
admin_bp = Blueprint(
    'admin_bp', 
    __name__, 
    url_prefix='/admin',
    template_folder=os.path.join(admin_dir, 'templates'),
    static_folder=os.path.join(admin_dir, 'static'),
    static_url_path='/admin/static'
)

# --- DET HÄR ÄR DEN VIKTIGASTE RADEN ---
# Om denna saknas ser inte Flask dina routes!
from application.admin import routes