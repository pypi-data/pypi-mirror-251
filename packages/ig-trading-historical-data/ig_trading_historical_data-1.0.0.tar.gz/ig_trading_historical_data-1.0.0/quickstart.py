# import packages
from ig_trading_historical_data import IG_API
import user_info
from pprint import pprint  # for nicer dictionary printing


""" input user information """

# account details
demo = 1  # 1: using demo account / 0: using live account
username = user_info.username
pw = user_info.pw
api_key = user_info.api_key

# let's say you want data for 'Microsoft' and 'GBPUSD Forward'
# format of the 'assets' dictionary:
assets = {
    
    'GBPUSD Forward': {  # asset name in normal language (without slashes)
        'instrument_name': 'GBP/USD Forward',  # asset name in EXACT way as seen on IG web platform (with slashes if relevant)
        'expiry': 'MAR-24'  # either 'DFB' or the expiration date
    },

    'Microsoft': {  # another asset example
        'instrument_name': 'Microsoft Corp (All Sessions)',  
        'expiry': 'DFB'
    },
}

# historical data inputs
resolution = 'MINUTE_5'  # price resolution (SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
range_type = 'num_points'  # 'num_points' or 'dates'
num_points = 1  # ignored if range_type == 'dates'
start_date = '2024-01-08 10:00:00'  # yyyy-MM-dd HH:mm:ss (inclusive dates and times)
end_date = '2024-01-10 10:30:00'  # yyyy-MM-dd HH:mm:ss (inclusive dates and times)
weekdays = (0, 2)  # 0: Mon, 6: Sun (deactivated if time portion above is equal) 


""" API key usage """

# logging in / make a class instance
ig_api = IG_API(demo, username, pw, api_key)

# get epics automatically and update 'assets' dict with respective epics
assets = ig_api.get_epics(assets)

# view epics
pprint(assets) 

# get historical prices
assets, allowance = ig_api.get_prices_all_assets(
    assets, 
    resolution, 
    range_type, 
    start_date,
    end_date,
    weekdays,
    num_points
)

# view data fields
print(assets['GBPUSD Forward']['prices'].columns)

# view pricing data (17 columns of data fields)
print(assets['GBPUSD Forward']['prices'])
print(assets['Microsoft']['prices'])


""" sample of other available values """

# view remaining quota for the week
pprint(allowance)

# view instrument types
pprint(assets['GBPUSD Forward']['instrument_type'])
pprint(assets['Microsoft']['instrument_type'])
