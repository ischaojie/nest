import click
import requests
import uuid
import time
import hashlib

AUTH = {
    "youdao": {
        "APP_KEY": "218f4a5913a2b64d",
        "APP_SECRET": "tn49UOKE8VBy5zezLGWjr8HnusRMcxW8",
        "URL": "https://openapi.youdao.com/api",
    },
    "baidu": {
        "APP_KEY": "20200807000534875",
        "APP_SECRET": "4rpXNwhV0dpMaZFiXFui",
        "URL": "https://fanyi-api.baidu.com/api/trans/vip/translate",
    },
}


class BaseTranslate(object):
    def __init__(self, q, src, to):
        self.q = q
        self.src = src
        self.to = to

    @staticmethod
    def request(url: str, data: dict):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(url=url, data=data, headers=headers)
        return resp.json()

    @staticmethod
    def status(s):
        return "\033[1m{0}\033[0m".format(s)


class YoudaoTranslate(BaseTranslate):
    def __init__(self, q, src, to):
        super().__init__(q, src, to)

        self.current_time = str(int(time.time()))
        self.salt = str(uuid.uuid4())
        self.sign = self.encrypt()

    def trans(self):

        trans_data = {
            "q": self.q,
            "from": self.src,
            "to": self.to,
            "appKey": AUTH["youdao"]["APP_KEY"],
            "salt": self.salt,
            "sign": self.sign,
            "signType": "v3",
            "curtime": self.current_time,
        }

        resp = self.request(AUTH["youdao"]["URL"], trans_data)

        result = []

        # base translation
        base_result = resp["translation"][0]

        # web translation and explains
        try:
            web_result = resp["web"]
            explains = resp["basic"]["explains"]
        except KeyError as e:
            web_result = ""
            explains = ""

        # if is word
        is_word = resp["isWord"]
        if is_word:
            result.append(base_result)
            result.append("\033[1;31m---\033[0m")
            result.append("\033[1;31m词性:\033[0m")
            for exp in explains:
                result.append(exp)
            result.append("\033[1;31m---\033[0m")
            result.append("\033[1;31m网络释义:\033[0m")
            for web in web_result:
                value = ",".join(web["value"])
                result.append(web["key"] + ":" + value)
        else:
            result.append(base_result)

        result = "\n".join(result)

        error_code = resp["errorCode"]

        if error_code != "0":
            if error_code == "102":
                result = "不支持的语言类型!"
            elif error_code == "103":
                result = "翻译文本过长!"
        return result

    def encrypt(self):
        sign_str = (
            AUTH["youdao"]["APP_KEY"]
            + self.truncate()
            + self.salt
            + self.current_time
            + AUTH["youdao"]["APP_SECRET"]
        )
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign_str.encode("utf-8"))
        return hash_algorithm.hexdigest()

    def truncate(self):
        if self.q is None:
            return None
        size = len(self.q)
        return (
            self.q
            if size <= 20
            else self.q[0:10] + str(size) + self.q[size - 10 : size]
        )


class BaiduTranslate(BaseTranslate):
    def __init__(self, q, src, to):
        super(BaiduTranslate, self).__init__(q, src, to)
        self.salt = str(uuid.uuid4())
        self.sign = self.encrypt()

    def trans(self):
        trans_data = {
            "q": self.q,
            "from": self.src,
            "to": self.to,
            "appid": AUTH["baidu"]["APP_KEY"],
            "salt": self.salt,
            "sign": self.sign,
        }

        resp = self.request(AUTH["baidu"]["URL"], trans_data)

        result = []

        dst = resp["trans_result"][0]["dst"]
        result.append(dst)

        return "\n".join(result)

    def encrypt(self):
        sign_str = (
            AUTH["baidu"]["APP_KEY"] + self.q + self.salt + AUTH["baidu"]["APP_SECRET"]
        )
        hash_algorithm = hashlib.md5()
        hash_algorithm.update(sign_str.encode("utf-8"))
        return hash_algorithm.hexdigest()


class GoogleTranslate(BaseTranslate):
    pass


# trans
def trans(q: str, engine="youdao", src="auto", to="auto") -> str:
    youdao = YoudaoTranslate(q, src, to)
    google = GoogleTranslate(q, src, to)
    baidu = BaiduTranslate(q, src, to)

    result = ""

    if engine == "youdao":
        result = youdao.trans()
    elif engine == "baidu":
        result = baidu.trans()
    elif engine == "google":
        result = google.trans()
    else:
        result = "仅支持有道&百度"

    return result
