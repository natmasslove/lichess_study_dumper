import urllib3
from urllib.parse import urljoin, urlencode
import json


class Urllib3Exception(Exception):
    pass


class Urllib3Helper:
    def __init__(self, base_url: str) -> None:
        """_summary_

        Args:
            base_url (_type_): base url to requests like http://localhost:3000/
        """
        self.http = urllib3.PoolManager()
        self.base_url = base_url

    def _prep_headers(self, token: str | None = None) -> dict:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _get_api_url(self, api_path: str) -> str:
        """
        Construct the full API URL from the base URL and API path.
        """
        api_path = api_path.lstrip("/")  # Ensure no leading slash in api_path
        url = urljoin(self.base_url, api_path)
        return url

    def get(
        self, api_path: str, params: dict | None = None, token: str | None = None
    ) -> str:
        """
        Makes a GET request to the specified API path with optional query parameters.

        Args:
            api_path (str): API path to append to the base URL.
            params (dict, optional): Query parameters for the GET request. Defaults to None.
            token (str, optional): Authorization token. Defaults to None.

        Returns:
            dict: Decoded JSON response.

        Raises:
            Urllib3Exception: If the request fails or an error occurs.
        """
        url = self._get_api_url(api_path)
        if params:
            url += f"?{urlencode(params)}"

        headers = self._prep_headers(token)

        try:
            response = self.http.request(
                method="GET",
                url=url,
                headers=headers,
            )

            if response.status == 200:
                return response.data.decode("utf-8")
            else:
                raise Urllib3Exception(
                    f"GET request failed: {response.status} {response.data.decode('utf-8')}"
                )
        except Exception as e:
            raise Urllib3Exception(f"An error occurred during GET: {str(e)}")
