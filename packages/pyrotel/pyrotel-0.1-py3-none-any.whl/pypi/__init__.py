# REQUESTS
from requests import post
from requests import get
# SYS
from sys import exit
# COLORAMA
from colorama import  Fore
# START MESSAGE
print("""
Wellcome to pyrotel library.

pyrotel library version: 0.1

pyrotel is a library for telegram api bots.
""")

# DEF
def ifa(update):
	update = f'{update}'
	upc = update.count("callback")
	if upc == 0:
		return True
	elif upc != 0:
		return False

# BOT CLASS FOR GET YOUR BOT TOKEN
class Bot:
	# GET TOKEN
	def __init__(self, token:str):
		a = get(f"https://api.telegram.org/bot{token}/deleteWebhook")
		a = a.json()
		a = a["ok"]
		if a == False:
			print(f"\n{Fore.LIGHTRED_EX}Token Not Found.{Fore.RESET}")
			exit()
		elif a == True:
			self.token = token
		else:
			print(f"\n{Fore.LIGHTRED_EX}ERROR ! ! !{Fore.RESET}")
	# UPDATE
	# GET UPDATES
	def get_updates(self):
		a = get(f"https://api.telegram.org/bot{self.token}/getupdates")
		a = a.json()
		return a
	# GET LAST UPDATE
	def get_last_update(self):
		a = get(f"https://api.telegram.org/bot{self.token}/getupdates")
		a = a.json()
		a = a["result"]
		a = a[-1]
		return a
	# MESSAGE
	# SEND MESSAGE
	def send_message(self, chat_id:int, text:str):
		a = get(f"https://api.telegram.org/bot{self.token}/sendmessage?chat_id={chat_id}&text={text}")
		a = a.json()
		return a
	# SEND ALL
	def send_all(self, text:str):
		a = get(f"https://api.telegram.org/bot{self.token}/getupdates")
		a = a.json()
		a = a['result']
		ac = len(a)
		ac -= 1
		b = 0
		ab = -1
		e = []
		while ac != ab:
			update = a[b]
			update1 = f'{update}'
			update1 = update1.count('message')
			if update1 == 2:
				id = update['message']['from']['id']
				ab += 1
				b += 1
				ec = e.count(id)
				if ec == 0:
					e.append(id)
			elif update1 == 3:
				b += 1
				ab += 1
		idc = len(e) - 1
		ida = -1
		while idc != ida:
			ida += 1
			idd = e[ida]
			get(f"https://api.telegram.org/bot{self.token}/sendmessage?chat_id={idd}&text={text}")
	# INLINE KEYBOARD
	def inline_keyboard(self, chat_id:int, text:str, keys:list):
		a = post(url=f'https://api.telegram.org/bot{self.token}/sendMessage', json={"chat_id":chat_id, "text":text, "reply_markup": {"inline_keyboard": [keys]} })
		a = a.json()
		return a

	# EDIT MESSAGE
	def edit_message(self, chat_id:int, message_id:int, text:str):
		a = get(f"https://api.telegram.org/bot{self.token}/editmessagetext?chat_id={chat_id}&message_id={message_id}&text={text}")
		a = a.json()
		return a
	# DELETE MESSAGE
	def delete_message(self, chat_id:int, message_id:int):
		a = get(f"https://api.telegram.org/bot{self.token}/deletemessage?chat_id={chat_id}&message_id={message_id}")
		a = a.json()
		return a
	# USERS
	# GET ME
	def getme(self):
		a = get(f"https://api.telegram.org/bot{self.token}/getme")
		a = a.json()
		return a
	# GET ALL USERS
	def get_all_users(self):
		a = get(f"https://api.telegram.org/bot{self.token}/getupdates")
		a = a.json()
		a = a['result']
		ac = len(a)
		ac -= 1
		b = 0
		ab = -1
		e = []
		while ac != ab:
			update = a[b]
			update1 = f'{update}'
			update1 = update1.count('message')
			if update1 == 2:
				id = update['message']['from']['id']
				ab += 1
				b += 1
				ec = e.count(id)
				if ec == 0:
					e.append(id)
			elif update1 == 3:
				b += 1
				ab += 1
		return e
	# GET CHAT
	def get_chat(self, chat_id:int):
		a = get(f"https://api.telegram.org/bot{self.token}/getchat?chat_id={chat_id}")
		a = a.json()
		return a
# MESSAGE CLASS FOR IMPORT DATA WITH UPDATES
class Message:
	# GET UPDATE FOR IMPORT
	def __init__(self, update):
		self.update = update
	# TEXT
	def text(self):
		a = ifa(self.update)
		if a == True:
			a = self.update["message"]["text"]
			return a
		elif a == False:
			a = self.update["callback_query"]["data"]
			return a
	def message_id(self):
		a = ifa(self.update)
		if a == True:
			a = self.update["message"]["message_id"]
			return a
		elif a == False:
			a = self.update["callback_query"]["message"]["message_id"]
			return a
	def chat_id(self):
		a = ifa(self.update)
		if a == True:
			a = self.update["message"]["chat"]["id"]
			return a
		elif a == False:
			a = self.update["callback_query"]["from"]["id"]
			return a
	def first_name(self):
		a = ifa(self.update)
		if a == True:
			a = self.update["message"]["chat"]["first_name"]
			return a
		elif a == False:
			a = self.update["callback_query"]["from"]["first_name"]
			return a