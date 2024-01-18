import json

from trimble.id._constants import PACKAGE_NAME
from .http_client import HttpClient
from .analytics_http_client import AnalyticsHttpClient
import pkg_resources  

class RefreshableTokenProvider:
    """
    A refreshable token provider based on the OAuth refresh token grant type
    """
    def __init__(self, endpointProvider, consumerKey, consumerSecret, token, productName = None):
        """
        Initialize RefreshableTokenProvider class

        :param endpointProvider: An endpoint provider that provides the URL for the Trimble Identity token endpoint
        :param consumerKey: The consumer key for the calling application
        :param consumerSecret: The consumer secret for the calling application
        :param token: The initial access token issued for the authenticated user
        :param productName: Product name of the calling application
        """
        self._endpointProvider = endpointProvider
        self._consumerKey = consumerKey
        self._consumerSecret = consumerSecret
        self._token = token

        self._version = pkg_resources.require(PACKAGE_NAME)[0].version
        self._productName = productName

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_token(self):
        """
        Retrieves an access token for the application using refresh grant type

        :return: The access token for the given application
        """

        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_token", 
            client_name=PACKAGE_NAME, 
            client_version=self._version,
            application_id=self._consumerKey)

        tokenEndpoint = await self._endpointProvider.retrieve_token_endpoint()
        client = HttpClient('', {})
        result = await client.post(
            tokenEndpoint, 
            'grant_type=refresh_token&client_id=' + self._consumerKey + '&client_secret=' + self._consumerSecret, 
            { 'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json', 'user-agent': f"TrimbleCloud.Authentication/{self._version} python-sdk {self._productName}" }
        )
        jsonResult = json.loads(result)
        return jsonResult['access_token']