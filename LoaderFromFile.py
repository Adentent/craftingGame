from chardet import detect
from pip import main as pipInstall

from Communications import ItemStack, RecipeStack, attributes
from Const import Const
from LogOutput import logOutput

# Currently not used
# try:
#     from numba import jit
# except ImportError:
#     logOutput("缺失numba, 正在安装")
#     pipInstall(["install", "numba"])
#     try:
#         from numba import jit, njit
#     except ImportError:
#         logOutput("安装失败, 请自行安装numba后再运行")
#         exit()


def getFileEncoding(filepath):
    with open(filepath, "rb") as f:
        encoding = detect(f.read())["encoding"]
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
        output = i.split(">")[1].split("[")[0].split(",")
        name = i.split(">")[1].split("[")[1].split("]")[0]
        res.append([input, mid, output, name])
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
            with open(i, encoding=getFileEncoding(i)) as f:
                recipes = recipesFixer(f.readlines())
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

if __name__ == "__main__":
    Loader()
