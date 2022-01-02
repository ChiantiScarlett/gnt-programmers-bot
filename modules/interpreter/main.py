
import discord
import os
import re
from .constants import TIER_LIST, TIER_NAME_MAP, TIER_NORMALIZATION_MAP, \
    TIER_NORMALIZATION_MAP_KEYS, WEEKDAY_ENG_TO_INT, WEEKDAY_ENG_TO_KOR
from .functions import load_problemset
import random
import numpy
import ast
from datetime import datetime, date


class Interpreter:
    def __init__(self):
        self.problemset = load_problemset()
        self.action_map = {
            '랜덤': self.command__random,
            '스터디': self.command__study,
            '채점현황': self.command__status,
            '채점': self.command__status,
            '도움말': self.command__help,
            '__default__': self.command__default
        }

    async def command__default(self, ctx, command):
        """
        [Description]
            다른 액션이 실행되지 않을 때, default로 실행할 메소드입니다.
        """
        output_string = '명령어를 잘 이해하지 못했어요. [도움말] 명령어를 통해 사용가능한 커맨드와 그 형식을 '
        output_string += '확인해주세요. :face_with_monocle:'
        await ctx.channel.send(output_string+'\nㅤ')

    async def command__help(self, ctx, command):
        """
        [Description]
            <도움말> 커맨드입니다.
        """

        # 환경변수에서 값을 불러옵니다:
        APP_NAME = os.getenv('APP_NAME')
        APP_VERSION = os.getenv('APP_VERSION')
        STARTS_AT = WEEKDAY_ENG_TO_KOR[os.getenv('STUDY_STARTS_AT')]
        PROBLEMSET_NAME = f"{self.problemset['description']} (v" + \
            f"{self.problemset['version']})"

        # 각 티어 별 문제 개수를 계산합니다:
        PROBLEMSET_COUNT = {'B': 0, 'S': 0,
                            'G': 0, 'P': 0, 'D': 0, 'R': 0, '?': 0}
        for _item in self.problemset['data']:
            PROBLEMSET_COUNT[_item['tier'][0]] += 1

        # 적절한 메시지를 출력합니다:
        output_string = f":gear: {APP_NAME} "
        output_string += f"(v{APP_VERSION}) :gear: \n\n"
        output_string += f"현재 사용중인 문제집은 [{PROBLEMSET_NAME}]이고, "
        output_string += f"총 {sum(PROBLEMSET_COUNT.values())}개의 문제가 담겨 있어요.\n\n"
        output_string += f"- 브론즈 {PROBLEMSET_COUNT['B']}개\n"
        output_string += f"- 실버 {PROBLEMSET_COUNT['S']}개\n"
        output_string += f"- 골드 {PROBLEMSET_COUNT['G']}개\n"
        output_string += f"- 플래티넘 {PROBLEMSET_COUNT['P']}개\n"
        output_string += f"- 다이아 {PROBLEMSET_COUNT['D']}개\n"
        output_string += f"- 루비 {PROBLEMSET_COUNT['R']}개\n"
        output_string += f"- Unrated {PROBLEMSET_COUNT['?']}개\n\n"
        output_string += f"이하의 명령어 형식에 맞게 저를 불러주시면, 백준 문제 번호를 보내드릴게요. \nㅤ"

        embed = discord.Embed(
            title="", description="", color=0x00a8ff)
        embed.add_field(
            name=f":keyboard: 스터디",
            value=f"이번주에 풀어야 할 문제를 출력해요. 매주 {STARTS_AT}마다 문제 리스트가 변경되며, " +
            f"다음주 {STARTS_AT}가 되기 전까지는 \"스터디\" 커맨드를 여러번 실행해도 문제 번호가 " +
            f"바뀌지 않아요.\nㅤ\nㅤ",
            inline=False)
        embed.add_field(
            name=f":keyboard: 랜덤 [티어] [개수]",
            value=f"조건에 맞는 문제를 랜덤으로 출력해요. \"랜덤 실버 2개\", \"랜덤 골3~플레5 3문제\", " +
            f"\"랜덤 브5-플1\" 처럼 사용할 수 있어요. 티어는 solved.ac에 기반하며, " +
            f"Unrated나 Master 티어의 문제는 검색되지 않아요.\nㅤ\nㅤ",
            inline=False)
        embed.add_field(
            name=f":keyboard: 도움말",
            value=f"지금 보고 계시는 것처럼 도움말을 출력해요. :raised_hands:'\nㅤ\nㅤ",
            inline=False)

        await ctx.channel.send(output_string+'\nㅤ', embed=embed)

    async def command__status(self, ctx, command):
        """
        [Description]
            <채점현황> 커맨드에 관한 메소드입니다.
        """
        ...

    async def command__study(self, ctx, command):
        """
        [Description]
            <스터디> 커맨드에 관한 메소드입니다.
            환경변수에 명시된 스터디 관련 설정을 토대로,적절한 문제를 선별하여 그 결과를
            메시지로 출력합니다.
        """
        # 적절한 시드를 생성합니다.
        weeknumber, weekday = map(
            int, datetime.now().strftime("%V %u").split())
        study_seed = int(os.getenv('STUDY_SEED'))
        seed = study_seed * (weeknumber * 10 - 6 + weekday) // 10
        random_state = numpy.random.RandomState(seed)

        # 환경변수에 적힌 문제 리스트를 가져옵니다.
        study_tier_list = os.getenv('STUDY_TIERS')
        study_tier_list = re.sub('\s', '', study_tier_list)
        study_tier_list = ast.literal_eval(study_tier_list)

        # 시드와 문제 범위를 토대로, 적절하게 문제를 추출합니다.
        problem_list = []
        for item in study_tier_list:
            problem_list += list(random_state.choice(
                list(filter(lambda k: k['tier'] in item[0],
                            self.problemset['data'])), int(item[1])))

        # 문제를 ID 오름차순 정렬합니다.
        problem_list.sort(key=lambda k: int(k['id']))

        # "N월 M주차"를 도출합니다:
        cursor = 1 - date(datetime.now().year,
                          datetime.now().month, 1).weekday()
        week_count = 0
        today = datetime.now()

        while cursor < today.day:
            week_count += 1
            cursor += 7

        # 제목과 문제를 출력합니다:
        output_string = f'{today.year}년 {today.month}월 {week_count}주차 스터디 문제입니다.\nㅤ'
        embed = discord.Embed(
            title="", description="", color=0x00ff56)
        for index, problem in enumerate(problem_list):
            embed.add_field(
                name=f"[{problem['id']}번]",
                value=f"[{problem['title']}](https://boj.kr/{problem['id']})" +
                ('\nㅤ' if index != len(problem_list) - 1 else ''), inline=False)

        await ctx.channel.send(output_string, embed=embed)

    async def command__random(self, ctx, command):
        """
        [Description]
            <랜덤> 커맨드에 대한 메소드입니다.
            e.g. 랜덤 브3 ~ 골2 3문제

            특정 범위 및 수량에 대해, 주어진 문제집에서 랜덤으로 설정하여 추출합니다.
        """
        # 1. 해당 조건에 맞는 티어 및 개수를 저장할 변수를 선언합니다:
        tier_list = []
        count = 1

        # 2. 정규식을 이용해 필요한 데이터를 추출하고 불필요한 문자를 제거합니다:
        # 2-1. 정규식으로 문제 개수를 추론 및 저장:
        count = re.findall(r'[0-9]{1,100}문제|[0-9]{1,100}개', command)
        count = int(re.sub(r'문제|개', '', count[0])) if count else 1

        # 2-2. 불필요한 단어 제거:
        command = re.sub(r'[0-9]{0,100}문제|[0-9]{0,100}개', '', command)
        command = re.sub(r'랜덤', '', command)
        command = re.sub(r'\s', '', command).lower()

        # 2-3. 티어 범위 추론을 위한 정규식:
        begin_tier, end_tier = None, None
        if re.match(r"[\S]+[-]+[\S]", command):
            begin_tier, end_tier = command.split('-')
        elif re.match(r"[\S]+[~]+[\S]", command):
            begin_tier, end_tier = command.split('~')
        elif re.match('[\S]', command):
            begin_tier = command
            end_tier = command

        # 3. 데이터가 존재하지 않을 경우, None을 저장합니다.
        if not begin_tier or not end_tier:
            tier_list = None
        else:
            # 각각의 티어 키워드를 일반화합니다.(B, S, G 등)
            for keyword in TIER_NORMALIZATION_MAP_KEYS:
                begin_tier = begin_tier.replace(
                    keyword, TIER_NORMALIZATION_MAP.get(keyword))
                end_tier = end_tier.replace(
                    keyword, TIER_NORMALIZATION_MAP.get(keyword))

            # 각 티어의 레벨이 주어지지 않았을 경우, 범위에 걸맞게 레벨을 부여합니다.
            if not re.match(r"[\S]+[1-5]", begin_tier):
                begin_tier = begin_tier+'5'
            if not re.match(r"[\S]+[1-5]", end_tier):
                end_tier = end_tier+'1'

            # 이렇게 해서 생겨난 begin_tier와 end_tier가 부적절할 경우, None을 저장합니다.
            if begin_tier not in TIER_LIST or end_tier not in TIER_LIST:
                tier_list = None

            # 그 외의 경우 (즉 정상작동의 경우) 해당 티어 리스트를 저장합니다.
            else:
                tier_list = TIER_LIST[TIER_LIST.index(
                    begin_tier):TIER_LIST.index(end_tier)+1]

        # 4. tier_list가 None일 경우, 에러 메시지를 출력하고 메소드를 종료합니다.
        if tier_list is None:
            return await ctx.channel.send(
                '명령을 잘 이해하지 못했어요 :cry:   도움말을 읽고 형식에 맞게 요청해주세요.'
            )

        # 5. 해당 범위 내에 있는 문제를 가져옵니다.
        problem_list = list(filter(lambda k: k['tier']
                                   in tier_list, self.problemset['data']))

        # 6. 문제를 뽑고, 그에 적절한 데이터를 출력합니다.

        # 6-1. 입력받은 개수만큼 뽑되, 만약 개수 미달일 경우 가능한만큼만 뽑습니다.
        try:
            samples = random.sample(problem_list, count)
        except ValueError:
            samples = random.sample(problem_list, len(problem_list))

        # 6-2. 해당되는 문제가 존재하지 않을 경우:
        output_string = ''
        if not len(samples):
            if len(tier_list) == 1:
                output_string += f'{TIER_NAME_MAP[tier_list[0]]}'
            else:
                output_string += f'{TIER_NAME_MAP[tier_list[0]]}부터 '
                output_string += f'{TIER_NAME_MAP[tier_list[-1]]}까지의 범위'
            output_string += f'에 해당하는 문제를 못찾았어요. :cry:'
            embed = None
        else:
            # 6-3. 단일 티어 범위일 경우:
            if len(tier_list) == 1:
                output_string += f'{TIER_NAME_MAP[tier_list[0]]} 문제를 '
            # 6-4. 복수의 티어 범위일 경우:
            else:
                output_string += f'{TIER_NAME_MAP[tier_list[0]]}부터 '
                output_string += f'{TIER_NAME_MAP[tier_list[-1]]}까지의 '
                output_string += f'범위에서 '

            # 6-5. 문제 개수가 하나일 때:
            if len(samples) == 1:
                output_string += '랜덤으로 하나 뽑아봤어요.'
            # 6-6. 문제 개수가 여러개일 때:
            else:
                output_string += f'{len(samples)}개 뽑아봤어요.'
            # 6-7. 개수 미달일 경우를 표시:
            if len(samples) < count:
                output_string += ' (개수 미달)'

            # 6-8. 선별된 문제를 적절한 형식으로 출력합니다:
            embed = discord.Embed(
                title="", description="", color=0x00ff56)
            for index, sample in enumerate(samples):
                embed.add_field(
                    name=f"[{sample['id']}번]",
                    value=f"[{sample['title']}](https://boj.kr/{sample['id']})" +
                    ('\nㅤ' if index != len(samples) - 1 else ''), inline=False)

        await ctx.channel.send(output_string+'\nㅤ', embed=embed)
