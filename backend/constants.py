CURRENCY_EXCHANGE_RATE_LINK = "https://www.bnm.gov.my/exchange-rates"
CPI_LINK = "https://data.imf.org/?sk=4FFB52B2-3653-409A-B471-D47B46D904B5&sId=1485878855236"
GDP_LINK = "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel"
INTEREST_RATE_LINK = "https://api.worldbank.org/v2/en/indicator/FR.INR.RINR?downloadformat=excel"
DATA_FILENAME = "MYR-ForeignCurrency.csv"
CPI_FILENAME = "Consumer_Price_Index_CPI.xlsx"
DOWNLOAD_DIR = "/home/user/Downloads"

MODEL_WITH_CPI = "CPI"
MODEL_WITH_GDP = "GDP"
MODEL_WITH_GDP_AND_CPI = "CPI_GDP"
MODEL_ONLY_RATE = "RATE_ONLY"

MODEL_SAVE_PATH = "./model"
MODEL_FILENAME = "model"
WINDOW_SIZE = 3