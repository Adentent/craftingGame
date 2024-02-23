from time import ctime, time
from tkinter import END, LEFT, SOLID, TOP, Button, Frame, Label, PhotoImage, Text, Tk

from pip import main as pipInstall

from Communications import *
from LogOutput import logOutput
from MainLoop import Loop

try:
    from pyglet import font
except ImportError:
    logOutput("缺失pyglet, 正在安装")
    pipInstall(["install", "pyglet"])
    from pyglet import font


class UserInterfaceGenerator:  # It is not a interface, but it is a user interface. (cold joke)
    def __init__(self, looper: Loop):
        if not font.have_font("MiSans") or not font.have_font("Exo"):
            font.add_directory("assets/fonts")
            font.load("MiSans Medium")
            font.load("Exo")
        self.mouseX: int = 0
        self.mouseY: int = 0
        self.looper = looper

        self.root = Tk()
        self.root.title("Contribute & Idea & Code by Adentent | 2023/9/29 版本")

        self.generateWidgets()
        self.buttonBind()
        self.tagInitiation()
        self.root.after(10, self.looper.eventWaiting, self.root)
        self.root.after(100, self.DynWidgetsUpdates)
        self.root.mainloop()

        logOutput("UI界面终止")

    def generateWidgets(self):
        self.textShowInfo = Text(self.root, cursor="arrow", height=8, width=50)
        self.textShowInfo.bind("<Button-1>", lambda f: "break")
        self.textShowInfo.delete(1.0, END)
        self.showInfo(
            "Tips:\n按'Q'来获取一些橡树木头...\n按'W'来挖矿...\n按'H'以显示此Tips",
        )
        self.textShowInfo.pack(fill="both", expand=True)

        self.buttonFrame = Frame(self.root)
        self.buttonShowInventory = Button(
            self.buttonFrame, text="查看背包", command=self.showInventory
        )
        self.buttonCraft = Button(
            self.buttonFrame, text="合成", command=self.showRecipes
        )
        self.buttonShowTips = Button(
            self.buttonFrame, text="帮助", command=self.showTips
        )
        self.buttonShowInventory.pack(side=LEFT)
        self.buttonCraft.pack(side=LEFT)
        self.buttonShowTips.pack(side=LEFT)
        self.buttonFrame.pack()

        self.clock = Label(self.root, text="")
        self.clock.pack()
        self.tooltip = Label(
            self.root,
            text="Tooltip",
            background="light grey",
            bd=1,
            relief=SOLID,
        )

    def buttonBind(self):
        self.root.bind("<KeyPress-q>", self.qDown)
        self.root.bind("<KeyRelease-q>", self.qRelease)
        self.root.bind("<KeyPress-w>", self.wDown)
        self.root.bind("<KeyRelease-w>", self.wRelease)
        self.root.bind("<Key-e>", self.showInventory)
        self.root.bind("<Key-h>", self.showTips)
        self.root.focus_set()

    def showInventory(self, _=None):
        self.textShowInfo.delete(1.0, END)
        self.showInfo("背包: " + attributes.inventory.formatOutput())
        self.root.update()

    # BUG: 表面上显示了两个合成表，其实只有一个！！
    def showRecipes(self):
        recipeStackRecipes = attributes.recipeStack.returnRecipe()
        self.textShowInfo.delete(1.0, END)
        for i in recipeStackRecipes:
            for j in i.output:
                self.textShowInfo.tag_configure(
                    "link" + j.name, foreground="blue", underline=True
                )
                self.textShowInfo.tag_bind(
                    "link" + j.name, "<Button-1>", lambda _: self.showRecipe(i)
                )
                self.showInfo(j.name, "link" + j.name)
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
        self.textShowInfo.tag_bind("back", "<Button-1>", lambda _: self.showRecipes())
        self.textShowInfo.tag_configure(
            "craft" + ",".join([i.name for i in recipe.output]),
            foreground="blue",
            underline=True,
        )
        self.textShowInfo.tag_bind(
            "craft" + ",".join([i.name for i in recipe.output]),
            "<Button-1>",
            lambda _: self.doRecipe(recipe),
        )
        self.showInfo("合成", "craft" + ",".join([i.name for i in recipe.output]))
        self.showInfo("<-返回", "back")

    def doRecipe(self, recipe: Recipe):
        inventoryCpy = attributes.inventory
        for ipt in recipe.input:
            if not inventoryCpy.loseItem(ipt, 1):
                self.textShowInfo.delete(1.0, END)
                self.showInfo(f"合成失败! 缺失{ipt.name}!")
                self.showInfo("<-返回", "back")
                return
        for ipt in recipe.input:
            attributes.inventory.loseItem(ipt, 1)
        for opt in recipe.output:
            attributes.inventory.getItem(opt, 1)
        self.showInfo(f"合成成功!")

    def DynWidgetsUpdates(self):
        self.clock["text"] = ctime()
        self.root.update()
        self.root.after(100, self.DynWidgetsUpdates)

    def showInfo(self, text: str, tag: str = ""):
        if text == "\n":
            self.textShowInfo.insert(END, "\n")
            return
        lines = text.split("\n")
        existing_lines = self.textShowInfo.get("1.0", END).count("\n")
        for j in range(len(lines)):
            line = lines[j]
            if tag == "":
                self.textShowInfo.insert(END, line + "\n")
            else:
                self.textShowInfo.insert(END, line + "\n", tag)
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
        self.item_specifer()

    # BUG: 为什么什么都是铬？？？
    def add_tag_to_text(self, specifer: str, tag_name: str):
        start = 1.0
        while True:
            start = self.textShowInfo.search(specifer, start, END)
            if not start:
                break
            end = f"{start}+{len(specifer)}c"
            self.textShowInfo.tag_add(tag_name, start, end)
            start = end

    def item_specifer(self):
        items = attributes.itemStack.returnAllItems()
        for i in items:
            if i not in self.textShowInfo.get(1.0, END):
                continue
            self.add_tag_to_text(i, f"item_{i}")

    def tagInitiation(self):
        items = attributes.itemStack.returnAllItems()
        for i in items:
            self.textShowInfo.tag_configure(f"item_{i}", background="light grey")
            self.textShowInfo.tag_bind(
                f"item_{i}", "<Enter>", lambda e: self.enterItemTag(e, i)
            )
            self.textShowInfo.tag_bind(f"item_{i}", "<Leave>", self.leaveItemTag)

    def enterItemTag(self, e, name: str):
        global image
        image = PhotoImage(file=f"assets/resources/{name}.png")
        self.tooltip.configure(
            image=image,
            text=name,
            compound=TOP,
            anchor="sw",
            font=("MiSans Normal", 10),
        )
        self.tooltip.place(x=e.x, y=e.y)

    def leaveItemTag(self, _):
        global image
        self.tooltip.place_forget()
