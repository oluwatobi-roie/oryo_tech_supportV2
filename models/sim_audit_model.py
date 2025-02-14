from datetime import datetime
from models import db
from models.product_model import Product
from models.users_model import User
from models.stage_model import Stage
from models.project_model import Project


class Installation(db.Model):
    audit_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False, index=True)
    support_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    technician_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False, index=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.stage_id'), default=1, index=True) # other stages are table Test, Ready for Installation, Awaiting Approval, Completed, 
    location = db.Column(db.String(255))
    device_imei = db.Column(db.String(50), unique=True, index=True)
    device_sim_serial = db.Column(db.String(50), unique=True)
    device_sim_phone = db.Column(db.String(20), unique=True, index=True)

    
    camera_imei = db.Column(db.String(50), unique=True, index=True)
    camera_sim_serial = db.Column(db.String(50), unique=True)
    camera_sim_phone = db.Column(db.String(20), unique=True, index=True)
    camera_seal_number = db.Column(db.String(50), unique=True)
    camera_password = db.Column(db.String(50))
     
    plate_number = db.Column(db.String(50))

    gps_imei_pics = db.Column(db.String(255))
    gps_sim_serial_pics = db.Column(db.String(255))
    gps_sim_phone_pics = db.Column(db.String(255))

    camera_imei_pics = db.Column(db.String(255))
    camera_sim_serial_pics = db.Column(db.String(255))
    camera_sim_phone_pics = db.Column(db.String(255))

    pictures_confirmed = db.Column(db.Boolean, default=False)

    approval_date = db.Column(db.DateTime)

    end_date = db.Column(db.DateTime)
    approval = db.Column(db.Boolean, default=False)


    project = db.relationship("Project", backref="installations", lazy="joined")
    product = db.relationship("Product", backref="installations", lazy="joined")
    technician = db.relationship("User", backref="technician_tasks", lazy="joined", foreign_keys=[technician_user_id])
    support = db.relationship("User", backref="support_tasks", lazy="joined", foreign_keys=[support_user_id])
    stage = db.relationship("Stage", backref="installations", lazy="joined")