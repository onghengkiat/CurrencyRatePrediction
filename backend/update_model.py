from webscraper import WebScraper
from constants import CURRENCY_EXCHANGE_RATE_LINK, CPI_LINK, CPI_FILENAME, GDP_LINK, DATA_FILENAME, WINDOW_SIZE, DOWNLOAD_DIR, MODEL_FILENAME, MODEL_SAVE_PATH
from modeltrainer import ModelTrainer
import pandas as pd
from constants import MODEL_WITH_CPI, MODEL_WITH_GDP, MODEL_WITH_GDP_AND_CPI, MODEL_ONLY_RATE

scraper = WebScraper(CURRENCY_EXCHANGE_RATE_LINK, CPI_LINK, CPI_FILENAME, GDP_LINK, DOWNLOAD_DIR)
df = scraper.get_df()
df.to_csv(DATA_FILENAME)
# df = pd.read_csv(DATA_FILENAME, index_col=0)
currency_codes = df['currency_code'].unique()
malaysia_df = df[df['currency_code'] == 'MYR'].reset_index(drop=True)
for currency_code in currency_codes:
    if currency_code == 'MYR':
        continue
    for algorithm in ModelTrainer.ALGORITHMS_AVAILABLE:
        modelTrainer = ModelTrainer(currency_code, MODEL_FILENAME, MODEL_SAVE_PATH,
            MODEL_WITH_CPI, MODEL_WITH_GDP, MODEL_WITH_GDP_AND_CPI, MODEL_ONLY_RATE)
        modelTrainer.set_window_size(WINDOW_SIZE)
        modelTrainer.set_algorithm(algorithm)
        targeted_df = df[df['currency_code'] == currency_code].reset_index(drop=True)

        modelTrainer.set_include_cpi(False)
        modelTrainer.set_include_gdp(False)
        modelTrainer.build(targeted_df, malaysia_df, only_show_evaluation=True)
        modelTrainer.save()

        modelTrainer.set_include_cpi(True)
        modelTrainer.set_include_gdp(False)
        modelTrainer.build(targeted_df, malaysia_df, only_show_evaluation=True)
        modelTrainer.save()

        modelTrainer.set_include_cpi(False)
        modelTrainer.set_include_gdp(True)
        modelTrainer.build(targeted_df, malaysia_df, only_show_evaluation=True)
        modelTrainer.save()

        modelTrainer.set_include_cpi(True)
        modelTrainer.set_include_gdp(True)
        modelTrainer.build(targeted_df, malaysia_df, only_show_evaluation=True)
        modelTrainer.save()
