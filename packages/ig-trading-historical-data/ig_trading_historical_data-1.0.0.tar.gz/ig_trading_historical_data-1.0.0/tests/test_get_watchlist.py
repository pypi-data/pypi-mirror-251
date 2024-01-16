import json
import responses
import pytest_mock

from ig_trading_historical_data import IG_API
import tests.data.mock_user_info_demo as muid


class TestGetWatchlist:
    """ unit tests for get_watchlist() method """

    @responses.activate
    def test_get_watchlist(self, mocker):
        """ get watchlist """
        
        """ mocking the class initialization """
        # create mocked object
        mocked_init = mocker.patch.object(
            IG_API, 
            '__init__',
            return_value=None
        )

        # mock initialize
        ig_api = IG_API(**muid.mock_user_info_demo)

        # set mock attributes
        ig_api.url_base = muid.mock_url_base
        ig_api.header_base = muid.mock_header_base


        """ test .get_watchlist() """

        # prepare watchlist information
        with open("tests/data/mock_watchlist.json", "r") as f:
            mock_watchlist_response_json = json.load(f)

        # mock the request.get inside the method
        mock_watchlist_url = "https://demo-api.ig.com/gateway/deal/watchlists"

        responses.get(
            mock_watchlist_url,
            json=mock_watchlist_response_json,
            status=200
        )

        # run method
        result = ig_api.get_watchlist()

        assert result['watchlists'][0]['id'] == mock_watchlist_response_json['watchlists'][0]['id']
        assert result['watchlists'][5]['name'] == mock_watchlist_response_json['watchlists'][5]['name']
