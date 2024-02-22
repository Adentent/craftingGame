from time import ctime, time
from tkinter import END, Button, Label, Text, Tk
from tkinter.font import Font

from Communications import *
from LogOutput import logOutput
from MainLoop import Loop


class UserInterfaceGenerator:  # It is not a interface, but it is a user interface. (cold joke)
    def __init__(self, looper: Loop):
        self.recipeStack = self.returnRecipeStack()
        self.looper = looper

        self.root = Tk()
        self.root.title("Contribute & Idea & Code by Adentent | 2023/9/29 版本")

        self.generateWidgets()
        self.buttonBind()
        self.root.after(10, self.looper.eventWaiting, self.root)
        self.root.after(100, self.clockUpdate)
        self.root.mainloop()

        logOutput("UI界面终止")

    def generateWidgets(self):
        self.textShowInfo = Text(self.root, cursor="arrow", height=8, width=50)
        self.textShowInfo.bind("<Button-1>", lambda f: "break")
        self.textShowInfo.delete(1.0, END)
        self.showInfo(
            "Tips:\n按'Q'来获取一些橡树木头...\n按'W'来挖矿...\n按H以显示此Tips",
        )
        self.textShowInfo.pack(fill="both", expand=True)
        self.buttonShowInventory = Button(
            self.root, text="查看背包", command=self.showInventory
        )
        self.buttonShowInventory.pack()
        self.buttonCraft = Button(self.root, text="合成", command=self.showCraft)
        self.buttonCraft.pack()
        self.buttonShowInventory = Button(self.root, text="帮助", command=self.showTips)
        self.buttonShowInventory.pack()
        self.clock = Label(self.root, text="")
        self.clock.pack()

    def buttonBind(self):
        self.root.bind("<KeyPress-q>", self.qDown)
        self.root.bind("<KeyRelease-q>", self.qRelease)
        self.root.bind("<KeyPress-w>", self.wDown)
        self.root.bind("<KeyRelease-w>", self.wRelease)
        self.root.bind("<Key-e>", self.showInventory)
        self.root.bind("<Key-h>", self.showTips)
        self.root.focus_set()

    def returnRecipeStack(self):
        res = attributes.recipeStack
        return res

    def returnInventory(self):
        res = attributes.inventory
        return res

    def showInventory(self, _=None):
        inventory = self.returnInventory()
        self.textShowInfo.delete(1.0, END)
        self.showInfo("背包: " + inventory.formatOutput())
        self.root.update()

    def showCraft(self):
        recipeStackRecipes = self.recipeStack.returnRecipe()
        self.textShowInfo.delete(1.0, END)
        for i in recipeStackRecipes:
            for j in i.output:
                self.textShowInfo.tag_configure(
                    "link" + j.name, foreground="blue", underline=True
                )
                self.showInfo(j.name, "link" + j.name)
                self.textShowInfo.tag_bind(
                    "link" + j.name, "<Button-1>", lambda _: self.showRecipe(i)
                )
        self.root.update()

    def showTips(self, _=None):
        self.textShowInfo.delete(1.0, END)
        self.showInfo("Tips:\n按'Q'来获取一些橡树木头...\n按'W'来挖矿...")
        self.root.update()

    def qDown(self, _):
        if event.treeButtonDown[1] != -1:
            return

        event.treeButtonDown = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.showInfo("正在获取橡木...")
        self.root.update()

    def qRelease(self, _):
        if not event.treeButtonDown[0]:
            # logOutput(str(event.treeButtonDown))
            return

        event.treeButtonRelease = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.showInfo("橡木获取好了")

    def wDown(self, _):
        if event.mineButtonDown[1] != -1:
            return

        event.mineButtonDown = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.showInfo("正在挖矿...")
        self.root.update()

    def wRelease(self, _):
        if not event.mineButtonDown[0]:
            # logOutput(str(event.mineButtonDown))
            return

        event.mineButtonRelease = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.showInfo("矿挖好了")

    def showRecipe(self, recipe):
        self.textShowInfo.delete(1.0, END)
        self.showInfo(
            f"{', '.join([i.name for i in recipe.input])}通过{recipe.mid.name}来合成{', '.join([i.name for i in recipe.output])}",
        )
        self.textShowInfo.tag_config("back", foreground="blue", underline=True)
        self.textShowInfo.tag_bind("back", "<Button-1>", lambda _: self.showCraft())
        self.showInfo(f"<-返回", "back")

    def clockUpdate(self):
        self.clock["text"] = ctime()
        self.root.update()
        self.root.after(100, self.clockUpdate)

    def showInfo(self, text: str, tag: str = ""):
        if text == "\n":
            self.textShowInfo.insert(END, "\n")
            return
        lines = text.split("\n")
        existing_lines = self.textShowInfo.get("1.0", END).count("\n")
        print(existing_lines)
        for j in range(len(lines)):
            line = lines[j]
            if tag == "":
                self.textShowInfo.insert(END, line + "\n")
            else:
                self.textShowInfo.insert(END, line + "\n", tag)
            print(line)
            for i in range(len(line)):
                if "\u4e00" <= line[i] <= "\u9fff":  # 判断是否为中文字符
                    self.textShowInfo.tag_configure(
                        "chinese", font=("MiSans Normal", 12)
                    )
                    self.textShowInfo.tag_add(
                        "chinese",
                        f"{j+existing_lines}.{i}",
                        f"{j+existing_lines}.{i+1}",
                    )
                else:
                    self.textShowInfo.tag_configure("english", font=("Exo", 12))
                    self.textShowInfo.tag_add(
                        "english",
                        f"{j+existing_lines}.{i}",
                        f"{j+existing_lines}.{i+1}",
                    )
