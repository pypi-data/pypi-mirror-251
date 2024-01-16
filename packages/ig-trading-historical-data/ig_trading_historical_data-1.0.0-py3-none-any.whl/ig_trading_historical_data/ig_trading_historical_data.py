""" this module contains the IG_API class that is used to log in and gather data."""

# ------------------------------------------------------------------
# import packages
# ------------------------------------------------------------------
import time
import requests
import pandas as pd


# ------------------------------------------------------------------
# API class definition
# ------------------------------------------------------------------
class IG_API:
    """
    Create an instance of this class to log into the IG REST API (using valid credentials).
    Use the methods to gather data.
    """

    def __init__(
        self,
        demo: int,
        username: str,
        pw: str,
        api_key: str,
    ) -> None:
        """
        Log into the IG REST API.

        ---
        Args:
            * demo (int):
                * 1: use Demo account and environment URL
                * 0: use Live account and environment URL
            * username (str): username
            * pw (str): password
            * api_key (str): API key
        ---
        Raises:
            * ValueError: if status_code != 200 (i.e. could not log in)
        ---
        Returns:
            * Nothing. Instead updates class instance attributes that are
            used in later methods:
                * token_cst (str): needed for all further API calls
                * token_x_security_token (str): needed for all further API calls
                * ls_addr (str): Lightstream address
                * utc_offset (str): timezoneOffset information
                * acc_info (dict): dict of misc. account data

                * header_base (dict): needed for all further API calls
        """
        # instantiate variables
        self.demo = demo
        self.username = username
        self.pw = pw
        self.api_key = api_key

        # determine correct URL (API gateway location link)
        self.url_base = "https://" + "demo-" * demo + "api.ig.com/gateway/deal"

        # log in: variables
        url = f"{self.url_base}/session"
        header = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "VERSION": "2",
            "X-IG-API-KEY": api_key,
        }
        json = {"identifier": username, "password": pw}

        # log in: POST request
        r = requests.post(url=url, headers=header, json=json)

        self.acc_info = r.json()

        # log in: reponse
        # (response.text or response.json())
        if r.status_code == 200:
            print("----------------------")
            print("Successfully logged in")
            print("----------------------")
            print()
        else:
            print("----------------------")
            print("ERROR OCCURED")
            print("----------------------")
            print(f"STATUS CODE: {r.status_code}")
            print()

            raise ValueError(r.content)

        # retrieve tokens that MUST BE PASSED AS HEADERS to ALL subsequent API requests
        # [both tokens valid for 6H?]; get extended up to max of 72H while they are in use
        self.token_cst = r.headers["CST"]  # client ID
        self.token_x_security_token = r.headers["X-SECURITY-TOKEN"]  # current account

        # retreieve Lightstream address (required for all streaming connections)
        self.ls_addr = self.acc_info["lightstreamerEndpoint"]

        # unpacking timezone info
        self.utc_offset = self.acc_info["timezoneOffset"]

        # instantiating reusable variables
        self.header_base = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": api_key,
            "CST": self.token_cst,
            "X-SECURITY-TOKEN": self.token_x_security_token,
        }

    def get_watchlist(
        self,
    ) -> dict:
        """
        Print and return dict (r.json()) of Watchlist.

        ---
        Returns:
            * dict: watchlist
        """
        # watchlist: variables
        url = f"{self.url_base}/watchlists"
        header = self.header_base

        # watchlist: GET request
        r = requests.get(url=url, headers=header)

        # watchlist: response
        return r.json()

    def get_market_search(
        self,
        search_term: str = None,
    ) -> dict:
        """
        Get list (value of first key) of available assets having match with search_term,
        later use another function to get the epic of a specific asset of interest.

        ---
        Args:
            * search_term (str, default None): str used in search

        ---
        Returns:
            * dict (1 key, then list with each elem being a dict of that asset's info)
                * can find epic of desired instrument in results
                (but first find correct asset in list of results)
        """
        # market_search: variables
        url = f"{self.url_base}/markets?searchTerm={search_term}"
        header = self.header_base

        # market_search: GET request
        r = requests.get(url=url, headers=header)

        # market_search: response
        return r.json()

    def find_asset_epic_or_info(
        self,
        market_search_dict: dict,
        instrument_name: str,
        expiry: str = "DFB",
        epic_only: int = 1,
    ) -> str:
        """
        Find info for asset of interest, either return the epic only (str),
        or the info found (dict).

        ---
        Args:
            * market_search_dict (dict): output of 'get_market_search' method
            * instrument_name (str): exactly as seen on IG web platform
            (i.e. 'GBP/USD' or 'GBP/USD Forward')
            * expiry (str, default='DFB'): either 'DFB' or the expiration date
            (i.e. 'DEC-23' if a Forward etc.)
            * epic_only (int, default=1):
                * 1: return only the epic str
                * 0: return the info found as a dixt
        ---
        Returns:
            * str or dict: epic string or dict with info found about the asset of interest
        """
        for asset_details in market_search_dict["markets"]:
            if all(
                [
                    asset_details["instrumentName"] == instrument_name,
                    asset_details["expiry"] == expiry,
                ]
            ):
                return asset_details["epic"] if epic_only else asset_details

        return "Asset not found"

    def get_epics(self, assets: dict) -> dict:
        """
        Return the 'assets' dict updated with each assets' epic.

        ---
        Args:
            * assets (dict of dict):
                * example key: 'GBPUSD'
                    * value: dict(key: 'instrument_name', value: 'GBP/USD')
        ---
        Returns:
            * dict of dict: 'assets' input dict updated and returned
        """
        # loop to get epics for all assets in 'assets' dict
        for asset_name, d in assets.items():
            instrument_name = d["instrument_name"]
            expiry = d["expiry"]
            assets[asset_name]["epic"] = self.find_asset_epic_or_info(
                self.get_market_search(
                    asset_name,
                ),
                instrument_name,
                expiry,
                epic_only=1,
            )

        return assets

    def get_prices_single_asset(
        self,
        epic: str,
        resolution: str,
        range_type: str,
        start_date: str = None,
        end_date: str = None,
        weekdays: tuple[int] = (0, 1, 2, 3, 4, 5, 6),
        num_points: int = None,
    ) -> tuple:
        """
        Get prices DataFrame (bid/ask/mid/spreads for all OHLC prices and volume)
        for given parameters and time interval;
        also returns 'allowance' dict
        (resets every 7 days to 10,000 historical price data points).

        ---
        Args:
            * epic (str): instrument epic
            * resolution (str): price resolution
                * SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10,
                MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH
            * range_type (str):
                * 'num_points': use num_points argument
                * 'dates': use start_date/end_date arguments with given timeInterval (see below)
            * start_date (str, opt. depending on range_type):
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates time_interval_start
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * end_date (str, opt. depending on range_type):
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates time_interval_end
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * weekdays (tup[int], opt.):
                * which days of the week to get data for (0: Mon, 6: Sun)
                * defaults to all days of the week (0, 1, 2, 3, 4, 5, 6)
                * NOTE: this is only applied to the code when the time portion
                of the date range is different
            * num_points (int, opt. depending on range_type):
                * get last num_points data points
                * defaults to None
        ---
        Notes to start_date/end_date:
            * if the time portions are the SAME (00:00:00) then data is fetched using
            ALL the 24 hours in EVERY single day available ('weekdays' parameter is IGNORED)
            * if the time portions are DIFFERENT from one another, then the timeInterval and
            'weekdays' parameter is applied
            * during the timeInterval technique, note that the time rounds DOWNWARDS
                * i.e. if getting HOURLY data from 00:00:00-23:59:59 final value would be 23:00:00
                instead of: 23:59:59 OR 00:00:00 (which would be midnight the NEXT day,
                but dates are INCLUSIVE so midnight the next day is technically
                out of date range)
        ---
        Returns:
            * tuple:
                * prices (DataFrame): bid/ask/mid/spreads for all OHLC prices and volume data
                for all time periods within time interval
                * allowance (dict):
                    * remainingAllowance: number of data points still available to fetch
                    within current allowance period
                    * totalAllowance: number of data points the API key and account
                    combination is allowed to fetch in any given allowance period
                    * allowanceExpiry: number of seconds till current allowance period
                    ends and remainingAllowance field is reset
                * instrument_type (str): e.g. CURRENCIES
        """
        # initialize flag at 0
        # i.e. not using and timeInterval (later updated if necessary)
        time_interval_flag = 0

        # range_type selection
        if range_type == "num_points":
            url = f"{self.url_base}/prices/{epic}/{resolution}/{num_points}"

            # number of times to loop requests.get for this range_type method
            n = 1

        elif range_type == "dates":
            # unpack dates to dates and timeInterval
            date_start, time_interval_start = start_date.split()
            date_end, time_interval_end = end_date.split()

            # condition to exclude time intervals
            # gets all data points possible
            # ignores 'weekdays' selection
            if time_interval_start == time_interval_end:
                url = (
                    f"{self.url_base}/prices/{epic}/{resolution}/{start_date}/{end_date}"
                )

                # number of times to loop requests.get for this range_type method
                n = 1

            else:
                # activate flag ONLY if 'dates' selected and time intervals DIFFER
                # 'weekdays' input only taken into account HERE
                time_interval_flag = 1

                # create date range taking into account 'weekdays' input
                date_range = pd.date_range(date_start, date_end)
                date_range = list(filter(lambda x: x.weekday() in weekdays, date_range))
                date_range = [x.strftime("%Y-%m-%d") for x in date_range]

                # number of times to loop requests.get for this range_type method
                n = len(date_range)

        header = self.header_base.copy()
        header["Version"] = "2"

        # initialize list for loop
        prices_historical = []

        for i in range(n):
            if time_interval_flag:
                start_date = f"{date_range[i]} {time_interval_start}"
                end_date = f"{date_range[i]} {time_interval_end}"
                url = (
                    f"{self.url_base}/prices/{epic}/{resolution}/{start_date}/{end_date}"
                )

            # prices: GET request
            # every request/loopIteration is 1 call to the API
            # we have limit of max 60 or 30 [unclear] per minute
            # need to sleep this section so that 1 call takes minimum 1s
            # [for limit of 60 per minute]
            # or 2s [for limit of 30 per minute]
            # in reality, so far 3s sleep throws no error, whereas 1s or 2s still gives error
            timer_start = time.time()

            r = requests.get(url=url, headers=header)

            timer_end = time.time()

            time_taken = timer_end - timer_start
            print(f"{time_taken:.2f} seconds for asset {epic} to run day {i+1}/{n}")

            # if NOT a single API call
            if n != 1:
                # number of seconds to sleep between each API call
                # to avoid exceeding unknown limit
                seconds_force_sleep = 3.0

                # sleep if time taken for request is less than value of seconds_force_sleep
                if time_taken < seconds_force_sleep:
                    time.sleep(seconds_force_sleep - time_taken)

            # store JSON result
            res = r.json()

            # early function exit if error
            if r.status_code != 200:
                print("ERROR OCCURED")
                print(f"STATUS CODE: {r.status_code}")
                print(r.content)
                print(res)

                # error codes link:
                # https://labs.ig.com/rest-trading-api-reference/service-detail?id=684

                return res

            # append prices info of each iteration in list container
            # NOTE:
            #   res['prices'] is a list
            #   each elem is a different point in times' price info
            prices_historical.extend(res["prices"])

        # unpack result
        allowance = res["allowance"]
        instrument_type = res["instrumentType"]

        ##########################
        # convert prices_historical list to 4 DataFrames
        # and then merge into 1 DataFrame with all fields: bid, ask, mid, spread, volume etc.
        ##########################
        # conversion inputs
        price_types = ["openPrice", "highPrice", "lowPrice", "closePrice"]
        last_traded_volume = []
        snapshot_times = []
        i = 0  # counter so we only gather snapshot_times values only ONCE

        # initialize output dict
        prices = {
            "bid": {k: [] for k in price_types},
            "ask": {k: [] for k in price_types},
        }

        # retrieve data in correct ordered way and place into DataFrames
        for k in prices:
            for t in prices_historical:
                for p_type in price_types:
                    prices[k][p_type].append(t[p_type][k])

                if i == 0:
                    last_traded_volume.append(t["lastTradedVolume"])
                    snapshot_times.append(pd.to_datetime(t["snapshotTime"]))

            prices[k] = pd.DataFrame(data=prices[k], index=snapshot_times)

            i += 1

        # create 'mid' DataFrame
        prices["mid"] = (prices["bid"][price_types] + prices["ask"][price_types]) / 2

        # create 'spread' DataFrame
        prices["spread"] = prices["ask"][price_types] - prices["bid"][price_types]

        # rename headers to shorten 'Prices' > 'Px'
        # and append type of field (bid, ask, mid, spread)
        for k in prices:
            prices[k].columns = prices[k].columns.str.replace(
                "Price", f"_px_{k}"
            )

        # merge the DataFrames and add last_traded_volume column
        prices = pd.concat([prices[k] for k in prices], axis=1)
        prices["last_traded_volume"] = last_traded_volume
        ##########################
        # end of conversion from list to 1 DataFrame
        ##########################

        return prices, allowance, instrument_type

    def get_prices_all_assets(
        self,
        assets: dict,
        resolution: str,
        range_type: str,
        start_date: str = None,
        end_date: str = None,
        weekdays: tuple[int] = (0, 1, 2, 3, 4, 5, 6),
        num_points: int = None,
    ) -> tuple[dict]:
        """
        Get prices DataFrame (bid/ask/mid/spreads for all OHLC prices and volume)
        for all assets in 'assets' dict for given parameters and time interval;
        also returns 'allowance' dict
        (resets every 7 days to 10,000 historical price data points).

        ---
        Args:
            * assets (dict): dict of assets with their epics
            * resolution (str): price resolution
                * SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10,
                MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH
            * range_type (str):
                * 'num_points': use num_points argument
                * 'dates': use start_date/end_date arguments with given timeInterval (see below)
            * start_date (str, opt. depending on range_type):
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates time_interval_start
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * end_date (str, opt. depending on range_type):
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates time_interval_end
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * weekdays (tup[int], opt.):
                * which days of the week to get data for (0: Mon, 6: Sun)
                * defaults to all days of the week (0, 1, 2, 3, 4, 5, 6)
                * NOTE: this is only applied to the code when the time portion
                of the date range is different
            * num_points (int, opt. depending on range_type):
                * get last num_points data points
                * defaults to None
        ---
        Notes to start_date/end_date:
            * if the time portions are the SAME (00:00:00) then data is fetched using
            ALL the 24 hours in EVERY single day available ('weekdays' parameter is IGNORED)
            * if the time portions are DIFFERENT from one another, then the timeInterval and
            'weekdays' parameter is applied
            * during the timeInterval technique, note that the time rounds DOWNWARDS
                * i.e. if getting HOURLY data from 00:00:00-23:59:59 final value would be 23:00:00
                instead of: 23:59:59 OR 00:00:00 (which would be midnight the NEXT day,
                but dates are INCLUSIVE so midnight the next day is technically
                out of date range)
        ---
        Returns:
            * tuple:
                * assets (dict): updated with 'prices' and 'instrument_type' keys for each
                asset (each asset is the first layer of keys)
                    * prices (DataFrame): bid/ask/mid/spreads for all OHLC prices
                    and volume data for all time periods within time interval
                    * instrument_type (str): e.g. CURRENCIES

                * allowance (dict):
                    * remainingAllowance: number of data points still available to fetch
                    within current allowance period
                    * totalAllowance: number of data points the API key and account
                    combination is allowed to fetch in any given allowance period
                    * allowanceExpiry: number of seconds till current allowance period
                    ends and remainingAllowance field is reset
        """
        for asset in assets:
            epic = assets[asset]["epic"]

            prices, allowance, instrument_type = self.get_prices_single_asset(
                epic, resolution, range_type, start_date, end_date, weekdays, num_points
            )

            assets[asset]["prices"] = prices
            assets[asset]["instrument_type"] = instrument_type

        return assets, allowance
