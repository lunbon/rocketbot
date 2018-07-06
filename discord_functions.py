"""
This functions use discord api and may be context dependent
"""
import asyncio
async def add_roles(bot,ranks, member, server_roles, log):
	for role in server_roles:
		if role.name in ranks:
			try:
				await asyncio.sleep(1)
				await bot.add_roles(member, role)
			except:
				error_message = f'Ошибка при добавлении ролей юзеру {member.name}'
				error_message += f'роль с ошибкой - {role.name}'
				await bot.send_message(log,error_message)
				return False
	return True

async def delete_roles(bot,ranks, member, server_roles, log):
	for role in server_roles:
		if role.name in ranks:
			try:
				await asyncio.sleep(1)
				await bot.remove_roles(member, role)
			except:
				error_message = f'Ошибка при удалении ролей юзера {member.name}!'
				error_message += f'роль с ошибкой - {role.name}'
				await bot.send_message(log_chan,error_message)
				return False
	return True
