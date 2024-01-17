"""
Clappform API Wrapper
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022 Clappform B.V..
:license: MIT, see LICENSE for more details.
"""
__requires__ = ["requests==2.28.1", "pandas==1.5.2"]

# Metadata
__version__ = "0.0.0"
__author__ = "Clappform B.V."
__email__ = "info@clappform.com"
__license__ = "MIT"
__doc__ = "Clappform Python API wrapper"


import logging
import json
import requests


class RudholmException(Exception):
    """Integration Exceptions Class"""

class Rudholm:
    # Define a list of supported endpoints with their paths and HTTP methods


    def __init__(self, url: str, headers: dict, version: str = "v1", timeout: int = 5):
        """Initialize the Rudholm client.

        Args:
            url (str): Base URL of the Rudholm API.
            headers (dict): Headers to be included in API requests.
            version (str, optional): API version. Defaults to "v1".
            timeout (int, optional): Request timeout in seconds. Defaults to 5.
        """
        self.headers = headers
        self.timeout = timeout
        self.url = url
        self.version = version
        self.base_url = f"https://{url}/api/{version}"

        self.endpoints = []
        with open('endpoints.json', 'r', encoding="utf-8") as f:
            self.endpoints = json.load(f)

    def __get_endpoint(self, endpoint_id: str) -> dict:
        """Find and retrieve information about a specific endpoint.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.

        Returns:
            dict: Information about the endpoint.
        """
        endpoint = next(
            (item for item in self.endpoints if item["endpoint_id"] == endpoint_id),
            None,
        )

        if endpoint is None:
            logging.error("%s not found in supported endpoints.", endpoint_id)
            raise RudholmException()  # Define the Rudholm Exception class
        return {} if endpoint is None else endpoint

    def __add_url_segment(self, base_url: str, segment: str):
        """Add a URL segment to the base URL if the segment is not empty.

        Args:
            base_url (str): The base URL to which the segment may be added.
            segment (str): The segment to be added to the URL.

        Returns:
            str: The updated URL with the added segment.
        """
        if segment:
            return f"{base_url}/{segment}"
        return base_url

    def __add_query_parameters(
        self,
        base_url: str,
        **kwargs):
        """Add a query parameter to the base URL if the parameter value is not empty.

        Args:
            base_url (str): The base URL to which the query parameter may be added.
            parameter_name (str): The name of the query parameter.
            parameter_value (str): The value of the query parameter.

        Returns:
            str: The updated URL with the query parameter.
        """
        count = 0
        for key, value in kwargs.items():
            operator = "&"
            if count == 0:
                operator = "?"

            base_url = f"{base_url}{operator}{key}={value}"
            count += 1
        return base_url

    def __build_api_url(
        self, endpoint_id: str, item_id: str = "", **kwargs) -> str:
        """Generate the complete URL for a specific endpoint.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.
            item_id (str, optional): Identifier for an optional ID. Defaults to "".

        Returns:
            str: Complete URL for the API request.
        """
        endpoint = self.__get_endpoint(endpoint_id)
        partial_url = f"{self.base_url}/{endpoint['path']}"

        partial_url = self.__add_query_parameters(partial_url, **kwargs)

        # Add the item_id if provided
        partial_url = self.__add_url_segment(partial_url, item_id)

        # Finally, for each route, determine if some additional specification is needed
        partial_url = self.__add_url_segment(
            partial_url, endpoint.get('path_extension', ''))
        method = endpoint['method']

        logging.debug("Generated URL: %s with method %s", partial_url, method)
        return {
            'partial_url': partial_url,
            'method': method
        }

    def __fetch_data(
            self,
            base_url: str,
            method: str,
            body: dict = None
        ) -> list:
        """Send an API request and fetch the data.

        Args:
            base_url (str): Complete URL for the API request.
            method (str): HTTP method (GET, PUT, POST, DELETE).
            body (dict, optional): Request body for POST and PUT requests.

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        if body is None:
            body = {}
        data = {
            'response_code': 0,
            'response_data': ""
        }

        logging.debug("API URL: %s", base_url)

        response = requests.request(method,
            base_url, headers=self.headers, json=body, timeout=self.timeout)

        data['response_code'] = response.status_code

        try:
            data['response_data'] = response.json()
        except json.JSONDecodeError as e:
            logging.debug("Failed to decode response for URL: %s, %s", base_url, e)

        return data

    def fetch_all(
            self,
            endpoint_id: str,
            **kwargs
        ) -> list:
        """Fetch data from an endpoint with no specific item ID.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        request_url = self.__build_api_url(endpoint_id=endpoint_id, **kwargs)
        return self.__fetch_data(request_url['partial_url'], request_url['method'])

    def fetch_one(self, endpoint_id: str, item_id: str = "", body: dict = None) -> list:
        """Fetch data for a specific item from an endpoint.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.
            item_id (str): Identifier for the specific item.
            body (dict, optional): Request body for POST and PUT requests.

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        if body is None:
            body = {}
        request_url = self.__build_api_url(
            endpoint_id=endpoint_id, item_id=item_id
        )

        return self.__fetch_data(
            request_url['partial_url'], request_url['method'], body)

    def fetch_templates_mandatory(self):
        """Fetch all templates with their required fields.

        Args:

        Returns:
            list: A list containing template response.
        """

        # Initialize Rudholm
        _trims = Rudholm(self.url, self.headers, self.version, self.timeout)

        response_templates = _trims.fetch_all(endpoint_id='templates')
        templates = response_templates["response_data"]

        for i in templates:
            resp_mandatory_fields = _trims.fetch_one(
                endpoint_id='templates_one',
                item_id=i['identifier']
            )

            if resp_mandatory_fields["response_code"] == 200:
                i['mandatory_fields'] = resp_mandatory_fields['response_data']
        return templates
