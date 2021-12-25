from dotenv import load_dotenv
import re
from .constants import TIER_LIST, NORMALIZATION_MAP, NORMALIZATION_MAP_KEYS
from urllib.request import urlopen
import json
import os


def load_problemset():
    load_dotenv()
    raw_data = urlopen(os.getenv('PROBLEMSET_URL')).read()

    return json.loads(raw_data)


def command_interpreter(command):
    # find problem quantity:
    count = re.findall(r'[0-9]{1,100}문제|[0-9]{1,100}개', command)
    count = int(re.sub(r'문제|개', '', count[0])) if count else 1

    # remove unnecessary keywords:
    command = re.sub(r'[0-9]{0,100}문제|[0-9]{0,100}개', '', command)
    command = re.sub(r'랜덤|선택|선택해|선택해줘|선택해줄래|!|[?]', '', command)
    command = re.sub(r'골라줄래|골라줘|골라|,|뽑아줘|뽑아줄래|뽑아|알려줘|알려줄래', '', command)
    command = re.sub(r'\s', '', command).lower()

    # infer the tier types from the remaining context:
    begin_tier, end_tier = None, None
    if re.match(r"[\S]+[-]+[\S]", command):
        begin_tier, end_tier = command.split('-')
    elif re.match(r"[\S]+[~]+[\S]", command):
        begin_tier, end_tier = command.split('~')
    elif re.match('[\S]', command):
        begin_tier = command
        end_tier = command

    # if data is empty, halt:
    if not begin_tier or not end_tier:
        return None

    # normalize each keyword:
    for keyword in NORMALIZATION_MAP_KEYS:
        begin_tier = begin_tier.replace(
            keyword, NORMALIZATION_MAP.get(keyword))
        end_tier = end_tier.replace(keyword, NORMALIZATION_MAP.get(keyword))

    # specify level if not given:
    if not re.match(r"[\S]+[1-5]", begin_tier):
        begin_tier = begin_tier+'5'
    if not re.match(r"[\S]+[1-5]", end_tier):
        end_tier = end_tier+'1'

    # if the outcome is invalid, return None.
    if begin_tier not in TIER_LIST or end_tier not in TIER_LIST:
        return None

    # otherwise, return range tiers & lexical quantity of the problemset:
    return (TIER_LIST[TIER_LIST.index(begin_tier):TIER_LIST.index(end_tier)+1], count)
