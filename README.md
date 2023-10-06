# 💸 Donatello-py

[![Upload Python Package](https://github.com/hampta/donatello-py/actions/workflows/python-publish.yml/badge.svg)](https://github.com/hampta/donatello-py/actions/workflows/python-publish.yml)
[![PyPi Version](https://img.shields.io/pypi/v/donatello-py.svg)](https://pypi.org/project/donatello-py/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/donatello-py.svg)](https://pypi.org/project/donatello-py/)
[![PyPi License](https://img.shields.io/pypi/l/donatello-py.svg)](https://pypi.org/project/donatello-py/)

Simple python wrapper for the Donatello API.

##  Features

- Full type hints
- Client info
- Get donates
- Get clients
- Long polling
- Add Async support
## Installation

```bash 
pip install donatello-py
```

For speedup: 
```bash
pip install donatello-py[speed]
```

## Basic Usage

Get and activate your API key [here](https://donatello.to/panel/doc-api).

#### Sync 

```python
from donatello import Donatello

client = Donatello("YOUR_API_KEY")

# Get client info
print(client.get_me())

# Get donates
print(client.get_donates(page=1, per_page=10))

# Get clients
print(client.get_clients())
```

#### Async

```python
from donatello import AsyncDonatello

client = AsyncDonatello("YOUR_API_KEY")

async def main():
    print(await client.get_me())
    print(await client.get_donates(page=1, per_page=10))
    print(await client.get_clients())

asyncio.run(main())
```

## Long polling

For use long polling you need to create widget [here](https://donatello.to/panel/alert-widget) and get widget id from url.

### Example url:

```
https://donatello.to/widget/<WIDGET_ID>/token/<YOUR_API_KEY>
```

### Code example

#### Sync

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

#### Async

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
## Examples

You can find more examples [here](https://github.com/hampta/donatello-py/tree/main/examples).


## License
[MIT](https://choosealicense.com/licenses/mit/)


## TODO

- [x] Add more examples
- [x] Add docs
- [ ] Add tests
- [ ] Goal, Top, interactive widgets?


## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.