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


# TODO: 弃用, 使用json来实现, 目前由于使用了读取整个文件夹的方案, json文件也被错误读取, 目前程序无法使用
# def recipesFixer(origin: list[str]):
#     print(origin)
#     res = []
#     for i in origin:
#         i = "".join(i.split())  # 除去所有空格
#         input = i.split("-")[0].split(",")
#         if "->" in i:
#             mid = None
#         else:
#             mid = i.split("-")[1].split(">")[0]
#         output = i.split(">")[1].split("[")[0].split(",")
#         name = i.split(">")[1].split("[")[1].split("]")[0]
#         res.append([input, mid, output, name])
#     return res


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
                # recipes = recipesFixer(f.readlines())
                # print(f.read())
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
