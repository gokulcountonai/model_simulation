from flask import Flask, render_template, request, jsonify
from src.db import DatabaseAPI
from main import ImageProcessor

image_processor = ImageProcessor()

app = Flask(__name__)

def validation_log(data):
    query  = f"INSERT INTO validation_log (data) VALUES ('{data}')"



@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)  # Print data to console for demonstration
    
    

    return jsonify({'message': 'Data received successfully'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
