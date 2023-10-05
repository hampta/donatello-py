from donatello import Donatello

client = Donatello("YOUR_API_KEY")

# Get client info
print(client.get_me())

# Get donates
print(client.get_donates(page=1, per_page=10))

# Get clients
print(client.get_clients())