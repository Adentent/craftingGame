from os import walk
from os.path import dirname, join, realpath


class Const:
    currentDir = dirname(realpath(__file__))
    itemsDir = join(currentDir, "items")
    itemsFiles = []
    for root, dirs, files in walk(itemsDir):
        for file in files:
            itemsFiles.append(join(root, file))
    recipesDir = join(currentDir, "recipes")
    recipesFiles = []
    for root, dirs, files in walk(recipesDir):
        for file in files:
            recipesFiles.append(join(root, file))

    # Events
    eventGetInventory = 0
    eventQuit = 1
    eventTreeButtonDown = 2
    eventTreeButtonRelease = 3
    eventMineButtonDown = 4
    eventMineButtonRelease = 5
    eventGetRecipeStack = 6
