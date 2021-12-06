from flask import Flask
from constants import DATA_FILENAME
import pandas as pd

app = Flask(__name__)

df = pd.read_csv(DATA_FILENAME, index_col=0)

df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
# remove the timezone
df["date"] = df["date"].dt.tz_localize(None)
# convert to datetime
df["date"] = df["date"].dt.to_pydatetime()

malaysia_df = df[df['currency_code'] == 'MYR'].reset_index(drop=True)
df = df[df['currency_code'] != 'MYR']

currency_codes = df['currency_code'].unique().tolist()

from app import routes