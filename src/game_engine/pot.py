class Pot: 
    """
    Pot class to manage the pot in a poker game.
    this is seperate from a value so that there can multiple pots (side pots)
    in future
    """
    def __init__(self):
        self.value = 0
    
    def add_to_pot(self, amount):
        self.value += amount