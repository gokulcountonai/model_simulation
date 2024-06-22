from flask import Flask, render_template, request, jsonify
from src.db import ProcessDB
from main import ImageProcessor

db = ProcessDB()
image_processor = ImageProcessor()

app = Flask(__name__)

def run_validation(path,fps,score):

    image_processor.score = score
    return image_processor.read_images(path,fps)


def preprocess_data(data):
    # Convert all keys to lowercase
    
    
    # Process each key individually
    for key in ['tp', 'fp', 'fda', 'report_availability']:
        if data.get(key) in [None, '', 'no']:
            data[key] = 2
        else:
            data[key] = 1
    return data


@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/machines', methods=['GET'])
def get_machine_details():
    mill_name = "BEST COLOR"
    print("MIl  name",mill_name)
    mill_data = db.fetch_mill_details_by_millname(mill_name)
    print(mill_data)
    print(type(mill_data))
    machine_details = db.fetch_machine_details(str(mill_data['mill_id']))
    return jsonify(machine_details)

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
    
    # Process the data (example: save to database, perform calculations, etc.)
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
    # processed_data = preprocess_data(data)
    print(data)
    path = data['fileUpload']
    fps = data['fps']
    score = data['score']
    db.insert_validation_log(data)
    run_validation(path,fps,score)
    # Assuming file needs to be saved
    if file_upload:
        filename = file_upload.filename
        file_upload.save(f"./uploads/{filename}")
        print(f"File {filename} uploaded successfully.")
    
    # Return a response
    return jsonify({"status": "success", "message": "Data inserted successfully"})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5021)
