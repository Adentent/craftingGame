from random import choice

from Communications import *
from LoaderFromFile import Loader
from LogOutput import logOutput


# TODO: 制作一个能让工作台等Machine放下来的办法, 并且给Item加一个属性以区分Item和Machine
class Loop:
    def __init__(self):
        self.loader = Loader()
        self.loader.writeIntoCommunication()
        self.itemStack, self.recipeStack = self.loader.returnValue()
        self.playerItemStack = PlayerInventoryItemStack()

    def eventWaiting(self, root):
        # 定时任务
        if event.goQuit:
            return
        if event.treeButtonRelease[0]:
            newTrees = int((event.treeButtonRelease[1] - event.treeButtonDown[1]))
            self.playerItemStack.getItem(self.itemStack.findItem("橡树木头"), newTrees)
            event.treeButtonRelease = [False, -1]
            event.treeButtonDown = [False, -1]
        if event.mineButtonRelease[0]:
            newOres = int((event.mineButtonRelease[1] - event.mineButtonDown[1]))
            self.playerItemStack.getItem(
                self.itemStack.findItem(choice(["铁", "锡", "铜"])), newOres
            )
            event.mineButtonRelease = [False, -1]
            event.mineButtonDown = [False, -1]
        root.after(10, self.eventWaiting, root)
