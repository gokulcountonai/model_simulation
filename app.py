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
    machine_details = db.fetch_machine_details()
    return jsonify(machine_details)

@app.route('/mills', methods=['GET'])
def get_mill_details():
    mill_details = db.fetch_mill_details()
    return jsonify(mill_details)

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    print(data)
    processed_data = preprocess_data(data)
    path = data['fileUpload']
    fps = data['fps']
    score = data['score']
    db.insert_validation_log(processed_data)
    if run_validation(path, fps,score):
        print(preprocess_data)
        return jsonify({"status": "success", "message": "Data inserted successfully"})
    else:
        return jsonify({"status": "error", "message": "Error inserting data"})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
