""" initialize class variables """

mock_user_info_demo = {
    "demo": 1,
    "username": "test_username",
    "pw": "test_pw",
    "api_key": "test_api_key"
}

mock_url_base = 'https://demo-api.ig.com/gateway/deal'

mock_header_base = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json; charset=UTF-8',
    'X-IG-API-KEY': mock_user_info_demo['api_key'],
    'CST': 'test_CST',
    'X-SECURITY-TOKEN': 'test_X-SECURITY-TOKEN'
}
