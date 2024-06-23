from flask import Flask, render_template, request, jsonify
from src.db import ProcessDB
from main import ImageProcessor
import os,time

db = ProcessDB()
image_processor = ImageProcessor()

app = Flask(__name__)

def run_validation(path,fps,score):
    image_processor.path = path
    image_processor.score = float(score)
    return image_processor.read_images(path,fps)

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

@app.route('/add-machine', methods=['POST'])
def add_machine():
    data = request.json
    print(data)
    mill_name = data.get('mill_name')
    machine_name = data.get('machine_name')
    if not mill_name or not machine_name:
        return jsonify({"status": "error", "message": "Please provide both mill name and machine name."}), 400

    # Fetch mill_id for the given mill_name
    mill_id = db.fetch_mill_details_by_millname(str(mill_name))
    if not mill_id:
        return jsonify({"status": "error", "message": "Mill name not found.Please ADD the mill first."}), 400

    # Insert machine details
    data = {
        "machine_name": machine_name,
        "mill_id": mill_id["mill_id"]
    }
    db.add_machine(data)

    return jsonify({"status": "success", "message": "Machine added successfully."})


@app.route('/machines_details', methods=['GET'])
def machines_details():
    return render_template('machines.html')

@app.route('/view-machines', methods=['GET'])
def view_machines():
    return jsonify(db.fetch_machine_details())


@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    # Extract form data
    mill_name = request.form.get('mill')
    machine_name = request.form.get('machine')
    simulation_type = request.form.get('validationType')
    folder_path = request.form.get('folderpath')
    file_upload = request.files['fileUpload']
    score = request.form.get('score')
    fps = request.form.get('fps')
    report = request.form.get('report')

    print("Mill Name",mill_name)
    print("Machine Name",machine_name)
    print("Simulation Type",simulation_type)
    print("Folder Path",folder_path)
    print("File Upload",file_upload)
    print("Score",score)
    print("FPS",fps)
    print("Report",report)

    # Validate score and fps ranges
    try:
        print("Score",score)
        print("FPS",fps)
        score_float = float(score)
        fps_float = float(fps)

        if not (0 <= score_float <= 1.0):
            return jsonify({"status": "error", "message": "Score must be between 0 and 1."}), 400
        
        if not (10 <= fps_float <= 40):
            return jsonify({"status": "error", "message": "FPS must be between 10 and 40."}), 400

    except ValueError:
        return jsonify({"status": "error", "message": "Invalid score or fps value."}), 400

    # Prepare data for database insertion
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

    # Insert data into database
    db.insert_validation_log(data)
    # Assuming file needs to be saved
    if file_upload:
        filename = "reg"

        # # Delete all files in the directory
        # file_list = os.listdir("./uploads")
        # for file_name in file_list:
        #     file_path = os.path.join("./uploads", file_name)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)

        file_upload.save(f"./uploads/{filename}")
        print(f"File {filename} uploaded successfully.")

        with open('simulation/simulation.txt', 'w') as f:
            f.write("1")
        time.sleep(5)
        # Run validation
        run_validation(folder_path, fps, score)
        
    
    # Return a response
    return render_template('homepage.html')
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
