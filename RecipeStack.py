class RecipeStack:
    from Item import Item
    from Recipe import Recipe
    def __init__(self, itemStack) -> None:
        self.itemStack = itemStack
        self.stack = []

    def addRecipe(self, input: list, mid: str, output: list):
        from Recipe import Recipe
        recipe = Recipe(
            self.itemStack.findItems(input),
            self.itemStack.findItem(mid),
            self.itemStack.findItems(output),
        )
        self.stack.append(recipe)

    def addRecipes(self, stack: list):
        for i in stack:
            self.addRecipe(i[0], i[1], i[2])

    def returnOutputs(self) -> list[list[Item]]:
        res = []
        for i in self.stack:
            res.append(i.output)
        return res

    def returnRecipe(self) -> list[Recipe]:
        return self.stack

    def logFormat(self):
        return "\n".join(
            [
                "{}经过{}产出{}".format(
                    ",".join([j.name for j in i.input]),
                    i.mid.name,
                    ",".join([j.name for j in i.output]),
                )
                for i in self.stack
            ]
        )