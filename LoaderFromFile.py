from chardet import detect

from Const import Const
from ItemStack import ItemStack
from LogOutput import logOutput
from RecipeStack import RecipeStack


def getFileEncoding(filepath):
    with open(filepath, 'rb') as f:
        encoding = detect(f.read())['encoding']
        if encoding in ["ISO-8859-1", "ASCII"]:
            return "GB2312"
        if encoding == "EUC-TW":
            return "GBK"
        return encoding


def recipesFixer(origin: list[str]):
    res = []
    for i in origin:
        i = "".join(i.split())  # 除去所有空格
        input = i.split("-")[0].split(",")
        mid = i.split("-")[1].split(">")[0]
        output = i.split(">")[1].split(",")
        res.append([input, mid, output])
    return res


class Loader:
    def __init__(self):
        """Load the recipes and items from the file.

        Returns:
            (ItemStack, RecipeStack): ItemStack is all the items ingame, RecipeStack is all the Recipes ingame.
        """
        self.itemsLoad()
        self.recipesLoad()

    def itemsLoad(self):
        logOutput("读取物品")
        for i in Const.itemsFiles:
            with open(i, encoding=getFileEncoding(i)) as f:
                items = f.readlines()
                itemStack.addItems(items)
        logOutput("读取物品完毕")
        logOutput("所有物品输出如下：\n" + itemStack.logFormat())

    def recipesLoad(self):
        logOutput("读取配方")
        for i in Const.recipesFiles:
            with open(i, encoding=getFileEncoding(i)) as f:
                recipes = recipesFixer(f.readlines())
                recipeStack.addRecipes(recipes)
        logOutput("读取配方完毕")
        logOutput("所有配方输出如下：\n" + recipeStack.logFormat())

    def returnValue(self):
        return itemStack, recipeStack


itemStack = ItemStack()
recipeStack = RecipeStack(itemStack)

if __name__ == "__main__":
    Loader()
