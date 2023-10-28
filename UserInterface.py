from queue import Queue
from time import sleep
from tkinter import Tk, Label, Button, Text, END

from Const import Const
from LogOutput import logOutput


class UserInterfaceGenerator:  # It is not a interface, but it is a user interface. (cold joke)
    def __init__(self, queue: Queue):
        self.queue = queue
        self.recipeStack = self.returnRecipeStack()
        self.root = Tk()

        self.rootSetup()

        self.generateWidgets()

        self.buttonBind()

        self.root.mainloop()

        self.queue.put(Const.eventQuit)
        logOutput("UI界面终止")

    def generateWidgets(self):
        self.textShowInfo = Text(self.root)
        # self.textShowInfo.config(state='disabled')
        self.textShowInfo.bind('<Button-1>', lambda f:'break')
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "没有什么可展示的...")
        self.textShowInfo.pack()
        self.labelShowHelp = Label(self.root,
                                   text="按'Q'来获取一些橡树木头...\n按'W'来挖矿...")
        self.labelShowHelp.pack()
        self.buttonShowInventory = Button(self.root,
                                          text="查看背包",
                                          command=self.showInventory)
        self.buttonShowInventory.pack()
        self.buttonCraft = Button(self.root,
                                  text="合成",
                                  command=self.showCraft)
        self.buttonCraft.pack()

    def buttonBind(self):
        self.root.bind("<KeyPress-q>", self.qDown)
        self.root.bind("<KeyRelease-q>", self.qRelease)
        self.root.bind("<KeyPress-w>", self.wDown)
        self.root.bind("<KeyRelease-w>", self.wRelease)
        self.root.focus_set()

    def rootSetup(self):
        self.root.title("制作游戏 | 想法 & 代码 by Adentent | 2023/9/29 版本")

    def returnRecipeStack(self):
        self.queue.put(Const.eventGetRecipeStack)
        logOutput("发送请求配方")
        sleep(1)
        res = self.queue.get()
        logOutput("配方请求结束")
        self.queue.task_done()
        return res

    def returnInventory(self):
        self.queue.put(Const.eventGetInventory)
        logOutput("发送请求背包")
        sleep(1)
        res = self.queue.get()
        logOutput("背包请求结束")
        self.queue.task_done()
        # logOutput(f"队列里还剩{self.queue.qsize()}个任务")
        return res

    def showInventory(self):
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "翻找背包...")
        self.root.update()
        inventory = self.returnInventory()
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "背包: " + inventory)
        self.root.update()

    def showCraft(self):
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "回忆合成...")
        self.root.update()
        recipeStackRecipes = self.recipeStack.returnRecipe()
        # res = []
        for i in recipeStackRecipes:
            for j in i.output:
                # res.append(j.name)
                self.textShowInfo.tag_configure('link'+j.name, foreground='blue', underline=True)
                self.textShowInfo.delete(1., END)
                self.textShowInfo.insert(END, j.name, 'link'+j.name)
                self.textShowInfo.delete(1., END)
                self.textShowInfo.insert(END, '\n')
                self.textShowInfo.tag_bind('link'+j.name, '<Button-1>', lambda _: self.showRecipe(i))
        # self.textShowInfo['text'] = "合成: \n" + "\n".join(res)
        self.root.update()

    def qDown(self, _):
        # logOutput("按下Q")
        self.queue.put(Const.eventTreeButtonDown)
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "正在获取橡木...")
        self.root.update()

    def qRelease(self, _):
        # logOutput("松开Q")
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "橡木获取好了")
        self.queue.put(Const.eventTreeButtonRelease)

    def wDown(self, _):
        # logOutput("按下W")
        self.queue.put(Const.eventMineButtonDown)
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "正在挖矿...")
        self.root.update()

    def wRelease(self, _):
        # logOutput("松开W")
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, "矿挖好了")
        self.queue.put(Const.eventMineButtonRelease)

    def showRecipe(self, recipe):
        self.textShowInfo.delete(1., END)
        self.textShowInfo.insert(END, f"{', '.join([i.name for i in recipe.input])}通过{recipe.mid.name}来合成{', '.join([i.name for i in recipe.output])}\n")
