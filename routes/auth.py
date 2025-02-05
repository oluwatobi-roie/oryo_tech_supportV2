from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from models.users_model import User
from werkzeug.security import check_password_hash



index_bp = Blueprint('index', __name__)
login_bp = Blueprint('login', __name__, template_folder='../templates')
logout_bp = Blueprint('logout', __name__)


# redirect all index url back to login page. 
@index_bp.route('/')
def index():
    # return render_template('logout.html')
    return redirect(url_for('login.login')) # when user loads the app, they are redirected to login page. 


# login route to handle all login request and checks if session currently exist
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_role' in session:
        user_role = session['user_role']
        if user_role == 1:
            return redirect(url_for('admin.admin'))
        elif user_role == 2:
            return redirect(url_for('support.support'))
        elif user_role == 3:
            return redirect(url_for('technician.technician'))

    if request.method == 'POST':
        # receive  the user name and password from the form passed     
        form_username = request.form['username']
        form_password = request.form['password']

        logged_user = User.query.filter_by(username=form_username).first()
        if logged_user:
            if check_password_hash(logged_user.password_hash, form_password):
                # save login details to session, and reload the login page
                session['user_id'] = logged_user.user_id
                session['user_role'] = logged_user.role
                session.modified = True # session wasnt getting saved, hence forcing flask to make the save. 
                return redirect(url_for("login.login"))
            else:
             flash('Incorrect Password, Please try again', 'danger')
        else:
            flash('Incorrect Username, Please try again', 'danger')
        

    return render_template('login.html')



# Logout to clear session and return user back to login page. 
@logout_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index.index'))
