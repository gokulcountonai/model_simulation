from flask import Flask, render_template, request, jsonify
from src.db import ProcessDB
from main import ImageProcessor
import os
import os

db = ProcessDB()
image_processor = ImageProcessor()

app = Flask(__name__)

def run_validation(path,fps,score):

    image_processor.score = score
    return image_processor.read_images(path,fps)

def preprocess_data(data):
    for key in ['tp', 'fp', 'fda', 'report_availability']:
        if data.get(key) in [None, '', 'no']:
            data[key] = 2
        else:
            data[key] = 1
    return data


@app.route('/')
def index():
    return render_template('homepage.html')

# @app.route('/machines', methods=['GET'])
# def get_machine_details():
#     mill_name = "BEST COLOR"
#     print("MIl  name",mill_name)
#     mill_data = db.fetch_mill_details_by_millname(mill_name)
#     print(mill_data)
#     print(type(mill_data))
#     machine_details = db.fetch_machine_details(str(mill_data['mill_id']))
#     return jsonify(machine_details)


@app.route('/machines_by_mill/<mill_name>', methods=['GET'])
def get_machines_by_mill(mill_name):
    if mill_name:
        # print(mill_name)
        machine_details = db.fetch_machine_details_by_mill_name(mill_name)
        return jsonify(machine_details)
    return jsonify([])

@app.route('/mills', methods=['GET'])
def get_mill_details():
    mill_details = db.fetch_mill_details()
    return jsonify(mill_details)


@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    # Fetch form data
    mill_name = request.form.get('mill')
    machine_name = request.form.get('machine')
    simulation_type = request.form.get('validationType')
    folder_path = request.form.get('folderpath')
    file_upload = request.files['fileUpload']
    score = request.form.get('score')
    fps = request.form.get('fps')
    report = request.form.get('report')
    
    # For now, just print it
    data = {
        "mill": mill_name,
        "machine": machine_name,
        "simulation_type": simulation_type,
        "score": score,
        "fps": fps,
        "report_availability": report,
        "fileUpload": file_upload,
        "folderpath": folder_path
    }
    # print(data)
    print(data)
    path = data['fileUpload']
    fps = data['fps']
    score = data['score']
    db.insert_validation_log(data)
    # Assuming file needs to be saved
    if file_upload:
        filename = "reg"

        # Delete all files in the directory
        file_list = os.listdir("./uploads")
        for file_name in file_list:
            file_path = os.path.join("./uploads", file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        file_upload.save(f"./uploads/{filename}")
        print(f"File {filename} uploaded successfully.")
    
    # Return a response
    return jsonify({"status": "success", "message": "Data inserted successfully"})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50211)
