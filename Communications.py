from typing import Dict, List, Tuple


class Item:
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number


class Recipe:
    def __init__(self, input: list[Item], mid: Item, output: list[Item], name: str):
        self.input = input
        self.mid = mid
        self.output = output
        self.name = name


class ItemStack:
    def __init__(self):
        self.stack: List[Item] = []

    def addItem(self, name: str):
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

    def returnAllItems(self) -> Tuple[str, ...]:
        return tuple(i.name for i in self.stack)

    def logFormat(self):
        return ",".join([i.name + "(%d)" % i.number for i in self.stack])


class RecipeStack:
    def __init__(self, itemStack: ItemStack) -> None:
        self.itemStack = itemStack
        self.stack = []

    def addRecipe(self, ipt: list, mid: str, output: list, name: str):
        recipe = Recipe(
            self.itemStack.findItems(ipt),
            self.itemStack.findItem(mid),
            self.itemStack.findItems(output),
            name,
        )
        self.stack.append(recipe)

    def addRecipes(self, stack: list):
        for i in stack:
            self.addRecipe(i[0], i[1], i[2], i[3])

    def returnOutputs(self) -> list[list[Item]]:
        res = []
        for i in self.stack:
            res.append(i.output)
        return res

    def returnRecipes(self) -> list[Recipe]:
        return self.stack

    def logFormat(self):
        return "\n".join(
            [
                "{}: {}经过{}产出{}".format(
                    i.name,
                    ",".join([j.name for j in i.input]),
                    i.mid.name,
                    ",".join([j.name for j in i.output]),
                )
                for i in self.stack
            ]
        )


class PlayerInventoryItemStack:
    def __init__(self) -> None:
        self.stack = {}
        self.communicationUpdate()

    def communicationUpdate(self):
        attributes.inventory = self

    def getItem(self, item: Item, number: int):
        if number <= 0:
            return
        if item not in self.stack.keys():
            self.stack[item] = 0
        self.stack[item] += number
        self.communicationUpdate()

    def loseItem(self, item: Item, number: int):
        if item not in self.stack.keys():
            return False
        if self.stack[item] < number:
            return False
        self.stack[item] -= number
        self.communicationUpdate()
        return True

    def returnItems(self) -> Dict[Item, int]:
        return self.stack

    def craftItem(self, recipe: Recipe):
        inventoryBackup = self.stack
        inputs = recipe.input
        for i in inputs:
            if self.loseItem(
                i, 1
            ):  # If the player doesn't own enough items, then return all the items.
                self.stack = inventoryBackup
                return 1
        outputs = recipe.output
        for i in outputs:
            self.getItem(i, 1)
        self.communicationUpdate()
        return 0

    def formatOutput(self) -> str:
        allZero = False
        for i in self.stack.items():
            if i != 0:
                break
            allZero = True
        if (not self.stack) or allZero:
            return "空空如也..."
        res = ""
        for item in self.stack:
            number = self.stack[item]
            if number == 0:
                continue
            res += f"{item.name}({number}), "
        return res[:-2]


class event:
    goQuit = False
    treeButtonDown = [False, -1]
    treeButtonRelease = [False, -1]
    mineButtonDown = [False, -1]
    mineButtonRelease = [False, -1]


class attributes:
    itemStack: ItemStack
    recipeStack: RecipeStack
    inventory: PlayerInventoryItemStack
