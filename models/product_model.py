from models import db

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(30), nullable=False)
    product_description = db.Column(db.String(255), nullable=False)
    product_fields = db.Column(db.JSON, nullable=False) 