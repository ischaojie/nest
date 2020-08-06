import click
import requests
import uuid
import time
import hashlib

APP_KEY = "218f4a5913a2b64d"
APP_SECRET = "tn49UOKE8VBy5zezLGWjr8HnusRMcxW8"
YOUDAO_URL = "https://openapi.youdao.com/api"


class BaseTranslate(object):
    def __init__(self, q, src, to):
        self.q = q
        self.src = src
        self.to = to

    @staticmethod
    def http_get(url: str, data: dict):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(url=url, data=data, headers=headers)
        return resp.json()

    @staticmethod
    def status(s):
        return '\033[1m{0}\033[0m'.format(s)


class YoudaoTranslate(BaseTranslate):

    def __init__(self, q, src, to):
        super().__init__(q, src, to)

        self.current_time = str(int(time.time()))
        self.salt = str(uuid.uuid4())
        self.sign_str = APP_KEY + self.truncate() + self.salt + self.current_time + APP_SECRET
        self.sign = self.encrypt()

    def trans(self):

        trans_data = {
            "from": self.src,
            "to": self.to,
            "signType": "v3",
            "curtime": self.current_time,
            "appKey": APP_KEY,
            "q": self.q,
            "salt": self.salt,
            "sign": self.sign
        }

        resp = self.http_get(YOUDAO_URL, trans_data)

        result = ''

        # base translation
        base_result = resp['translation'][0]

        # web translation
        try:
            web_result = resp['web']
            explains = resp['basic']['explains']
        except KeyError as e:
            web_result = ''
            explains = ''

        # if is word
        is_word = resp['isWord']
        if is_word:
            result += base_result + '\n'
            result += '\033[1;31m---\033[0m\n'
            result += '\033[1;31m词性:\033[0m\n'
            for exp in explains:
                result += exp + '\n'
            result += '\033[1;31m---\033[0m\n'
            result += '\033[1;31m网络释义:\033[0m\n'
            for web in web_result:
                value = ','.join(web['value'])
                result += web['key'] + ':' + value + '\n'
        else:
            result += base_result + '\n'

        error_code = resp['errorCode']

        if error_code != '0':
            if error_code == '102':
                result = '不支持的语言类型!'
            elif error_code == '103':
                result = '翻译文本过长!'
        return result

    def encrypt(self):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(self.sign_str.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self):
        if self.q is None:
            return None
        size = len(self.q)
        return self.q if size <= 20 else self.q[0:10] + str(size) + self.q[size - 10:size]


class GoogleTranslate(BaseTranslate):
    pass


# trans
def trans(q, translate='youdao', src='auto', to='auto'):
    youdao = YoudaoTranslate(q, src, to)
    google = GoogleTranslate(q, src, to)

    result = ''

    if translate == 'youdao':
        result = youdao.trans()
    elif translate == 'google':
        result = google.trans()

    return result


@click.command()
@click.option('--src', default='auto', help="source language")
@click.option('--to', default='auto', help="target language")
@click.option('--translate', default='youdao', help="translate engine")
@click.argument('q')
def trans_cli(q, translate, src, to):
    """this is a translation tool."""
    click.echo("翻译结果来自: %s" % translate)
    click.echo("\033[1;31m---------------------\033[0m")
    result = trans(q, src=src, to=to)
    click.echo(result)


if __name__ == "__main__":
    trans_cli()
