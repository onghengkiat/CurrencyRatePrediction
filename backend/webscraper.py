import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
from requests import ConnectionError
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
import time
import os
import tempfile
from datetime import datetime

class WebScraper:
    def __init__(self, curex_url, cpi_url, cpi_filename, gdp_url, download_dir):
        self.CURRENCY_EXCHANGE_RATE_URL = curex_url
        self.CPI_URL = cpi_url
        self.CPI_FILENAME = cpi_filename
        self.GDP_URL = gdp_url
        self.DOWNLOAD_DIR = download_dir
        self.CPI_MAPPING = {
            "United States": {
                "currency_code": "USD",
                "position": 0
            },
            "United Kingdom": {
                "currency_code": "GBP",
                "position": 0
            },
            "Euro Area": {
                "currency_code": "EUR",
                "position": 0
            },
            "Japan": {
                "currency_code": "JPY",
                "position": 0
            },
            "Switzerland": {
                "currency_code": "CHF",
                "position": 0
            },
            "Australia": {
                "currency_code": "AUD",
                "position": 0
            },
            "Canada": {
                "currency_code": "CAD",
                "position": 0
            },
            "Singapore": {
                "currency_code": "SGD",
                "position": 0
            },
            "China, P.R.: Hong Kong": {
                "currency_code": "HKD",
                "position": 0
            },
            "Thailand": {
                "currency_code": "THB",
                "position": 0
            },
            "Philippines": {
                "currency_code": "PHP",
                "position": 0
            },
            "Taiwan Province of China": {
                "currency_code": "TWD",
                "position": 0
            },
            "Korea, Rep. of": {
                "currency_code": "KRW",
                "position": 1
            },
            "Indonesia": {
                "currency_code": "IDR",
                "position": 0
            },
            "Saudi Arabia": {
                "currency_code": "SAR",
                "position": 0
            },
            "China, P.R.: Mainland": {
                "currency_code": "CNY",
                "position": 0
            },
            "Brunei Darussalam": {
                "currency_code": "BND",
                "position": 0
            },
            "Vietnam": {
                "currency_code": "VND",
                "position": 0
            },
            "Cambodia": {
                "currency_code": "KHR",
                "position": 0
            },
            "New Zealand": {
                "currency_code": "NZD",
                "position": 0
            },
            "Myanmar": {
                "currency_code": "MMK",
                "position": 0
            },
            "India": {
                "currency_code": "INR",
                "position": 1
            },
            "United Arab Emirates": {
                "currency_code": "AED",
                "position": 0
            },
            "Pakistan": {
                "currency_code": "PKR",
                "position": 0
            },
            "Nepal": {
                "currency_code": "NPR",
                "position": 0
            },
            "Egypt, Arab Rep. of": {
                "currency_code": "EGP",
                "position": 0
            },
            "Malaysia": {
                "currency_code": "MYR",
                "position": 0
            }
        }

        self.GDP_MAPPING = {
            "United States": "USD",
            "United Kingdom": "GBP",
            "Euro area": "EUR",
            "Japan": "JPY",
            "Switzerland": "CHF",
            "Australia": "AUD",
            "Canada": "CAD",
            "Singapore": "SGD",
            "Hong Kong SAR, China": "HKD",
            "Thailand": "THB",
            "Philippines": "PHP",
            "Taiwan": "TWD",
            "Korea, Rep.": "KRW",
            "Indonesia": "IDR",
            "Saudi Arabia": "SAR",
            "China": "CNY",
            "Brunei Darussalam": "BND",
            "Vietnam": "VND",
            "Cambodia": "KHR",
            "New Zealand": "NZD",
            "Myanmar": "MMK",
            "India": "INR",
            "United Arab Emirates": "AED",
            "Pakistan": "PKR",
            "Nepal": "NPR",
            "Egypt, Arab Rep.": "EGP",
            "Malaysia": "MYR",
        }

    def _is_header(self, row):
        """
        Parameters
        ----------
        row: NavigableString
            A row extracted from the table


        Return
        ------
        is_header: Boolean
            True or False for the statement of the row is a header row

        Description
        -----------
        This method is used to check if the row is the header row
        which contains the country code instead of date and exchange rate
        """

        if row.find("th"):
            return True
        return False

    def _is_empty_row(self, columns):
        """
        Parameters
        ----------
        columns: List[String]
            A list of string that is formed from a row of the table by splitting them
            into different cells


        Return
        ------
        is_empty: Boolean
            True or False for the statement of the row is an empty row

        Description
        -----------
        This method is used to check if the row is an empty row.
        The website is intercepting a few empty rows in the table tag
        to make the appearance looks nicer.
        """
        
        if len(columns) == 1:
            return True
        return False
    
    def _get_timerange_query_string(self):
        cur_time = datetime.now()
        end_year = cur_time.year
        # The month to be used in the query string in the website is based on index
        # Example October will be 9 in this case
        end_month = cur_time.month - 1
        begin_year = end_year - 3
        begin_month = end_month
        return f"_bnm_exchange_rate_display_portlet_monthStart={begin_month}&_bnm_exchange_rate_display_portlet_yearStart={begin_year}&_bnm_exchange_rate_display_portlet_monthEnd={end_month}&_bnm_exchange_rate_display_portlet_yearEnd={end_year}"

    def _get_exchange_rate_url(self):
        # URL with query string to the data from last year
        QUERY_STRING_FRONT = "?p_p_id=bnm_exchange_rate_display_portlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&"
        QUERY_STRING_BACK = "&_bnm_exchange_rate_display_portlet_sessionTime=1200&_bnm_exchange_rate_display_portlet_rateType=MR&_bnm_exchange_rate_display_portlet_quotation=fx"
        return self.CURRENCY_EXCHANGE_RATE_URL + QUERY_STRING_FRONT + self._get_timerange_query_string() + QUERY_STRING_BACK

    def _scrap_currency_exchange_rate(self):
        connection_trial = 0
        connection_is_failed = True
        while connection_is_failed:
            try:
                page = requests.get(self._get_exchange_rate_url())
                connection_is_failed = False
            except ConnectionError as e:
                connection_trial += 1
                print(f"Connection failed for {connection_trial} trials.")

        soup = BeautifulSoup(page.content, "html.parser")

        # Find the table tag
        data_table = soup.find(id="dvData2")

        # Used to build the dataframe
        data = {
            "date": [],
            "currency_code": [],
            "from_myr": [],
            "to_myr": [],
        }

        # Also used to track the data scraping now is having what headers
        # The table on the website is built from multiple header rows
        cur_header = []
        for row in data_table:
            # Split the row into separated cells
            columns = row.text.strip().replace('\t', '').replace('\r', '').split("\n")

            # Skip the empty line in the table
            if self._is_empty_row(columns):
                continue

            if self._is_header(row):
                cur_header = columns
            else:
                index = 0
                date, rates = columns[0], columns[1:]
                for rate in rates:
                    if rate == '':
                        continue

                    rate = float(rate.replace(',', ''))

                    if rate == 0:
                        rate = None
                        to_myr = None
                    else:
                        to_myr = round(1.0/rate, 4)
                    
                    data["date"].append(date)
                    cur_currency_code = cur_header[index]
                    data["currency_code"].append(cur_currency_code)
                    data["from_myr"].append(rate)
                    data["to_myr"].append(to_myr)
                    index += 1
        df = pd.DataFrame.from_dict(data)
        return df

    def _scrap_cpi(self):

        def click_changing_button(dr, class_name, position=0):
            for i in range(20):
                try:
                    WebDriverWait(dr, 60).until(
                        lambda driver : driver.find_element_by_class_name(class_name)
                    )
                    if position != 0:
                        button = dr.find_elements_by_class_name(class_name)[position]
                    else:
                        button = dr.find_element_by_class_name(class_name)
                    button.click()
                    break
                except StaleElementReferenceException as e:
                    time.sleep(1)
                    print(f"Trial {i+1}")
                except ElementNotInteractableException as e:
                    time.sleep(1)
                    print(f"Trial {i+1}")
        
        driver = webdriver.Chrome("chromedriver_linux64/chromedriver")
        driver.get(self.CPI_URL)
        # maximize browser window
        driver.maximize_window()
        

        WebDriverWait(driver, 60).until(
            lambda driver : driver.find_element_by_class_name("EarDimItem")
        )
        # 15 seconds for everything to really completed loading
        time.sleep(15)
        control_panels = driver.find_elements_by_class_name("EarDimItem")
        # Select Time
        for control_panel in control_panels:
            dimension_name = control_panel.find_element_by_class_name("DimensionName")
            if dimension_name.text == "Time":
                # Enter the editing panel
                click_changing_button(control_panel, "MenuIndBtn")

                # Change frequency to monthly
                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("FrequencyLayout")
                )
                time.sleep(1)
                frequency_layout = driver.find_element_by_class_name("FrequencyLayout")
                frequency_layout.find_elements_by_class_name("PPCheckBox")[0].click()

                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("FrequencyLayout")
                )
                time.sleep(1)
                frequency_layout = driver.find_element_by_class_name("FrequencyLayout")
                frequency_layout.find_elements_by_class_name("PPCheckBox")[3].click()

                # Change time period
                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("RelPeriodLayout")
                )
                time.sleep(1)
                period_layout = driver.find_element_by_class_name("RelPeriodLayout")
                period_layout.find_elements_by_class_name("PPTextBoxInput")[1].send_keys(Keys.CONTROL + "a")
                period_layout.find_elements_by_class_name("PPTextBoxInput")[1].send_keys(Keys.DELETE)
                period_layout.find_elements_by_class_name("PPTextBoxInput")[1].send_keys(-37)

                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("RelPeriodLayout")
                )
                time.sleep(1)
                period_layout = driver.find_element_by_class_name("RelPeriodLayout")
                period_layout.find_elements_by_class_name("PPTextBoxInput")[3].send_keys(Keys.CONTROL + "a")
                period_layout.find_elements_by_class_name("PPTextBoxInput")[3].send_keys(Keys.DELETE)
                period_layout.find_elements_by_class_name("PPTextBoxInput")[3].send_keys(1)


                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("RelPeriodLayout")
                )
                time.sleep(1)
                period_layout = driver.find_element_by_class_name("RelPeriodLayout")
                period_layout.find_elements_by_class_name("PPButton")[2].click()

                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("PPMenuItemContentPart")
                )
                time.sleep(1)
                item_contents = driver.find_elements_by_class_name("PPMenuItemContentPart")
                for item_content in item_contents:
                    if item_content.text == "Months":
                        item_content.click()
                        break
                
                # Apply the changes 
                time.sleep(1)
                dialog_buttons = driver.find_element_by_class_name("PPDialogButtons")
                click_changing_button(dialog_buttons, "PPButton")
                break

        WebDriverWait(driver, 60).until(
            lambda driver : driver.find_element_by_class_name("EarDimItem")
        )
        time.sleep(15)
        control_panels = driver.find_elements_by_class_name("EarDimItem")

        # Select field
        for control_panel in control_panels:
            dimension_name = control_panel.find_element_by_class_name("DimensionName")
            if dimension_name.text == "Indicator":
                # Enter the editing panel
                click_changing_button(control_panel, "DeleteIndBtn")
                
                # Clear all the default values
                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("PPFloatBlocks")
                )
                time.sleep(2)
                float_block = driver.find_element_by_class_name("PPFloatBlocks")
                click_changing_button(float_block, "PPButton")
                
                time.sleep(2)
                texts = driver.find_elements_by_class_name("PPTLVNodeSelected")
                for text in texts:
                    click_changing_button(driver, "PPTLVNodeSelected")

                click_changing_button(float_block, "PPButton")

                # Select the field
                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("PPFloatBlocks")
                )
                time.sleep(1)

                float_block = driver.find_element_by_class_name("PPFloatBlocks")
                float_block.find_elements_by_class_name("PPTextBoxInput")[1].clear()
                float_block.find_elements_by_class_name("PPTextBoxInput")[1].send_keys("Consumer")

                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("PPFloatBlocks")
                )
                time.sleep(1)
                float_block = driver.find_element_by_class_name("PPFloatBlocks")
                click_changing_button(float_block, "PPTextBoxImage")

                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("PPTLVNodeText")
                )
                time.sleep(1)
                click_changing_button(driver, "PPTLVNodeText")

                # Apply the changes
                time.sleep(1)
                dialog_buttons = driver.find_element_by_class_name("PPDialogButtons")
                click_changing_button(dialog_buttons, "PPButton")
                break

        WebDriverWait(driver, 60).until(
            lambda driver : driver.find_element_by_class_name("EarDimItem")
        )
        time.sleep(15)
        control_panels = driver.find_elements_by_class_name("EarDimItem")

        # Select countries
        for control_panel in control_panels:
            dimension_name = control_panel.find_element_by_class_name("DimensionName")
            if dimension_name.text == "Country":
                # Enter the editing panel
                click_changing_button(control_panel, "MenuIndBtn")
                
                # Clear all the default values
                WebDriverWait(driver, 60).until(
                    lambda driver : driver.find_element_by_class_name("PPFloatBlocks")
                )
                time.sleep(2)
                float_block = driver.find_element_by_class_name("PPFloatBlocks")
                click_changing_button(float_block, "PPButton")
                
                time.sleep(2)
                texts = driver.find_elements_by_class_name("PPTLVNodeSelected")
                for text in texts:
                    click_changing_button(driver, "PPTLVNodeSelected")

                click_changing_button(float_block, "PPButton")

                # Select the countries
                for key, detail in self.CPI_MAPPING.items():
                    # Key in country name
                    WebDriverWait(driver, 60).until(
                        lambda driver : driver.find_element_by_class_name("PPFloatBlocks")
                    )
                    time.sleep(1)

                    float_block = driver.find_element_by_class_name("PPFloatBlocks")
                    float_block.find_elements_by_class_name("PPTextBoxInput")[1].clear()
                    float_block.find_elements_by_class_name("PPTextBoxInput")[1].send_keys(key)

                    # Search Country
                    WebDriverWait(driver, 60).until(
                        lambda driver : driver.find_element_by_class_name("PPFloatBlocks")
                    )
                    time.sleep(1)
                    float_block = driver.find_element_by_class_name("PPFloatBlocks")
                    click_changing_button(float_block, "PPTextBoxImage")

                    # Select country
                    WebDriverWait(driver, 60).until(
                        lambda driver : driver.find_element_by_class_name("PPTLVNodeText")
                    )
                    time.sleep(1)
                    click_changing_button(driver, "PPTLVNodeText", position=detail["position"])

                # Apply the changes
                time.sleep(1)
                dialog_buttons = driver.find_element_by_class_name("PPDialogButtons")
                click_changing_button(dialog_buttons, "PPButton")
                break

        # Export to excel file
        WebDriverWait(driver, 60).until(
            lambda driver : driver.find_elements_by_class_name("PPContextPanel")
        )
        time.sleep(10)
        ppcontents = driver.find_element_by_class_name("PPContextPanel")
        click_changing_button(ppcontents, "PPContent", position=5)
        time.sleep(3)
        WebDriverWait(driver, 60).until(
            lambda driver : driver.find_element_by_id("Xlsx")
        )
        driver.find_element_by_id("Xlsx").click()
        time.sleep(15)

    def get_df(self):
        print("Scraping Currency Exchange Rate Data...")
        df = self._scrap_currency_exchange_rate()
        print("Done Scraping Currency Exchange Rate Data.\n\n")
        malaysia_data = [{
            "currency_code": "MYR",
            "date": date,
            "from_myr": 1,
            "to_myr": 1,
        } for date in df["date"].unique()]
        df = df.append(malaysia_data, ignore_index=True, sort=False)

        df["date"] = pd.to_datetime(df["date"], format='%d %b %Y')
        # remove the timezone
        df["date"] = df["date"].dt.tz_localize(None)
        # convert to datetime
        df["date"] = df["date"].dt.to_pydatetime()

        # SDR is not a currency
        df = df[df["currency_code"] != "SDR"]

        # Sort it by currency code followed by dates
        df.sort_values(["currency_code", "date"], ascending=[True, True], inplace=True)
        print("Scraping CPI Data...")

        connection_trial = 0
        connection_is_failed = True
        while connection_is_failed:
            try:
                self._scrap_cpi()
                connection_is_failed = False
            except Exception as e:
                connection_trial += 1
                print(f"Connection failed for {connection_trial} trials.")

        # Move the downloaded file to the temp app directory
        # Which will be deleted after being loaded
        tmpdir = tempfile.mkdtemp() 
        destination = os.path.join(tmpdir, self.CPI_FILENAME)
        # destination = self.CPI_FILENAME
        source = os.path.join(self.DOWNLOAD_DIR, self.CPI_FILENAME)
        if os.path.exists(source):
            os.rename(source, destination)
        cpi_df = pd.read_excel(destination)

        # First column name changes from Unnamed to country_name
        column_names = cpi_df.columns.tolist()
        column_names[0] = "country_name"
        cpi_df.columns = column_names

        # Search for the countries that are not found in the CPI database and filter their currency codes out from the df
        for key, val in self.CPI_MAPPING.items():
            if key not in cpi_df["country_name"].unique():
                print(key + " is not found in the CPI database")
                df = df[df['currency_code'] != val["currency_code"]]

        df["month"] = df.date.dt.month
        df["year"] = df.date.dt.year
        df["cpi"] = np.nan
        for i, row in cpi_df.iterrows():
            currency_code = self.CPI_MAPPING[row["country_name"]]["currency_code"]
            for date in column_names[1:]:
                date_obj = datetime.strptime(date, "%b %Y")
                month, year = date_obj.month, date_obj.year
                # plus 1 because cur month is used to predict next month
                month = int(month) + 1
                year = int(year)
                if month > 12:
                    month = 1
                    year = year + 1
                df.loc[(df["month"] == month) & (df["year"] == year) & (df["currency_code"] == currency_code), "cpi"] = row[date]

        print("Done Scraping CPI Data.\n\n")

        print("Scraping GDP Data...")
        connection_trial = 0
        connection_is_failed = True
        while connection_is_failed:
            try:
                downloaded = requests.get(self.GDP_URL)
                connection_is_failed = False
            except ConnectionError as e:
                connection_trial += 1
                print(f"Connection failed for {connection_trial} trials.")

        # Header row starting from 4th row
        gdp_df = pd.read_excel(downloaded.content, sheet_name="Data", skiprows=3)
        gdp_df.reset_index(drop=True, inplace=True)
        column_names = gdp_df.columns.tolist()

        # Search for the countries that are not found in the GDP database and filter their currency codes out from the df
        for key, val in self.GDP_MAPPING.items():
            if key not in gdp_df["Country Name"].unique():
                print(key + " is not found in the GDP database")
                df = df[df["currency_code"] != self.GDP_MAPPING[key]]

        df["gdp"] = np.nan
        for i, row in gdp_df.iterrows():

            currency_code = self.GDP_MAPPING.get(row["Country Name"], None)
            if currency_code is None:
                continue

            for year in column_names[-4:]:
                
                # Year plus 1 because cur year is used to predict next year
                df.loc[(df["year"] == int(year) + 1) & (df["currency_code"] == currency_code), "gdp"] = row[year]
        print("Done Scraping GDP Data.\n\n")
        print(df[df.isna().any(axis=1)])
        # Month and Year are not needed for visualization and analysis processes
        df.drop(["month", "year"], axis=1, inplace=True)

        # Filling missing values with previous data
        df.fillna(method="ffill", inplace=True)

        df.reset_index(drop=True, inplace=True)

        return df

