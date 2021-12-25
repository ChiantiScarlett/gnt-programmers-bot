import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re
from .constants import TIER_NAME_MAP
from .functions import command_interpreter, load_problemset
import random


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        kwargs['command_prefix'] = ""
        load_dotenv()
        self.load_problemset()
        super().__init__(*args, **kwargs)

    def load_problemset(self):
        self.problemset = load_problemset()

    def run(self):
        super().run(os.getenv('DISCORD_BOT_TOKEN'))

    async def on_ready(self):
        print('루비 온라인!')

    async def on_message(self, ctx):
        """
        [Description]
            <Message Handler>
        """

        # ff the channel is not private, you need to mention the bot.
        if ctx.channel.type == discord.ChannelType.text:
            if not self.user.mentioned_in(ctx):
                return
        elif ctx.channel.type == discord.ChannelType.private:
            pass
        else:
            return

        # remove all mention tag.
        command = re.sub(
            re.escape("<@")+"[\S]+?"+re.escape(">"), "", ctx.content).strip()

        # [랜덤] command execution:
        if command.startswith('랜덤'):
            await self._command__random(ctx, command=command)

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
