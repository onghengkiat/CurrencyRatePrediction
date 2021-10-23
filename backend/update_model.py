from webscraper import WebScraper
from constants import DATASOURCE_LINK, DATA_FILENAME
from modeltrainer import ModelTrainer
import pandas as pd

# scraper = WebScraper(url=DATASOURCE_LINK)
# df = scraper.get_df()

# df.to_csv(DATA_FILENAME)
df = pd.read_csv("MYR-ForeignCurrency.csv", index_col=0)
modelTrainer = ModelTrainer("USD")
modelTrainer.build(df)
modelTrainer.save()
