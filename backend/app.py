from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

# Import your file-processing functions
from excel import excel_main
from ppt import ppt_main
from new_pdf import pdf_main
from image import image_file_description_and_keyfindings

# Flask app setup
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Node frontend
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "ppt", "pptx", "xls", "xlsx", "jpg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Test route to check server
@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

# Upload route
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    ext = filename.rsplit(".", 1)[1].lower()
    try:
        if ext == "pdf":
            file_description, key_findings = pdf_main(filepath)
            file_type = "PDF"
        elif ext in ["ppt", "pptx"]:
            file_description, key_findings = ppt_main(filepath)
            file_type = "PPT"
        elif ext in ["xls", "xlsx"]:
            file_description, key_findings = excel_main(filepath)
            file_type = "Excel"
        elif ext in ["jpg", "png"]:
            file_description, key_findings = image_file_description_and_keyfindings(filepath)
            file_type = "Image"
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        
        print("DEBUG: JSON to send:", {
    "filename": filename,
    "file_type": file_type,
    "file_description": file_description,
    "key_findings": key_findings
})


        return jsonify({
            "filename": filename,
            "file_type": file_type,
            "file_description": file_description,
            "key_findings": key_findings
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
