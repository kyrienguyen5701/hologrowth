import os
import io
import json
from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd

credentials_fn = os.path.join(os.getcwd(), 'credentials.json')
credentials_dict = json.load(open(credentials_fn, 'r'))
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
gcs_bucket_name = 'hologrowth-db'

def gcp_csv_to_df(bucket_name, source_blob_name, parse_dates=None, nrows=None):
  storage_client = storage.Client(project='hologrowth', credentials=credentials)
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(source_blob_name)
  data = blob.download_as_bytes()
  df = pd.read_csv(io.BytesIO(data), parse_dates=parse_dates, encoding='utf-8', nrows=nrows)
  return df

def df_to_gcp_csv(df, bucket_name, tgt_file_name):
  storage_client = storage.Client(project='hologrowth', credentials=credentials)
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(tgt_file_name)
  blob.upload_from_string(df.to_csv(), 'text/csv')
