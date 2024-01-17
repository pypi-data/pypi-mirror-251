import os
import re
import time
import random
import string
import requests


class Atlas:
    def __init__(self):
        self.domain = os.environ.get("ATLAS_DOMAIN")
        self.identify = os.environ.get("ATLAS_IDENTIFY")
        self.token = os.environ.get("ATLAS_TOKEN")
        self.url = f"http://{self.identify}.{self.domain}"

    def get_subdomain(self):
        return f'{self.identify}.{self.domain}'

    def verify_request(self, flag, type="web"):
        ret_val = False
        counts = 3
        url = f"http://api.{self.domain}/{type}/search/{flag}"
        while counts:
            try:
                time.sleep(1)
                resp = requests.get(url, headers={"Atlas": self.token})
                if resp and resp.status_code == 200 and flag in resp.text:
                    ret_val = True
                    break
            except Exception as ex:
                time.sleep(1)
            counts -= 1
        return ret_val

    def build_request(self, value="poc", type="web"):
        ranstr = self.get_random_str(4).lower()
        domain = self.get_subdomain()
        url = ""
        if type == "web":
            url = "http://{}.{}/{}{}{}".format(ranstr, domain, ranstr, value, ranstr)
        elif type == "dns":
            url = "{}{}{}.{}".format(ranstr, re.sub(r"\W", "", value), ranstr, domain)
        return {"url": url, "flag": ranstr}

    def get_random_str(self, length=4):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))
