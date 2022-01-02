# gnt-programmers-bot
GNT 알고리즘 스터디에 사용할 백준 랜덤 문제 선정용 디스코드 봇입니다.

## 1. Install required packages

이 프로그램은 discord, bs4, dotenv, numpy에 의존합니다. 이하의 커맨드를 통해 앱 실행에 필요한 모듈을 설치해주세요.
```
> pip3 install -r requirements.txt
```


## 2. Add .env file

`.env` 파일을 생성한 후, 이하의 양식에 맞게 작성해주세요.

```
APP_NAME=루비 # 봇 이름
APP_VERSION=1.0.0 # 봇 버전

DISCORD_BOT_TOKEN=SOME_DISCORD_TOKEN # 디스코드에서 발급받은 토큰
CHANNEL_ID=SOME_CHANNEL_ID # 디스코드 채널 ID

HEADERS__COOKIE = SOME_HEADER_COOKIE # 백준 사이트의 쿠키
PROBLEMSET_JSON = 'https://raw.githubusercontent.com/ChiantiScarlett/gnt-programmers-bot/develop/dataset/problemset-001.json' # JSON URL 또는 로컬 파일 경로


# 스터디 커맨드를 위한 변수 #
STUDY_SEED = 1000 # 랜덤 정수
STUDY_STARTS_AT = SATURDAY # 스터디를 시작하는 요일 (해당 요일 기준으로 문제집이 변경됨)
STUDY_TIERS= '[
    [["B5","B4","B3","B2","B1","S5","S4","S3","S2","S1"], 2],
    [["G5","G4"], 1]
    ]'
# --> [[티어 범위, 문제개수], ..., [티어 범위, 문제 개수]] 형식.
```


## 3. Run main.py

main.py를 실행합니다.

```
> python3 main.py
```