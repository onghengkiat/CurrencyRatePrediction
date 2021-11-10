from flask import Flask
from constants import DATA_FILENAME
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

df = pd.read_csv(DATA_FILENAME, index_col=0)
malaysia_df = df[df['currency_code'] == 'MYR']
df = df[df['currency_code'] != 'MYR']

df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
# remove the timezone
df["date"] = df["date"].dt.tz_localize(None)
# convert to datetime
df["date"] = df["date"].dt.to_pydatetime()

currency_codes = df['currency_code'].unique().tolist()

scalers = {}
for currency_code in currency_codes:
    scaler = MinMaxScaler()
    scaler.fit_transform(df[df['currency_code'] == currency_code][['from_myr']])
    scalers[currency_code] = scaler

from app import routes