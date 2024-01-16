#pyrotel

<h3 align="center">tele-py is a library for telegram bots.</h3>

> ## Install and Update:
```python
pip install pyrotel
```

> ## START:
```python
from pyrotel import Client, Message

bot = Client("TOKEN")

last_update = 0

while True:
	update = bot.get_last_update()
	if update != last_update:
		msg = Message(update)
		if msg.text() == "/start":
			bot.send_message(msg.chat_id(), "wellcome to my bot.")
```

> ## Social Media:
<a href="https://t.me/pyrotel">TELEGRAM</a><br>
<a href="https://github.com/Erfan-Bafandeh/pyrotel">GITHUB</a>
