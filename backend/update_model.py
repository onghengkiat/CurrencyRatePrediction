from webscraper import WebScraper
from constants import CURRENCY_EXCHANGE_RATE_LINK, CPI_LINK, CPI_FILENAME, GDP_LINK, INTEREST_RATE_LINK, DATA_FILENAME, WINDOW_SIZE, DOWNLOAD_DIR, MODEL_FILENAME, MODEL_SAVE_PATH
from modeltrainer import ModelTrainer
import pandas as pd
import itertools
from constants import MODEL_WITH_CPI, MODEL_WITH_GDP, MODEL_WITH_GDP_AND_CPI, MODEL_ONLY_RATE

scraper = WebScraper(CURRENCY_EXCHANGE_RATE_LINK, CPI_LINK, CPI_FILENAME, GDP_LINK, INTEREST_RATE_LINK, DOWNLOAD_DIR, duration=3)
df = scraper.get_df()
df.to_csv(DATA_FILENAME)
df = pd.read_csv(DATA_FILENAME, index_col=0)

df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
# remove the timezone
df["date"] = df["date"].dt.tz_localize(None)
# convert to datetime
df["date"] = df["date"].dt.to_pydatetime()

currency_codes = df['currency_code'].unique()
malaysia_df = df[df['currency_code'] == 'MYR'].reset_index(drop=True)

for currency_code in currency_codes:
    if currency_code == 'MYR':
        continue

    modelTrainer = ModelTrainer(currency_code, MODEL_FILENAME, MODEL_SAVE_PATH,
            MODEL_WITH_CPI, MODEL_WITH_GDP, MODEL_WITH_GDP_AND_CPI, MODEL_ONLY_RATE,
            num_of_neuron=20, num_of_iteration=30, alpha=0.1, dropout=0.1,
            test_n_months=12, compute_difference=True, predict_change=False,
            adjust_y_intercept=True, adjust_y_intercept_interval=1)
    modelTrainer.set_window_size(WINDOW_SIZE)

    for algorithm in ModelTrainer.ALGORITHMS_AVAILABLE:    
        modelTrainer.set_algorithm(algorithm)

        targeted_df = df[df['currency_code'] == currency_code].reset_index(drop=True)

        choices = [False, True]
        # permutated_true_and_false = list(itertools.product(choices, repeat=3))
        permutated_true_and_false = list(itertools.product(choices, repeat=2))

        for permutation in permutated_true_and_false:
            modelTrainer.set_include_gdp(permutation[0])
            modelTrainer.set_include_cpi(permutation[1])
            # modelTrainer.set_include_interest_rate(permutation[2])
            modelTrainer.build(targeted_df, malaysia_df, only_show_evaluation=True)
            modelTrainer.save()

        
