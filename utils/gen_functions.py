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
