import os
import time
import unittest
from poclib3.atlas import Atlas


class TestAtlas(unittest.TestCase):

    def test_http_record(self):
        atlas = Atlas()
        flag = atlas.build_request(type="web")
        os.system("curl " + flag["url"])
        time.sleep(1)
        self.assertTrue(atlas.verify_request(flag["flag"], type="web"))

    def test_dns_record(self):
        atlas = Atlas()
        flag = atlas.build_request(type="dns")
        os.system("ping -nc 2 " + flag["url"])
        time.sleep(1)
        self.assertTrue(atlas.verify_request(flag["flag"], type="dns"))


if __name__ == "__main__":
    unittest.main()
