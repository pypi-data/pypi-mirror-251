from typing import Dict
import requests
from requests import Response


class RegisterRecordObject:
    """
    RegisterRecord object to register data in RegisterRecord
    """

    def __init__(self, url: str):
        """
        Constructor
        :param url: URL of RegisterRecord - str
        """
        url = url.rstrip("/")
        self.url = url
        self.url_metrics = f"{url}/registerRecord/v1/metric/register"
        self.url_test = f"{url}/registerRecord/v1/test"

    def register(self, data: Dict) -> Response:
        """
        Register a record in RegisterRecord
        :param data: Data to register - Dict
        :return: requests.Response
        """
        return requests.post(url=self.url_metrics, json=data)

    def test(self) -> Response:
        """
        Test if RegisterRecord is up
        :return: requests.Response
        """
        return requests.get(url=self.url_test)


"""
def run_sync():
    register_record = RegisterRecordObjectSync(url="http://localhost:3001")
    response_test = register_record.test()
    assert(response_test.status_code == 200)

    response_register: Response = register_record.register(data={"test": "test", "service": "test-python"})
    assert(response_register.status_code == 200)
"""
