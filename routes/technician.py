# all activities around admin activities happens here
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from functools import wraps
from models.installation_model import Installation
from .auth import logout

technician_bp = Blueprint('technician', __name__, template_folder='../templates', url_prefix='/technician')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 3:
            flash("You must be logged in as an on-site technical staff to access this page.", "danger")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function


@technician_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def technician():
    try:
        if request.method == 'GET':
            user_id = session.get('user_id')

            if not user_id:
                return redirect(url_for('login.login'))

            installations = Installation.query.filter(
                Installation.stage_id == 3,
                Installation.technician_user_id == user_id).all()
            

            return render_template('technician-dashboard.html', installations = installations)
    
    except Exception as e:
        return redirect(url_for(logout))