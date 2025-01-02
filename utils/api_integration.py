# api_integration.py
import requests
import logging
import time
from requests.exceptions import RequestException, HTTPError, Timeout

class APIIntegration:
    def __init__(self, base_url, api_key=None, headers=None, retries=3, timeout=10):
        """
        Initialize the API integration with base URL, API key, headers, and retry policy.
        :param base_url: The base URL for the API.
        :param api_key: API key for authentication (optional).
        :param headers: Additional headers for the requests (optional).
        :param retries: Number of retry attempts on failure (default is 3).
        :param timeout: Timeout for requests (default is 10 seconds).
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = headers or {}
        self.retries = retries
        self.timeout = timeout
        self.logger = logging.getLogger("APIIntegration")
        self.logger.setLevel(logging.DEBUG)
        
        # Set the Authorization header if API key is provided
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        self.logger.info(f"Initialized APIIntegration with base URL: {self.base_url}")

    def send_get_request(self, endpoint, params=None):
        """
        Send a GET request to the specified endpoint with optional query parameters.
        :param endpoint: API endpoint to send the GET request to.
        :param params: Optional query parameters.
        :return: The response JSON data or None in case of failure.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self._make_request("GET", url, params=params)
            return response.json() if response else None
        except Exception as e:
            self.logger.error(f"Error sending GET request to {url}: {str(e)}")
            return None

    def send_post_request(self, endpoint, data=None):
        """
        Send a POST request to the specified endpoint with optional data.
        :param endpoint: API endpoint to send the POST request to.
        :param data: Optional data for the POST request (usually JSON format).
        :return: The response JSON data or None in case of failure.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self._make_request("POST", url, json_data=data)
            return response.json() if response else None
        except Exception as e:
            self.logger.error(f"Error sending POST request to {url}: {str(e)}")
            return None

    def send_put_request(self, endpoint, data=None):
        """
        Send a PUT request to the specified endpoint with optional data.
        :param endpoint: API endpoint to send the PUT request to.
        :param data: Optional data for the PUT request (usually JSON format).
        :return: The response JSON data or None in case of failure.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self._make_request("PUT", url, json_data=data)
            return response.json() if response else None
        except Exception as e:
            self.logger.error(f"Error sending PUT request to {url}: {str(e)}")
            return None

    def send_delete_request(self, endpoint):
        """
        Send a DELETE request to the specified endpoint.
        :param endpoint: API endpoint to send the DELETE request to.
        :return: The response JSON data or None in case of failure.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self._make_request("DELETE", url)
            return response.json() if response else None
        except Exception as e:
            self.logger.error(f"Error sending DELETE request to {url}: {str(e)}")
            return None

    def _make_request(self, method, url, params=None, json_data=None):
        """
        A helper method to make HTTP requests (GET, POST, PUT, DELETE).
        Handles retries, timeout, and error logging.
        :param method: HTTP method (GET, POST, PUT, DELETE).
        :param url: The full URL to make the request to.
        :param params: Optional query parameters.
        :param json_data: Optional JSON data for POST/PUT requests.
        :return: The HTTP response object.
        """
        attempts = 0
        while attempts < self.retries:
            try:
                if method == "GET":
                    response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
                elif method == "POST":
                    response = requests.post(url, headers=self.headers, json=json_data, timeout=self.timeout)
                elif method == "PUT":
                    response = requests.put(url, headers=self.headers, json=json_data, timeout=self.timeout)
                elif method == "DELETE":
                    response = requests.delete(url, headers=self.headers, timeout=self.timeout)
                else:
                    self.logger.error(f"Unsupported HTTP method: {method}")
                    return None
                
                # Check for successful response
                if response.status_code == 200:
                    return response
                else:
                    # Log HTTP errors (e.g., 4xx, 5xx)
                    self.logger.error(f"HTTP error {response.status_code} - {response.text}")
                    break
            except Timeout:
                self.logger.warning(f"Request timed out. Retrying... (Attempt {attempts + 1}/{self.retries})")
            except HTTPError as e:
                self.logger.error(f"HTTPError occurred: {e}")
                break
            except RequestException as e:
                self.logger.error(f"RequestException occurred: {e}")
                break
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {str(e)}")
                break
            
            # Retry if the request fails
            attempts += 1
            time.sleep(2 ** attempts)  # Exponential backoff
        
        return None

    def get_status_code(self, endpoint, params=None):
        """
        Get the HTTP status code for a GET request.
        :param endpoint: The endpoint to send the GET request to.
        :param params: Optional query parameters.
        :return: HTTP status code or None in case of failure.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self._make_request("GET", url, params=params)
            if response:
                return response.status_code
        except Exception as e:
            self.logger.error(f"Error getting status code for {url}: {str(e)}")
        return None

    def handle_error(self, status_code, error_message):
        """
        Handle errors based on the status code and log appropriate error messages.
        :param status_code: HTTP status code.
        :param error_message: Error message to log.
        """
        if status_code >= 400 and status_code < 500:
            self.logger.error(f"Client Error ({status_code}): {error_message}")
        elif status_code >= 500:
            self.logger.error(f"Server Error ({status_code}): {error_message}")
        else:
            self.logger.error(f"Unexpected Error ({status_code}): {error_message}")

    def test_connection(self):
        """
        Test the connection to the API by sending a simple GET request to the root endpoint.
        :return: Boolean indicating whether the connection was successful.
        """
        try:
            response = self.send_get_request("")
            if response is not None:
                self.logger.info("Connection to API was successful.")
                return True
            else:
                self.logger.error("Failed to connect to API.")
                return False
        except Exception as e:
            self.logger.error(f"Error testing API connection: {str(e)}")
            return False
