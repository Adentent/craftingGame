from os import walk
from os.path import dirname, join, realpath


class Const:
    version = "1.0.0"
    currentDir = dirname(realpath(__file__))
    itemsDir = join(currentDir, "../items")
    itemsFiles = []
    for root, dirs, files in walk(itemsDir):
        for file in files:
            itemsFiles.append(join(root, file))
    recipesDir = join(currentDir, "../recipes")
    recipesFiles = []
    for root, dirs, files in walk(recipesDir):
        for file in files:
            recipesFiles.append(join(root, file))
