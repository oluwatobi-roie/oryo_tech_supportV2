# all activities around admin activities happens here
import inspect
import os
from flask import Blueprint, json, jsonify, redirect, render_template, request,  session, url_for, flash
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import selectinload
from functools import wraps
from .auth import logout
from models.project_model import Project
from models.product_model import Product
from models.users_model import User
from models.installation_model import Installation
from models.customer_model import Customer
from models.stage_model import Stage
from models import db
from datetime import datetime
from utils.gen_functions import save_uploaded_file, convert_to_boolean, all_field_types

support_bp = Blueprint('support', __name__, template_folder='../templates', url_prefix='/support')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 2:
            flash("You must be logged in as a support staff to access this page.", "danger")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function


def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in as a support staff to access this page.", "danger")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function


# root file for support 
@support_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def support():
    try:
        if request.method == 'GET':
            installations = Installation.query.filter(Installation.stage_id.in_([1, 2, 4])).all()
            return render_template('support-dashboard.html', installations = installations)
        
    except Exception as e:
        return redirect(url_for(logout))
    


# add task for support
@support_bp.route('/addtask', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
@session_required
def addTask():
    try:
        # Populate entried to help select vehicles lists
        if request.method == 'GET':
            projects = Project.query.all()
            clients = Customer.query.all()
            users = User.query.filter_by(role=3).all()
            products = Product.query.all()


            # installations = Installation.query.filter_by(stage=1).all()
            installations = (
                db.session.query(Installation)
                .filter(Installation.stage_id == 1)
                .options(
                    selectinload(Installation.project),
                    selectinload(Installation.product),
                    selectinload(Installation.technician),
                    selectinload(Installation.stage)
                ).all()
            )
            return render_template ('addtask.html', projects=projects, clients=clients, users=users, products=products, installations=installations)
        
        if request.method == 'POST':
            data = request.json # Ensure JSON is received

            print("Data from Front End: ", data) #Debugging
            if not data:
                return jsonify({"error": "No JSON data received"}), 400
            
            # extract all column name from the installation table
            empty_entry = [key for key, value in data.items() if not value]

            if empty_entry:
                return jsonify({"error": f"Missing values for: {', '. join(empty_entry)}"}), 400
            installation_columns = {col.name for col in inspect(Installation).columns}
            installation_data = {
                key: value for key, value in data.items() if key in installation_columns
            }

            # add other detals to the installation data. 
            installation_data["support_user_id"] = session.get('user_id')
            installation_data["start_date"] = datetime.now()
            print("\n\n\n\n\nform_data : ", installation_data)


            # Create a new Installation Task
            new_task = Installation(**installation_data) #unpacking a dictionary to database

            db.session.add(new_task)
            db.session.commit()

            return jsonify({"message": "Installation Task Created Successfully!"}), 201

        if request.method == 'PUT':
            # Determine how data is sent
            if request.content_type == "application/json":
                data = request.json  # JSON request (no files)
                files = {}
            else:
                data = request.form.to_dict()  # Form data (files included)
                files = request.files  # File uploads

            # Debugging Output
            print("Data from Front End:", data)
            print("Files received:", files)

            if not data:
                return jsonify({"error": "No data received"}), 400

            installation_id = data.get('installation_id')
            if not installation_id:
                return jsonify({'error': 'Installation ID required'}), 400

            installation = Installation.query.get(installation_id)
            if not installation:
                return jsonify({'error': 'Installation ID not found'}), 400

            failed_fields = []  # Track fields that failed validation

            # Process JSON/Form fields
            for key, value in data.items():
                if hasattr(installation, key):
                    if isinstance(getattr(installation, key), bool):
                        value = convert_to_boolean(value)

                    if isinstance(value, bool) and not value:
                        failed_fields.append(key)

                    setattr(installation, key, value)

            # Handle file uploads (save and store file paths)
            for key, uploaded_file in files.items():
                if uploaded_file and uploaded_file.filename:  # If file is uploaded
                    file_url = save_uploaded_file(uploaded_file)
                    setattr(installation, key, file_url)  # Save file URL in DB

            # Handle stage progression
            if not failed_fields:
                if 'stage_id' in data:
                    installation.stage_id = int(data['stage_id']) + 1
                my_message = "Task Updated successfully. Ready for Deployment"
            else:
                installation.stage_id = 1
                my_message = f"Task Failed to move to next stage because the following fields: {failed_fields} were labeled false"

            db.session.commit()
            return jsonify({"message": my_message}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400




@support_bp.route('/addtask/get_product_fields/<int:product_id>/<int:stage_id>', methods=['GET'])
@session_required
def get_product_fields(product_id,stage_id):
    product = Product.query.get(product_id)
    stage = Stage.query.get(stage_id)

    if not product or not product.product_fields:
        return jsonify({'fields' : []})
        
    fields = all_field_types()

    # This is strictly for profile viewing, we naturally set profile to be 0 so as to target this funciton.
    if stage_id == 0:
        # Return all fields for this product type
        all_product_fields = product.product_fields
        edit_fields = {field: fields.get(field, "string") for field in all_product_fields}
        return jsonify({'fields': edit_fields})
    

    if product and product.product_fields and stage.stage_fields:
        try:
            product_fields = product.product_fields
            stage_fields = (stage.stage_fields)
        

                # edit_fields = list(set(stage_fields) & set(product_fields))
            edit_fields = {field: fields.get(field, "string") for field in set(stage_fields) & set(product_fields)}

            return jsonify({'fields': edit_fields})
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return jsonify({'fields': []})  # Return empty if no fields found




# this helps display an installation profile, we are 
@support_bp.route('/installation-profile/<int:installation_id>', methods=['GET'])
@login_required
def profile(installation_id):
    installation = Installation.query.get(installation_id)

    if not installation:
        return jsonify({"error": "Installation not found"}), 404


    product = installation.product_id
    get_product_fields(product, 0)
    product_fields_response = get_product_fields(product, 0)
    product_fields = product_fields_response.get_json().get("fields", {})
    product_data = {field: getattr(installation, field, "N/A") for field in product_fields.keys()}

    return jsonify(product_data)
