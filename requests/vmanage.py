#! /usr/bin/env python

import logging

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(filename="sdwan.log", level=logging.INFO)


class Authentication:
    def __init__(self, host, port=443, user=None, password=None, validate_certs=False, timeout=10):
        """
        Initialize Authentication object with session parameters.

        Args:
            host (str): hostname or IP address of vManage
            user (str): username for authentication
            password (str): password for authentication
            port (int): default HTTPS port 443
            validate_certs (bool): turn certificate validation on or off.
            timeout (int): how long Requests will wait for a response from the server, default 10 seconds
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout
        self.base_url = f"https://{self.host}:{self.port}"
        self.session = requests.Session()
        self.session.verify = validate_certs
        self.jsessionid = None

    def login(self):
        api = "/j_security_check"
        url = f"{self.base_url}{api}"
        payload = {"j_username": self.user, "j_password": self.password}

        try:
            response = self.session.post(url, data=payload, timeout=self.timeout)
            logger.info(f"login - Status code: {response.status_code}")
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"HTTP request failed during login: {e}")
            return None

        cookies = response.headers.get("Set-Cookie")
        if not cookies:
            logger.error("No valid Set-Cookie header returned")
            return None

        self.jsessionid = cookies.split(";")[0]
        return self.jsessionid

    def get_token(self):
        if not self.jsessionid:
            logger.error("JSESSIONID is not set. Please log in first.")
            return None

        headers = {"Cookie": self.jsessionid}
        api = "/dataservice/client/token"
        url = f"{self.base_url}{api}"

        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            logger.info(f"get token - Status code: {response.status_code}")
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"HTTP request failed while fetching token: {e}")
            return None

        return response.text if response.status_code == 200 else None
