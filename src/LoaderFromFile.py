import json
from collections import deque
from typing import Deque

from chardet import detect

from src.Communications import ItemStack, RecipeStack, attributes
from src.Const import Const
from src.LogOutput import logOutput


def getFileEncoding(filepath):
    with open(filepath, "rb") as f:
        encoding = detect(f.read())["encoding"]
        if encoding in ["ISO-8859-1", "ASCII"]:
            return "GB2312"
        if encoding == "EUC-TW":
            return "GBK"
        return encoding


def recipesFixer(originJsonScript: str) -> Deque:
    res = deque()
    for key, value in json.loads(originJsonScript).items():
        name = key
        ipt = value["input"]
        if "mid" in value:
            mid = value["mid"]
        else:
            mid = None
        opt = value["output"]
        if "time" in value:
            time = value["time"]
        else:
            time = 0
        res.append([ipt, mid, opt, name, time])
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
                tag = ""
                items = f.readlines()
                if items[0] == "#" and "MACHINE" in items[0]:
                    tag = "machine"
                for item in items:
                    item = item.removesuffix("\n")
                    if item == "" or item[0] == "#" or item[:2] == "//":
                        continue
                    itemStack.addItem(item, tag)
        logOutput("读取物品完毕")
        logOutput(f"所有物品输出如下：\n{itemStack}")

    def recipesLoad(self):
        logOutput("读取配方")
        for i in Const.recipesFiles:
            if ".rcp" in str(i):
                logOutput(f"请不要使用rcp文件, 已忽略{i}")
                continue
            with open(i, encoding=getFileEncoding(i)) as f:
                recipes = recipesFixer(f.read())
                recipeStack.addRecipes(recipes)
        logOutput("读取配方完毕")
        logOutput(f"所有配方输出如下：\n{recipeStack}")

    def returnValue(self):
        return itemStack, recipeStack

    def writeIntoCommunication(self):
        attributes.recipeStack = recipeStack
        attributes.itemStack = itemStack


itemStack = ItemStack()
recipeStack = RecipeStack(itemStack)
