from webscraper import WebScraper
from constants import DATASOURCE_LINK, DATA_FILENAME, WINDOW_SIZE
from modeltrainer import ModelTrainer
import pandas as pd

scraper = WebScraper(url=DATASOURCE_LINK)
df = scraper.get_df()
df.to_csv(DATA_FILENAME)
# first column is date
currency_codes = df.columns[1:]
for currency_code in currency_codes:
    modelTrainer = ModelTrainer(currency_code)
    modelTrainer.set_window_size(WINDOW_SIZE)
    modelTrainer.build(df)
    modelTrainer.save()
