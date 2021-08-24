from flask import Flask, request
from flask_cors import CORS
import os
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

@app.route('/get-member-data', methods=['POST'])
def get_member_data():
    period = request.json['range']
    talent = request.json['talent']
    count_type = request.json['countType']
    db = f'holo_{count_type}counts.csv'
    df = pd.read_csv(db, encoding='utf-8')
    df.set_index('Date', inplace=True)
    period = df.index.size if period == 0 or period > df[talent].size else period
    # reduce data point to speed up render speed
    interval = 1 if period <= 200 else 2
    start = 1 if period % 2 and period > 200 == 0 else 0
    return_dict = df[talent].iloc[:period].iloc[start::interval].to_dict()
    # dates = list(return_dict.keys())
    # i = -1
    # while return_dict[dates[i - 1]] == 0:
    #     return_dict[dates[i]] = None
    #     i -= 1
    return return_dict

if __name__ == '__main__':
    app.run(port=8000, debug=False)