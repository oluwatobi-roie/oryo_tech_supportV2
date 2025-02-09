import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid


# Helper function to convert "Yes" / "No" to boolean
def convert_to_boolean(value):
    if value == "Yes":
        return True
    elif value == "No":
        return False
    return value  # Return original value if it's not "Yes" or "No"



def save_uploaded_file(uploaded_file, folder="uploads"):
    if uploaded_file:
        file_ext = os.path.splitext(secure_filename(uploaded_file.filename))[1]  # Get file extension
        unique_id = uuid.uuid4().hex[:8]  # Generate unique identifier
        unique_filename = f"upload-{unique_id}{file_ext}"  # Force standard naming format

        upload_folder = os.path.join(current_app.root_path, folder)
        os.makedirs(upload_folder, exist_ok=True)  # Ensure folder exists
        file_path = os.path.join(upload_folder, unique_filename)
        
        uploaded_file.save(file_path)
        return f"/{folder}/{unique_filename}"  # Return relative file path

    return None


def all_field_types():
     # Define expected field types
    field_types = {
        "installation_id": "number",
        "product_id": "number",
        "support_user_id": "number",
        "technician_user_id": "number",
        "start_date": "datetime-local",
        "stage_id": "number",
        "device_imei": "number",
        "device_sim_serial": "number",
        "device_sim_phone": "number",
        "device_sim_seal": "number",
        "device_password": "text",
        "camera_imei": "number",
        "camera_sim_serial": "number",
        "camera_sim_phone": "number",
        "camera_seal_number": "number",
        "camera_password": "text",
        "fuel_sensor_1_mac": "text",
        "fuel_sensor_1_password": "text",
        "fuel_sensor_2_mac": "text",
        "fuel_sensor_2_password": "text",
        "add_gps_online": "checkbox",
        "location_check": "checkbox",
        "ignition_check": "checkbox",
        "external_battery": "checkbox",
        "camera_check": "checkbox",
        "fuel_1_check": "checkbox",
        "fuel_2_check": "checkbox",
        "plate_number": "text",
        "nick_name": "text",
        "driver_name": "text",
        "tank_1_capacity": "number",
        "tank_1_calibration_chart": "text",
        "tank_1_seal_number": "text",
        "tank_2_capacity": "number",
        "tank_2_calibration_chart": "text",
        "tank_2_seal_number": "text",
        "gps_install_pics": "file",
        "fuel_sensor_1_pics": "file",
        "fuel_sensor_2_pics": "file",
        "camera_install_pics": "file",
        "installation_date": "datetime-local",
        "pictures_confirmed": "checkbox",
        "flespi_linkage": "checkbox",
        "external_battery_alert": "checkbox",
        "idling_detect": "checkbox",
        "tank_1_current_volume": "number",
        "tank_2_current_volume": "number",
        "tank_1_drain_test_volume": "number",
        "tank_2_drain_test_volume": "number",
        "tank_1_refill_test_volume": "number",
        "tank_2_refill_test_volume": "number",
        "end_date": "datetime-local",
        "approval": "checkbox"
    }

    return field_types




