from flask import Flask
from constants import DATA_FILENAME, MODEL_FILENAME, SCALAR_FILENAME, GRAPH_FILENAME, MODEL_SAVE_PATH, WINDOW_SIZE
import pandas as pd
import os
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)

df = pd.read_csv(DATA_FILENAME, index_col=0)
df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
# remove the timezone
df["date"] = df["date"].dt.tz_localize(None)
# convert to datetime
df["date"] = df["date"].dt.to_pydatetime()

currency_codes = df['currency_code'].unique().tolist()

models = {}
scalers = {}
for currency_code in currency_codes:
    models[currency_code] = load_model(os.path.join(MODEL_SAVE_PATH, currency_code, MODEL_FILENAME))
    scalers[currency_code] = joblib.load(os.path.join(MODEL_SAVE_PATH, currency_code, SCALAR_FILENAME))

from app import routes