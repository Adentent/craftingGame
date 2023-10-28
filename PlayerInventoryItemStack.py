class PlayerInventoryItemStack:
    from Item import Item
    from Recipe import Recipe

    def __init__(self) -> None:
        self.stack = {}

    def getItem(self, item: Item, number: int):
        if item not in self.stack.keys():
            self.stack[item] = 0
        self.stack[item] += number
        return 0

    def loseItem(self, item: Item, number: int):
        if self.stack[item] < number:
            return 1
        self.stack[item] += number
        return 0

    def craftItem(self, recipe: Recipe):
        inventoryBackup = self.stack
        inputs = recipe.input
        for i in inputs:
            if self.loseItem(i, 1):  # If the player doesn't own enough items, then return all the items.
                self.stack = inventoryBackup
                return 1
        outputs = recipe.output
        for i in outputs:
            self.getItem(i, 1)
        return 0

    def formatOutput(self):
        if not self.stack:
            return "空空如也..."
        return str(", ".join([f"{i.name}({self.stack[i]})" for i in self.stack]))
