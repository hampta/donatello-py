class EventHandler:
    """An event handler for functions"""
    def __init__(self):
        """Initialise a list of listeners"""
        self.__listeners = []
    
    def add_listener(self, listener):
        """Add a listener to the list"""
        self.__listeners.append(listener)

    def handle_event(self, event_data):
        """Call all listeners"""
        for listener in self.__listeners:
            listener(event_data)
    
    def remove_listener(self, listener):
        """Remove a listener from the list"""
        self.__listeners.remove(listener)


class AsyncEventHandler:
    """An event handler for async functions"""
    def __init__(self):
        """Initialise a list of listeners"""
        self.__listeners = []

    def add_listener(self, listener: callable):
        """Add a listener to the list"""
        self.listeners.append(listener)

    async def handle_event(self, event_data: dict):
        """Call all listeners"""
        for listener in self.listeners:
            await listener(event_data)

    def remove_listener(self, listener: callable):
        """Remove a listener from the list"""
        self.listeners.remove(listener)