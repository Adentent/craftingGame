import json

from chardet import detect
from pip import main as pipInstall

from Communications import ItemStack, RecipeStack, attributes
from Const import Const
from LogOutput import logOutput

# Currently not used
# from numba import jit


def getFileEncoding(filepath):
    with open(filepath, "rb") as f:
        encoding = detect(f.read())["encoding"]
        if encoding in ["ISO-8859-1", "ASCII"]:
            return "GB2312"
        if encoding == "EUC-TW":
            return "GBK"
        return encoding


def recipesFixer(originJsonScript: str):
    res = []
    for key, value in json.loads(originJsonScript).items():
        name = key
        ipt = value["input"]
        if "mid" in value:
            mid = value["mid"]
        else:
            mid = None
        opt = value["output"]
        res.append([ipt, mid, opt, name])
    return res


class Loader:
    def __init__(self):
        """加载所有物品和合成表"""
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
            # print(i)
            if ".rcp" in str(i):
                logOutput(f"请不要使用rcp文件, 已忽略{i}")
                continue
            with open(i, encoding=getFileEncoding(i)) as f:
                recipes = recipesFixer(f.read())
                recipeStack.addRecipes(recipes)
        logOutput("读取配方完毕")
        logOutput("所有配方输出如下：\n" + recipeStack.logFormat())

    def returnValue(self):
        return itemStack, recipeStack

    def writeIntoCommunication(self):
        attributes.recipeStack = recipeStack
        attributes.itemStack = itemStack


itemStack = ItemStack()
recipeStack = RecipeStack(itemStack)
