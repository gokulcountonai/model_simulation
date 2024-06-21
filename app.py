from flask import Flask, render_template, request, jsonify
from src.db import ProcessDB
from main import ImageProcessor

image_processor = ImageProcessor()

app = Flask(__name__)

# def validation_log(data):
#     query  = f"INSERT INTO validation_log (data) VALUES ('{data}')"

def run_validation(path,fps,score):

    image_processor.score = score
    return image_processor.read_images(path,fps)

@app.route('/')
def index():
    image_processor.score = 0.1
    return render_template('homepage.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    path = data['path']
    fps = data['fps']
    run_validation(path, fps)
    
    

    return jsonify({'message': 'Data received successfully'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
