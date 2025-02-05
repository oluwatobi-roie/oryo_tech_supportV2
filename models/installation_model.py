from datetime import datetime
from models import db
from models.product_model import Product
from models.users_model import User
from models.stage_model import Stage
from models.project_model import Project


class Installation(db.Model):
    installation_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False, index=True)
    support_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    technician_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False, index=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.stage_id'), default=1, index=True) # other stages are table Test, Ready for Installation, Awaiting Approval, Completed, 
    
    device_imei = db.Column(db.String(50), unique=True, index=True)
    device_sim_serial = db.Column(db.String(50), unique=True)
    device_sim_phone = db.Column(db.String(20), unique=True, index=True)
    device_sim_seal = db.Column(db.String(50), unique=True)
    device_password = db.Column(db.String(50))
    
    camera_imei = db.Column(db.String(50), unique=True, index=True)
    camera_sim_serial = db.Column(db.String(50), unique=True)
    camera_sim_phone = db.Column(db.String(20), unique=True, index=True)
    camera_seal_number = db.Column(db.String(50), unique=True)
    camera_password = db.Column(db.String(50))
    
    fuel_sensor_1_mac = db.Column(db.String(50), unique=True)
    fuel_sensor_1_password = db.Column(db.String(50))
    fuel_sensor_2_mac = db.Column(db.String(50), unique=True)
    fuel_sensor_2_password = db.Column(db.String(50))
    
    add_gps_online = db.Column(db.Boolean, default=False)
    location_check = db.Column(db.Boolean, default=False)
    ignition_check = db.Column(db.Boolean, default=False)
    external_battery = db.Column(db.Boolean, default=False)
    
    camera_check = db.Column(db.Boolean, default=False)
    fuel_1_check = db.Column(db.Boolean, default=False)
    fuel_2_check = db.Column(db.Boolean, default=False)

    plate_number = db.Column(db.String(50))
    nick_name = db.Column(db.String(50))
    driver_name = db.Column(db.String(100))
    
    tank_1_capacity = db.Column(db.Float)
    tank_1_calibration_chart = db.Column(db.String(255))
    tank_1_seal_number = db.Column(db.String(50))
    
    tank_2_capacity = db.Column(db.Float)
    tank_2_calibration_chart = db.Column(db.String(255))
    tank_2_seal_number = db.Column(db.String(50))
    
    gps_install_pics = db.Column(db.String(255))
    fuel_sensor_1_pics = db.Column(db.String(255))
    fuel_sensor_2_pics = db.Column(db.String(255))
    camera_install_pics = db.Column(db.String(255))
    pictures_confirmed = db.Column(db.Boolean, default=False)

    installation_date = db.Column(db.DateTime)
    flespi_linkage = db.Column(db.String(255))
    
    external_battery_alert = db.Column(db.Boolean, default=False)
    idling_detect = db.Column(db.Boolean, default=False)

    tank_1_current_volume = db.Column(db.Float)
    tank_2_current_volume = db.Column(db.Float)
    tank_1_drain_test_volume = db.Column(db.Float)
    tank_2_drain_test_volume = db.Column(db.Float)
    tank_1_refill_test_volume = db.Column(db.Float)
    tank_2_refill_test_volume = db.Column(db.Float)

    end_date = db.Column(db.DateTime)
    approval = db.Column(db.Boolean, default=False)


    project = db.relationship("Project", backref="installations", lazy="joined")
    product = db.relationship("Product", backref="installations", lazy="joined")
    technician = db.relationship("User", backref="technician_tasks", lazy="joined", foreign_keys=[technician_user_id])
    support = db.relationship("User", backref="support_tasks", lazy="joined", foreign_keys=[support_user_id])
    stage = db.relationship("Stage", backref="installations", lazy="joined")