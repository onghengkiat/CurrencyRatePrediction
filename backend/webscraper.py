import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from requests import ConnectionError
from operator import itemgetter

class WebScraper:
    def __init__(self, curex_url):
        self.CURRENCY_EXCHANGE_RATE_URL = curex_url

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

    def get_df(self):
        df = self._scrap_currency_exchange_rate()

        df["date"] = pd.to_datetime(df["date"], format='%d %b %Y')
        # remove the timezone
        df["date"] = df["date"].dt.tz_localize(None)
        # convert to datetime
        df["date"] = df["date"].dt.to_pydatetime()

        # Sort it by currency code followed by dates
        df.sort_values(['currency_code', 'date'], ascending=[True, True], inplace=True)

        # Filling missing values with previous data
        df.fillna(method='ffill', inplace=True)

        df.reset_index(inplace=True)

        return df

