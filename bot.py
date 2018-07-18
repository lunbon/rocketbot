import os, sys
import asyncio
import json
import discord
from discord.ext import commands
from functions import get_ranks_by_nikname, save_member_ranks
from discord_functions import add_roles, delete_roles
import config
import logging

bot = commands.Bot(command_prefix='!')
#"""
#production setting
token = config.token
server_id = config.server_id
fileName = 'members.json'
update_channel_id = config.channel_id
newcomers_channel_id = config.newcomers_channel
newcomers_role = config.newcomers_role
log_chan = config.log
"""
#develop settiogs
token = os.environ.get('TOKEN')
server_id = '417269196850987027'
fileName = 'members.json'
update_channel_id = '417269196850987029'
newcomers_channel_id = '417269196850987029'
newcomers_role = '464414207484493834'
log_chan = '417269196850987029'
#"""


@bot.event
async def on_ready():
	logging.info('Logged in as')
	logging.info(bot.user.name)
	logging.info(bot.user.id)
	logging.info('-'*18)

@bot.event
async def on_member_join(member):
	server = bot.get_server(server_id)
	role = discord.utils.get(server.roles, id=newcomers_role)
	await bot.add_roles(member, role)
	channel=bot.get_channel(newcomers_channel_id)
	message='''
%s добро пожаловать на сервер RL Ranked! Для доступа ко всем каналам необходимо зарегистрироваться. После регистрации бот выдаст вам роли со званиями на сервере, для более простого поиска напарников! Для регистрации вы должны ввести специальную команду на данном канале, используя свой steam id/ps4 nick/xbox nick. Команда выглядит следующим образом: 
!reg steam <steam id> (Для PC игроков)
!reg ps <nick> (Для PS4 игроков) 
!reg xbox <nick> (Для XBOX игроков)
Если возникли проблемы с регистрацией, пожалуйста, обратитесь к администраторам!
	'''%member.name
	await bot.send_message(channel, message)



@bot.command(pass_context=True)
async def reg(ctx,platform:str, nick:str):
	log = bot.get_channel(log_chan)
	ranks = get_ranks_by_nikname(platform, nick)
	if ranks==False:
		await bot.say('404 Error! Check nick and platform!')
		return
	server = ctx.message.server
	try:
		server_roles = server.roles
	except:
		await bot.say('This is a server only bot!')
		return
	member = ctx.message.author
	with open(fileName,'r') as f:
		players = json.load(f)
	name=member.name+'#'+member.discriminator
	if name in players:
		await delete_roles(bot, players[name]['ranks'], member, server.roles,log)
	result_of_saving=save_member_ranks(member.name
						+'#'+member.discriminator, 
						platform, nick, ranks, fileName)
	if result_of_saving:
		if await add_roles(bot, ranks,member,server_roles,log):
				await bot.say('Successfully registered!')
				new_comer_role = discord.utils.get(server.roles, id=newcomers_role)
				await bot.remove_roles(member, new_comer_role)
	else:
		await bot.say('Saving Error')
	



async def check_ranks():
	await bot.wait_until_ready()
	while not bot.is_closed:
		
		server = bot.get_server(server_id)
		channel = bot.get_channel(update_channel_id)
		log = bot.get_channel(log_chan)
		with open(fileName, 'r') as f:
			players = json.load(f)

		for player in players:
			new_ranks = get_ranks_by_nikname(players[player]['platform'],players[player]['nick'])

			if new_ranks==False:
				await bot.send_message(log,'Ошибка при обновлении %s'%(players[player]['nick']))
				continue
			if list(new_ranks) != players[player]['ranks']:
				message = '%s Найдена разница рангов старые ранги - %s и %s. Новые ранги - %s и %s'%(player,players[player]['ranks'][0],
																								players[player]['ranks'][1],
																								new_ranks[0],
																								new_ranks[1])
				await bot.send_message(log, message)
				try:
					member = server.get_member_named(player)
					member.name
				except:
					bot.send_message(log,'Ошибка с участником %s! Возможно он покинул сервер!'%player)
					save_member_ranks(player,
						players[player]['platform'], players[player]['nick'], 
						new_ranks, fileName)
					continue
				if await delete_roles(bot, players[player]['ranks'], member, server.roles, log):
					save_member_ranks(player,
						players[player]['platform'], players[player]['nick'], 
						new_ranks, fileName)
					await add_roles(bot, new_ranks, member, server.roles, log)
					message = '%s, your ranks have been updated. Your current ranks is %s and %s!'
					await bot.send_message(channel, message%(member.mention, *new_ranks))
				else:
					message = 'Что-то пошло не так во время обновления - %s' % member.name
					await bot.send_message(log, message%(member.name))
			await asyncio.sleep(1)
		await asyncio.sleep(3600)

def run_bot():		
	bot.loop.create_task(check_ranks())
	bot.run(token)
