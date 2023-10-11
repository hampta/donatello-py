from donatello import Donatello
from donatello.models import Donate, User

client = Donatello("YOUR_API_KEY", "YOUR_WIDGET_ID")

@client.on_ready
def on_start(user: User):
    print(f"Started with user {user.nickname}")
    print(f"Donates Amount: {user.donates.total_amount}")
    print(f"Donates count: {user.donates.total_count}")

@client.on_donate
def on_donate(donate: Donate):
    print(donate)

client.start()