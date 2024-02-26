from typing import Dict, List, Tuple, Union


class Item:
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number


class Recipe:
    def __init__(
        self,
        input: Dict[Item, int],
        mid: Union[Item, None],
        output: Dict[Item, int],
        name: str,
    ):
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

    def findItem(self, name: str) -> Item:
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
        self.stack: List[Recipe] = []

    def addRecipe(
        self,
        ipt: Dict[str, int],
        mid: Union[str, None],
        output: Dict[str, int],
        name: str,
    ):
        recipe = Recipe(
            {self.itemStack.findItem(item): number for item, number in ipt.items()},
            None if mid is None else self.itemStack.findItem(mid),
            {self.itemStack.findItem(item): number for item, number in output.items()},
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
        res = []
        for i in self.stack:
            input_names = ", ".join(
                [f"{number}个{inp.name}" for inp, number in i.input.items()]
            )

            output_names = ", ".join(
                [f"{number}个{out.name}" for out, number in i.output.items()]
            )

            if i.mid is None:
                res.append(f"{i.name}: 用{input_names}制作{output_names}")
            else:
                res.append(f"{i.name}: {input_names}经过{i.mid.name}产出{output_names}")
        return "\n".join(res)


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
