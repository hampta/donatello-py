<div align="center">
<img src=https://raw.githubusercontent.com/hampta/donatello-py/main/assets/logo.png alt="Donatello-py logo" />
<br>
<a href="https://donatello.to/hampta"><img  src="https://img.shields.io/badge/donatello.to-donate-blue?style=for-the-badge" /></a>
<a href="https://pypi.org/project/donatello-py/"> <img   src="https://img.shields.io/pypi/v/donatello-py?style=for-the-badge" alt="PyPi Version" /> </a>
<a href="https://pypi.org/project/donatello-py/"> <img src="https://img.shields.io/pypi/pyversions/donatello-py?style=for-the-badge" alt="PyPi Python versions" /> </a>
<br>
<a href="https://donatello-py.readthedocs.io/en/latest/"> <img   src="https://img.shields.io/readthedocs/donatello-py?style=for-the-badge" alt="Read the Docs" /> </a>
<a href="https://pypi.org/project/donatello-py/"> <img   src="https://img.shields.io/pypi/dm/donatello-py?style=for-the-badge" alt="PyPi Downloads" /> </a>
<a href="https://pypi.org/project/donatello-py/"> <img   src="https://img.shields.io/pypi/l/donatello-py?style=for-the-badge" alt="PyPi License" /> </a>
<h3>🐍 Python wrapper for the Donatello API.</h3>
</div>

## ✨ Features

- Full type hints
- Client info
- Get donates
- Get clients
- Long polling
- Async support

## 🔗 Installation

```bash 
pip install donatello-py
```

For speedup: 
```bash
pip install donatello-py[speed]
```

## 🧑‍🏭 Basic Usage

Get and activate your API key [here](https://donatello.to/panel/doc-api).

#### ⛓️ Sync 

```python
from donatello import Donatello

client = Donatello("YOUR_API_KEY")

# Get client info
print(client.get_me())

# Get donates
print(client.get_donates(page=0, per_page=00))

# Get clients
print(client.get_clients())
```

#### ⛓️ Async

```python
from donatello import AsyncDonatello

client = AsyncDonatello("YOUR_API_KEY")

async def main():
    print(await client.get_me())
    print(await client.get_donates(page=0, per_page=00))
    print(await client.get_clients())

asyncio.run(main())
```

## 🥏 Long polling

For use long polling you need to create widget [here](https://donatello.to/panel/alert-widget) and get widget id from url.

### Example url:

```
https://donatello.to/widget/<WIDGET_ID>/token/<YOUR_API_KEY>
```

### Code example

#### ⛓️ Sync

```python
from donatello import Donatello
from donatello.models import Donate, User

client = Donatello("YOUR_API_KEY", "WIDGET_ID")

@client.on_ready
def start(user: User):
    print(f"Started with user {user.nickname}")
    print(f"Donates Amount: {user.donates.total_amount}")
    print(f"Donates count: {user.donates.total_count}")

@client.on_donate
def donate(donate: Donate):
    print(donate)

client.start()
```

#### ⛓️ Async

```python
from donatello import AsyncDonatello
from donatello.models import Donate, User

client = AsyncDonatello("YOUR_API_KEY", "WIDGET_ID")

@client.on_donate
async def donate(donate):
    print(f"Donator: {donate.nickname}")
    print(f"Amount: {donate.amount} {donate.currency} / {donate.goal_amount} {donate.goal_currency}")
    print(f"Message: {donate.message}")

@client.on_ready
async def ready(user):
    print(user)
    
client.start()
```
## 📚 Docs

You can find docs [here](https://donatello-py.readthedocs.io/en/latest/).

## 📝 Examples

You can find more examples [here](https://github.com/hampta/donatello-py/tree/main/examples).


## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)


## 📋 TODO

- [x] Add more examples
- [x] Add docs
- [ ] Add tests
- [ ] Websocket based long polling

- [ ] ~~Goal, Top, interactive widgets?~~ Never


## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.