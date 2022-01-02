import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

from numpy.random.mtrand import poisson, rand, random_sample
from .constants import TIER_NAME_MAP
from .functions import command_interpreter, load_problemset
import random
import numpy
import ast
from datetime import datetime
from .interpreter import Interpreter


class Bot(commands.Bot, Interpreter):
    """
    디스코드 봇.
    """

    def __init__(self, *args, **kwargs):
        # 환경 변수를 불러옵니다:
        load_dotenv()

        # commands.Bot의 생성자 인자인 command_prefix를 ""로 설정하고, 상위 생성자를 호출합니다.
        kwargs['command_prefix'] = ""
        commands.Bot.__init__(self, *args, **kwargs)
        Interpreter.__init__(self)

    def run(self):
        """
        [Description]
            봇을 실행합니다.
        """
        super().run(os.getenv('DISCORD_BOT_TOKEN'))

    async def on_ready(self):
        """
        [Description]
            봇이 준비되었을 때 실행될 메소드입니다.
        """
        print('루비 온라인!')

    async def on_message(self, ctx):
        """
        [Description]
            채널에서 대화가 오갈 때 처리할 이벤트 핸들러입니다.
            public 채널의 대화에서는 해당 봇을 맨션해야만 실행됩니다.
        """

        # 봇(자기 자신 포함)이 메시지를 보냈을 경우 무시합니다:
        if ctx.author.bot is True:
            return
        # 채널이 public인 경우, 봇을 맨션하지 않았다면 무시합니다:
        if ctx.channel.type == discord.ChannelType.text:
            if not self.user.mentioned_in(ctx):
                return
        # 봇에게 날아온 DM일 경우, 무조건 허용합니다:
        elif ctx.channel.type == discord.ChannelType.private:
            pass
        # 그 외의 경우에는 무시합니다:
        else:
            return

        # 멘션 태그를 전부 제거합니다.
        command = re.sub(re.escape("<@")+"[\S]+?"+re.escape(">"),
                         "", ctx.content).strip()

        # 주어진 커맨드에 상응하는 액션을 실행합니다. 만약 해당 액션이 존재하지 않을 경우, default 액션을 실행합니다.
        action = command.split()[0]
        if action in self.action_map.keys():
            await self.action_map[action](ctx, command=command)
        else:
            await self.action_map['__default__'](ctx, command=command)

    async def _command_study(self, ctx, command):
        """

        """
        study_tier_list = os.getenv('STUDY_TIERS')
        study_tier_list = re.sub('\s', '', study_tier_list)
        study_tier_list = ast.literal_eval(study_tier_list)

        problem_list = []

        weeknumber, weekday = map(int, datetime.now().strftime("%V %u"))
        study_seed = int(os.getenv('STUDY_SEED'))
        seed = study_seed * (weeknumber * 10 - 6 + weekday) // 10

        datetime.now().strftime("%Y%m%d")
        random_state = numpy.random.RandomState(seed)
        for item in study_tier_list:
            problem_list += list(random_state.choice(
                list(filter(lambda k: k['tier'] in item[0],
                            self.problemset['data'])), int(item[1])))

        problem_list.sort(key=lambda k: k['id'])

        # for index, sample in enumerate(problem):
        #     embed.add_field(
        #         name=f"[{sample['id']}번]",
        #         value=f"[{sample['title']}](https://boj.kr/{sample['id']})" +
        #         ('\nㅤ' if index != len(samples) - 1 else ''), inline=False)

    async def _command__random(self, ctx, command):
        """
        [Description]
            Pick random problems based on the input command, and send messages
            accordingly.

        """

        command_result = command_interpreter(command=command)
        if command_result is None:
            return await ctx.channel.send(
                '명령을 잘 이해하지 못했어요 :cry:   도움말을 읽고 형식에 맞게 요청해주세요.'
            )

        problem_list = list(filter(lambda k: k['tier']
                                   in command_result[0], self.problemset['data']))

        try:
            samples = random.sample(problem_list, command_result[1])
        except ValueError:
            samples = random.sample(problem_list, len(problem_list))

        output_string = ''
        if not len(samples):
            output_string += f'{TIER_NAME_MAP[command_result[0][0]]}부터 '
            output_string += f'{TIER_NAME_MAP[command_result[0][-1]]}까지의 '
            output_string += f'범위에 해당되는 문제를 못찾았어요. :cry:'

        else:
            if len(command_result[0]) == 1:
                output_string += f'{TIER_NAME_MAP[command_result[0][0]]} 문제를 '
            else:
                output_string += f'{TIER_NAME_MAP[command_result[0][0]]}부터 '
                output_string += f'{TIER_NAME_MAP[command_result[0][-1]]}까지의 '
                output_string += f'범위에서 '

            if len(samples) == 1:
                output_string += '랜덤으로 하나 뽑아봤어요.'
            else:
                output_string += f'{len(samples)}개 뽑아봤어요.'

            if len(samples) < command_result[1]:
                output_string += ' (개수 미달)'

            embed = discord.Embed(
                title="", description="", color=0x00ff56)

            for index, sample in enumerate(samples):
                embed.add_field(
                    name=f"[{sample['id']}번]",
                    value=f"[{sample['title']}](https://boj.kr/{sample['id']})" +
                    ('\nㅤ' if index != len(samples) - 1 else ''), inline=False)

        await ctx.channel.send(output_string)
        await ctx.channel.send(embed=embed)
