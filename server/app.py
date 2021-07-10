from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/send', methods=['POST'])
def get_data():
    days = request.json['days']
    talent = request.json['talent']
    count_type = request.json['countType']
    db = f'holo_{count_type}counts.csv'
    df = pd.read_csv(db, encoding='utf-8')
    df.set_index('Date', inplace=True)
    return df[talent][:days].to_dict()

if __name__ == '__main__':
    app.run(port=8000, debug=False)