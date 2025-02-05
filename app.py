import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.users_model import User
from models.customer_model import Customer
from models.product_model import Product
from models.project_model import Project
from models.installation_model import Installation
from models.stage_model import Stage
from models import db

from routes.auth import *
from routes.admin import *
from routes.support import *
from routes.technician import *

# set up Flas App
app = Flask(__name__)
app.config.from_object('utils.config.Config')
UPLOAD_FOLDER = "uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set up Db
db.init_app(app)
migrate = Migrate(app, db)


# Register your Routes
app.register_blueprint(index_bp) # This is / route
app.register_blueprint(login_bp) # This is /login route
app.register_blueprint(logout_bp) # This is /logout route
app.register_blueprint(admin_bp) # This is /admin route
app.register_blueprint(support_bp) # This is /support route
app.register_blueprint(technician_bp) # This is /technician route







# # add a default user
# with app.app_context():
#     if not User.query.filter_by(username='admin').first():
#         default_admin = User(
#         username='admin',
#         f_name="Victor",
#         l_name='Oluwatobi',
#         email='oluwatobi.akomolafe@oryoltd.com',
#         role='1',
#         )
#         default_admin.set_password('admin')
#         db.session.add(default_admin)
#         db.session.commit()
#         print("\n Default Admin User Created Successfully \n\n")

#     # Create tech support user
#     if not User.query.filter_by(username='demosupport').first():
#         default_support = User(
#         username='demosupport',
#         f_name="Demo",
#         l_name='Support',
#         email='support@oryoltd.com',
#         role='2',
#     )
#         default_support.set_password('demo123')
#         db.session.add(default_support)
#         db.session.commit()
#         print("\n Default support User Created Successfully\n\n ")


#     # Create techncian default 
#     if not User.query.filter_by(username='demotech').first():
#         default_support = User(
#         username='demotech',
#         f_name="Victor",
#         l_name='Oluwatobi',
#         email='technician@oryoltd.com',
#         role='3',
#     )
#         default_support.set_password('demo123')
#         db.session.add(default_support)
#         db.session.commit()
#         print("\n Default Technician User Created Successfully \n\n")


#     print("all default users has been created, \n\nApplication will now load...")



# Starts the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
