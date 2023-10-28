from queue import Queue
from random import choice

from Const import Const
from LoaderFromFile import Loader
# from LogOutput import logOutput
from PlayerInventoryItemStack import PlayerInventoryItemStack


class Loop:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.itemStack, self.recipeStack = Loader().returnValue()
        self.playerItemStack = PlayerInventoryItemStack()
        self.queueWaiting()
    def queueWaiting(self):
        treeTime = 0
        mineTime = 0
        while True:
            # logOutput("等待请求")
            event = self.queue.get()
            # logOutput(f"接收到请求{event}")
            if event == Const.eventQuit:
                self.queue.task_done()
                # logOutput("终止程序")
                return
            elif event == Const.eventGetInventory:
                # logOutput("请求物品栏")
                self.queue.put(self.playerItemStack.formatOutput())
                # logOutput("物品栏请求完成")
            elif event == Const.eventTreeButtonDown:
                treeTime += 1
            elif event == Const.eventTreeButtonRelease:
                newTrees = treeTime // 5
                self.playerItemStack.getItem(self.itemStack.findItem("橡树木头"), newTrees)
            elif event == Const.eventMineButtonDown:
                mineTime += 1
            elif event == Const.eventMineButtonRelease:
                newOres = mineTime // 5
                self.playerItemStack.getItem(self.itemStack.findItem(choice(["铁", "锡", "铜"])), newOres)
            elif event == Const.eventGetRecipeStack:
                self.queue.put(self.recipeStack)
            self.queue.task_done()
            self.queue.join()
            # logOutput("请求结束")
