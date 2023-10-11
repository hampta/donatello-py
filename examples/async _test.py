from donatello.async_client import AsyncDonatello

client = AsyncDonatello("YOUR_API_KEY", "YOUR_WIDGET_ID")

@client.on_donate
async def donate(donate):
    print(donate)

@client.on_ready
async def ready(user):
    print(user)

client.start()