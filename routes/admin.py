# all activities around admin activities happens here
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for, flash
from functools import wraps
from models import db
from models.customer_model import Customer
from models.project_model import Project
from models.product_model import Product


admin_bp = Blueprint('admin', __name__, template_folder='../templates', url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 1:
            flash("You must be logged in as an admin to access this page.", "danger")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def admin():
    return render_template('admin-dashboard.html')




@admin_bp.route('/customer', methods=['POST', 'GET'])
@login_required
def manage_customer():

    try:
        # Display all customer
        if request.method == 'GET':
            customers = Customer.query.all()
            return render_template('admin-customers.html', customers=customers)
        

        # To create a customer
        elif request.method == 'POST':
            if request.form:
                customer_name = request.form.get('customer_name')
                customer_address = request.form.get('customer_address')
                if not customer_name or not customer_address:    
                    flash("Mission required fields", 'danger')
                    return redirect(url_for('admin.manage_customer'))
            
            new_customer = Customer(
                customer_name = customer_name,
                customer_address = customer_address
            )

            db.session.add(new_customer)
            db.session.commit()

            flash("customer Created Successfully", 'success')
            return redirect(url_for('admin.manage_customer'))
        


    # Error Catching
    except Exception as e:
        db.session.rollback()
        flash("Error occured somewhere", str(e))
        return redirect(url_for('admin.manage_customer'))
    



# this helps us with assigning projects, we are only using post method now, we will have a route to manage project
# this is expected to support all CRUD operation in the project modal class
@admin_bp.route('/projects', methods=['POST', 'GET'])
@login_required
def manage_project():
    try:
        if request.method == 'GET':
            customers = Customer.query.all()
            customer_list = [{'id': customer.customer_id, 'name': customer.customer_name} for customer in customers]
            return jsonify(customer_list)
        
        elif request.method == 'POST':
            if request.form:
                customer_id = request.form.get('customer_id')
                project_description = request.form.get('project_description')
                if not customer_id or not project_description:
                    flash ("you need to assign project to a client", "danger")
                    return redirect(url_for('admin.admin'))
            new_project = Project(
                client_id = customer_id,
                project_description = project_description
            )
            db.session.add(new_project)
            db.session.commit()
            flash("Project Created Successfully", 'success')
            return redirect(url_for('admin.admin'))
    
    except Exception as e:
        db.session.rollback()
        flash("Error occured somewhere", str(e))
        return redirect(url_for('admin.admin'))


# this helps us with assigning products, we are only using post method now, we will have a route to manage project
# this is expected to support all CRUD operation in the product modal class
@admin_bp.route('/product', methods=['POST', 'GET'])
@login_required
def manage_product():
    try:
        
        if request.method == 'GET':
            products = Product.query.all()
            product_list = [{'id': Product.product_id, 'desciption': Product.product_description, 'fields': Product.product_fields} for product in products]
            return jsonify(product_list)
        
        elif request.method == 'POST':
            if request.form:
                print("\n\n we have a response form data")
                product_name = request.form.get('product_name', '').strip()
                product_description = request.form.get('product_description', '').strip()
                product_fields = request.form.get('product_fields', '').strip()
                print (product_name)
                print (product_description)
                print (product_fields)
                if not product_name or not product_description or not product_fields:
                    flash ("some items were not entered correctly", "danger")
                    return redirect(url_for('admin.admin'))
            new_product = Product(
                product_name = product_name,
                product_description = product_description,
                product_fields = product_fields,
            )
            db.session.add(new_product)
            db.session.commit()
            flash("Product Created Successfully", 'success')
            return redirect(url_for('admin.admin'))
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error occured somewhere: {str(e)}", 'error')
        return redirect(url_for('admin.admin'))
