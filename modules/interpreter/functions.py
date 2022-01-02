from urllib.request import urlopen
import json
import os


def load_problemset():
    """
    환경변수에 쓰여있는 URL 또는 경로의 JSON 파일을 불러옵니다.
    """
    try:
        env_path = os.getenv('PROBLEMSET_JSON')
        # URL 포맷이면 urlopen을, 파일일 경우 open 함수를 사용하여 불러옵니다.
        if str(env_path).startswith('http'):
            data = json.loads(urlopen(env_path).read())
        else:
            with open(env_path) as fp:
                data = json.load(fp)
    except:
        print("[*] JSON 파일 형식 또는 경로가 잘못되었어요!")
        exit()

    return data
