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
WINDOW_SIZE = 7

CURRENCY_TO_COUNTRY = {
    "USD": "United States",
    "GBP": "United Kingdom",
    "EUR": "Euro area",
    "JPY": "Japan",
    "CHF": "Switzerland",
    "AUD": "Australia",
    "CAD": "Canada",
    "SGD": "Singapore",
    "HKD": "Hong Kong SAR, China",
    "THB": "Thailand",
    "PHP": "Philippines",
    "TWD": "Taiwan",
    "KRW": "Korea, Rep.",
    "IDR": "Indonesia",
    "SAR": "Saudi Arabia",
    "CNY": "China",
    "BND": "Brunei Darussalam",
    "VND": "Vietnam",
    "KHR": "Cambodia",
    "NZD": "New Zealand",
    "MMK": "Myanmar",
    "INR": "India",
    "AED": "United Arab Emirates",
    "PKR": "Pakistan",
    "NPR": "Nepal",
    "EGP": "Egypt, Arab Rep.",
    "MYR": "Malaysia",
}

USERS = {
    "admin": {
        "username": "admin",
        "password": "admin",
        "fullname": "Admin",
        "role": "admin",
        "email": "admin@gmail.com",
    },
    "developer": {
        "username": "developer",
        "password": "developer",
        "fullname": "Developer",
        "role": "developer",
        "email": "developer@gmail.com",
    },
    "viewer": {
        "username": "viewer",
        "password": "viewer",
        "fullname": "Viewer",
        "role": "viewer",
        "email": "viewer@gmail.com",
    }
}

ACCESS_DENIED_ERROR = {
    "isError": True, 
    "code": "Access Denied", 
    "message": "You do not have permission to visit this page."
}

SECRET_KEY = 'hfdjksasdjnrnmq'