from webscraper import WebScraper
from constants import CURRENCY_EXCHANGE_RATE_LINK, CPI_LINK, CPI_FILENAME, GDP_LINK, DATA_FILENAME, WINDOW_SIZE, DOWNLOAD_DIR
from modeltrainer import ModelTrainer
import pandas as pd

scraper = WebScraper(CURRENCY_EXCHANGE_RATE_LINK, CPI_LINK, CPI_FILENAME, GDP_LINK, DOWNLOAD_DIR)
df = scraper.get_df()
df.to_csv(DATA_FILENAME)
# currency_codes = df['currency_code'].unique()
# for currency_code in currency_codes:
#     modelTrainer = ModelTrainer(currency_code)
#     modelTrainer.set_window_size(WINDOW_SIZE)
#     modelTrainer.build(df[df['currency_code'] == currency_code])
#     modelTrainer.save()
