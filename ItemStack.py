class ItemStack:
    def __init__(self) -> None:
        self.stack = []

    def addItem(self, name: str):
        from Item import Item
        item = Item(name, len(self.stack) + 1)
        self.stack.append(item)

    def addItems(self, names: list):
        items = []
        for i in names:
            if i[-1] == "\n":
                i = i[:-1]
            items.append(self.addItem(i))

    def findItem(self, name: str):
        for i in self.stack:
            if i.name == name:
                return i
        return self.stack[0]

    def findItems(self, names: list[str]):
        res = []
        for i in names:
            for j in self.stack:
                if j.name == i:
                    res.append(j)
        return res

    def logFormat(self):
        return ",".join([i.name + "(%d)" % i.number for i in self.stack])
