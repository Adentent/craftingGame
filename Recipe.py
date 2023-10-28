class Recipe:
    from Item import Item

    def __init__(self, input: list[Item], mid: str, output: list[Item]):
        self.input = input
        self.mid = mid
        self.output = output
