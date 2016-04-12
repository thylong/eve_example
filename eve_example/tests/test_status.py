import unittest
from .test_base import TestBase


class StatusTest(TestBase):
    def test_endpoint(self):
        response = self.client.get('/status')
        data, status = self.parse_response(response)

        self.assertEquals(200, status)

if __name__ == '__main__':
    unittest.main()
