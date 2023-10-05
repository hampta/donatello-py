from donatello.async_client import AsyncDonatello

client = AsyncDonatello("b29fec0e6fd45df05f9645946b80f538", "651de593663c4d142ea2ad77")

@client.on_donate
async def donate(donate):
    print(donate)

@client.on_ready
async def ready(user):
    print(user)

client.start()