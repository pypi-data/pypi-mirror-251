from trimble.id._constants import PACKAGE_NAME
from .analytics_http_client import AnalyticsHttpClient
import pkg_resources  

class FixedEndpointProvider:
    """
    An endpoint provider that returns fixed OAuth endpoints
    """
    def __init__(self, authorizationEndpoint, tokenEndpoint, userInfoEndpoint, tokenRevocationEndpoint = None, jwksEndpoint = None, productName = None):
        """
        Initialize FixedEndpointProvider class

        :param authorizationEndpoint: Set Authorization Endpoint
        :param tokenEndpoint: Set Token Endpoint
        :param userInfoEndpoint: Set UserInfo Endpoint
        :param tokenRevocationEndpoint: Set Token revocation Endpoint
        :param jwksEndpoint: Set JSON Web key set Endpoint
        :param productName: Product name of the consuming application (optional)
        """
        self._authorizationEndpoint = authorizationEndpoint
        self._tokenEndpoint = tokenEndpoint
        self._userInfoEndpoint = userInfoEndpoint
        self._tokenRevocationEndpoint = tokenRevocationEndpoint
        self._jwksEndpoint = jwksEndpoint
        self._version = pkg_resources.require(PACKAGE_NAME)[0].version

        AnalyticsHttpClient.send_init_event(
            name=self.__class__.__name__, 
            client_name=PACKAGE_NAME, 
            client_version=self._version)

    async def retrieve_authorization_endpoint(self):
        """
        Retrieves a fixed Authorization endpoint
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_authorization_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._authorizationEndpoint

    async def retrieve_token_endpoint(self):
        """
        Retrieves a fixed Token endpoint
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_token_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._tokenEndpoint

    async def retrieve_json_web_keyset_endpoint(self):
        """
        Retrieves a fixed JSON Web key set endpoint
        """
        AnalyticsHttpClient.send_method_event(
            name=f"{self.__class__.__name__}_retrieve_json_web_keyset_endpoint", 
            client_name=PACKAGE_NAME, 
            client_version=self._version)
        return self._jwksEndpoint