from donatello import Donatello
from donatello.models import Donate, User

client = Donatello("b29fec0e6fd45df05f9645946b80f538", "651de593663c4d142ea2ad77")

@client.on_ready
def on_start(user: User):
    print(f"Started with user {user.nickname}")
    print(f"Donates Amount: {user.donates.total_amount}")
    print(f"Donates count: {user.donates.total_count}")

@client.on_donate
def on_donate(donate: Donate):
    print(donate)

client.start()