import click
import requests
import uuid
import time
import hashlib

APP_KEY = "218f4a5913a2b64d"
APP_SECRET = "tn49UOKE8VBy5zezLGWjr8HnusRMcxW8"
YOUDAO_URL = "https://openapi.youdao.com/api"


def http_get(url: str, data: dict):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(url=url, data=data, headers=headers)
    return resp.json()


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def translate(q, source="auto", to="auto"):

    current_time = str(int(time.time()))
    salt = str(uuid.uuid4())
    signStr = APP_KEY + truncate(q) + salt + current_time + APP_SECRET
    sign = encrypt(signStr)

    trans_data = {
        "from": source,
        "to": to,
        "signType": "v3",
        "curtime": current_time,
        "appKey": APP_KEY,
        "q": q,
        "salt": salt,
        "sign": sign
    }

    resp = http_get(YOUDAO_URL, trans_data)
    error_code = resp['errorCode']
    if error_code != '0':
        if error_code == '102':
            result = '不支持的语言类型!'
        elif error_code == '103':
            result == '翻译文本过长!'
    result = resp['translation'][0]
    return result


@click.command()
@click.option('--source', default='auto', help="source language")
@click.option('--to', default='auto', help="target language")
@click.argument('q')
def trans_cli(source, to, q):
    click.echo("\033[1;31m*******翻译结果*******\033[0m")
    result = translate(q)
    click.echo(result)


if __name__ == "__main__":
    trans_cli()
