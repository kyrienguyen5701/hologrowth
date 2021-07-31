from flask import Flask, request
from flask_cors import CORS
import os
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

@app.route('/get-member-data', methods=['POST'])
def get_member_data():
    range = request.json['range']
    talent = request.json['talent']
    count_type = request.json['countType']
    db = f'holo_{count_type}counts.csv'
    df = pd.read_csv(db, encoding='utf-8')
    df.set_index('Date', inplace=True)
    range = df[talent].size if range == 0 or range > df[talent].size else range
    return df[talent][:range].to_dict()

@app.route('/get-holo-data', methods=['POST'])
def get_holo_data():
    count_type = request.json['countType']
    db = f'holo_{count_type}counts.csv'
    df = pd.read_csv(db, encoding='utf-8')
    df.set_index('Date', inplace=True)
    res = dict()
    for talent in df.columns:
        res[talent] = df[talent].to_dict()
    return json.dumps(res)

if __name__ == '__main__':
    app.run(port=8000, debug=False)