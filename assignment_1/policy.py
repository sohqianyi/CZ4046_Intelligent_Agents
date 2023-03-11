class Policy:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, direction):
        self.direction = direction

        if direction == 0:
            self.symbol = "^"
        elif direction == 1:
            self.symbol = "v"
        elif direction == 2:
            self.symbol = "<"
        elif direction == 3:
            self.symbol = ">"

    def get_symbol(self):
        return self.symbol

    def get_direction(self):
        return self.direction
