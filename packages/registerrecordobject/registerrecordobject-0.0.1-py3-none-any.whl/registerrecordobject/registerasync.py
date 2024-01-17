from typing import Dict
from aiohttp import ClientResponse
import aiohttp


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

    async def register(self, data: Dict) -> ClientResponse:
        """
        Register a record in RegisterRecord
        :param data: Data to register - Dict
        :return: requests.Response
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url_metrics, json=data) as response:
                return response

    async def test(self) -> ClientResponse:
        """
        Test if RegisterRecord is up
        :return: requests.Response
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url_test) as response:
                return response


"""
async def run_async():
    register_record = RegisterRecordObjectAsync(url="http://localhost:3001")
    response_test:ClientResponse = await register_record.test()
    assert (response_test.status == 200)

    response_register: ClientResponse = await register_record.register(data={"test": "test", "service": "test-python"})
    assert (response_register.status == 200)
"""
