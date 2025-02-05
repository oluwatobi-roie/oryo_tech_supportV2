from models import db

class Stage(db.Model):
    stage_id = db.Column(db.Integer, primary_key=True)
    stage_name = db.Column(db.String(30), nullable=False)
    stage_description = db.Column(db.String(255), nullable=False)
    stage_fields = db.Column(db.JSON, nullable=False)
    stage_next = db.Column(db.String(30), nullable=True)