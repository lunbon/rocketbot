import os
import asyncio
import json
import discord
from discord.ext import commands
from functions import get_ranks_by_nikname, save_member_ranks
from discord_functions import add_roles, delete_roles
bot = commands.Bot(command_prefix='!')
#"""
#production setting
token = os.environ.get('TOKEN')
server_id = '417269196850987027'
fileName = 'members.json'
channel = bot.get_channel('417269196850987029')
"""
#develop settiogs
token = os.environ.get('TOKEN')
server_id = '417269196850987027'
fileName = 'members.json'
channel_id = '417269196850987029'
#"""


@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

@bot.command(pass_context=True)
async def reg(ctx,platform:str, nick:str):
	ranks = get_ranks_by_nikname(platform, nick)
	server = ctx.message.server
	if server == None:
		bot.say('Бот работает только на сервере!')
	server_roles = server.roles
	member = ctx.message.author
	result_of_saving=save_member_ranks(member.name
						+'#'+member.discriminator, 
						platform, nick, ranks, fileName)
	if result_of_saving:
		if await add_roles(bot, ranks,member,server_roles):
			await bot.say('Successfully registered!')
	else:
		await bot.say('Ошибка при сохранении!')

async def check_ranks():
	await bot.wait_until_ready()
	server = bot.get_server(server_id)
	while not bot.is_closed:
		channel = bot.get_channel(channel_id)
		with open(fileName,'r') as f:
			players = json.load(f)
		for player in players:
			try:
				new_ranks = get_ranks_by_nikname(
					players[player]['platform'],players[player]['nick'])
			except:
				message = 'Запрос профиля %s не удался'%players[player]['nick']
				await bot.send_message(channel, message)
				continue
			if list(new_ranks) != players[player]['ranks']:
				member = server.get_member_named(player)
				if await delete_roles(bot, players[player]['ranks'], member, server.roles):
					save_member_ranks(member.name+'#'+member.discriminator,
						players[player]['platform'], players[player]['nick'], 
						new_ranks, fileName)
					await add_roles(bot, new_ranks, member, server.roles)
					message = '%s, your ranks have been updated. Your current ranks is %s and %s!'
					await bot.send_message(channel, message%(member.name, *new_ranks))
				else:
					message = 'Что-то пошло не так во время обновления - %s' % member.name
					await bot.send_message(channel, message%(member.name))
				await asyncio.sleep(1)
		await asyncio.sleep(20)
		
bot.loop.create_task(check_ranks())
bot.run(token)