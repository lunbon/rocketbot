"""
This functions use discord api and may be context dependent
"""
import asyncio
async def add_roles(bot,ranks, member, server_roles):
	for role in server_roles:
		if role.name in ranks:
			try:
				await asyncio.sleep(1)
				await bot.add_roles(member, role)
			except:
				error_message = f'Ошибка 403, роль {role.name} выше любой из ролей бота!'\
								+f' Поставьте роль бота выше {role.name}.'
				await bot.say(error_message)
				return False
	return True

async def delete_roles(bot,ranks, member, server_roles):
	for role in server_roles:
		if role.name in ranks:
			try:
				await asyncio.sleep(1)
				await bot.remove_roles(member, role)
			except:
				error_message = f'Ошибка 403, роль {role.name} выше любой из ролей бота!'\
								+f' Поставьте роль бота выше {role.name}.'
				await bot.say(error_message)
				return False
	return True