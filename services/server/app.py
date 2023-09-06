import os
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from db_mgr import gcp_csv_to_df, gcs_bucket_name
import pandas as pd

app = Flask(__name__)
allowed_origins = ['https://hologrowth.kyrie5701.com']
is_debugging = os.environ.get('FLASK_DEBUG')
if is_debugging:
    allowed_origins.append('http://localhost:8080')
CORS(app, origins=allowed_origins)

# thanks to https://stackoverflow.com/a/52875875
def _build_cors_preflight_response(req, res):
    res.headers.add('Access-Control-Allow-Origin', req.headers.get('Origin'))
    res.headers.add('Access-Control-Allow-Headers', 'Authorization, Origin, X-Requested-With, Content-Type, Accept')
    res.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD')
    res.headers.add('Access-Control-Max-Age', 1728000)
    return res

def _corsify_actual_response(req, res):
    res.headers.add('Access-Control-Allow-Origin', req.headers.get('Origin'))
    return res

@app.route('/get-member-data', methods=['POST', 'OPTIONS'])
# @cross_origin(origins=allowed_origins) # this is the short-hand way
def get_member_data():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request, make_response())
    
    period = request.json['range']
    talent = request.json['talent']
    count_type = request.json['countType']
    blob_name = f'holo_{count_type}counts_dev.csv'
    if not is_debugging:
        blob_name = f'holo_{count_type}counts.csv'
    df = gcp_csv_to_df(gcs_bucket_name, blob_name, nrows=period) if period != 0 else gcp_csv_to_df(gcs_bucket_name, blob_name)
    df.set_index('Date', inplace=True)
    period = df.index.size if period == 0 else period
    
    # reduce data point to speed up rendering
    interval = 1 if period <= 200 else 2
    start = 0
    return_dict = df[talent].iloc[:period].iloc[start::interval].to_dict()
    
    res = make_response(return_dict)
    
    return _corsify_actual_response(request, res)

if __name__ == '__main__':
    app.run(port=8000, debug=False)