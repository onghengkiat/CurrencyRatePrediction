import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from requests import ConnectionError

class WebScraper:
    def __init__(self, url):
        self.DATASOURCE_LINK = url

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
        begin_year = end_year - 1
        begin_month = end_month
        return f"_bnm_exchange_rate_display_portlet_monthStart={begin_month}&_bnm_exchange_rate_display_portlet_yearStart={begin_year}&_bnm_exchange_rate_display_portlet_monthEnd={end_month}&_bnm_exchange_rate_display_portlet_yearEnd={end_year}"

    def _get_complete_url(self):
        # URL with query string to the data from last year
        QUERY_STRING_FRONT = "?p_p_id=bnm_exchange_rate_display_portlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&"
        QUERY_STRING_BACK = "&_bnm_exchange_rate_display_portlet_sessionTime=1200&_bnm_exchange_rate_display_portlet_rateType=MR&_bnm_exchange_rate_display_portlet_quotation=rm"
        return self.DATASOURCE_LINK + QUERY_STRING_FRONT + self._get_timerange_query_string() + QUERY_STRING_BACK

    def get_df(self):
        connection_trial = 0
        connection_is_failed = True
        while connection_is_failed:
            try:
                page = requests.get(self._get_complete_url())
                connection_is_failed = False
            except ConnectionError:
                connection_trial += 1
                print(f"Connection failed for {connection_trial} trials.")

        soup = BeautifulSoup(page.content, "html.parser")

        # Find the table tag
        data_table = soup.find(id="dvData2")

        # Used to build the dataframe
        data = {
            "date": [],
        }
        # To prevent duplicate date collected due to existence of multiple tables in one table
        is_first_table = True

        # Also used to track the data scraping now is having what headers
        # The table on the website is built from multiple header rows
        cur_header = []
        for row in data_table:
            # Split the row into separated cells
            columns = row.text.strip().split("\n")

            # Skip the empty line in the table
            if self._is_empty_row(columns):
                continue

            if self._is_header(row):
                for col in columns:
                    data[col] = []
                if len(cur_header) != 0:
                    is_first_table = False
                cur_header = columns
            else:
                index = 0
                date, rates = columns[0], columns[1:]
                if is_first_table:
                    data["date"].append(date)
                for rate in rates:
                    cur_country_code = cur_header[index]
                    data[cur_country_code].append(rate)
                    index += 1

        df = pd.DataFrame.from_dict(data)
        return df

