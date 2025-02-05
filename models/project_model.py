from models import db
from models.customer_model import Customer


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    project_description = db.Column(db.String(255), nullable=False)