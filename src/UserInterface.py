from os import name as operatingSystemName
from time import ctime, time
from tkinter import END, LEFT, Event, Tk
from tkinter.font import ITALIC
from pyglet import font
from ttkbootstrap import Button, Frame, Label, PhotoImage, Style, Text
from ttkbootstrap.dialogs.dialogs import Messagebox
from Communications import *
from Const import Const
from LogOutput import logOutput
from MainLoop import Loop


class MyText(Text):
    def add_tag_to_text(self, specifer: str, tag_name: str):
        start = 1.0
        while True:
            start = self.search(specifer, start, END)
            if not start:
                break
            end = f"{start}+{len(specifer)}c"
            self.tag_add(tag_name, start, end)
            start = end

    def item_specifer(self):
        items = attributes.itemStack.returnAllItems()
        for i in items:
            if i not in self.get(1.0, END):
                continue
            self.add_tag_to_text(i, f"item_{i}")

    def showInfo(self, text: str, tag: str = ""):
        if text == "\n":
            self.insert(END, "\n")
            return
        lines = text.split("\n")
        existing_lines = self.get("1.0", END).count("\n")
        for j in range(len(lines)):
            line = lines[j]
            if tag == "":
                self.insert(END, line + "\n")
            else:
                self.insert(END, line + "\n", tag)
            for i in range(len(line)):
                if "\u4e00" <= line[i] <= "\u9fff":  # 判断是否为中文字符
                    self.tag_configure("chinese", font=("MiSans Normal", 12))
                    self.tag_add(
                        "chinese",
                        f"{j+existing_lines}.{i}",
                        f"{j+existing_lines}.{i+1}",
                    )
                else:
                    self.tag_configure("english", font=("Exo", 12))
                    self.tag_add(
                        "english",
                        f"{j+existing_lines}.{i}",
                        f"{j+existing_lines}.{i+1}",
                    )
        self.item_specifer()


class UserInterfaceGenerator:  # It is not a interface, but it is a user interface. (cold joke)
    def __init__(self, looper: Loop):
        if not font.have_font("MiSans") or not font.have_font("Exo"):
            font.add_directory("assets/fonts")
            font.load("MiSans Medium")
            font.load("Exo")
        self.ifDarkMode = True
        self.looper = looper

        self.style = Style(theme="darkly")
        self.root: Tk = self.style.master
        self.root.title(f"Craft Game | Version {Const.version}")
        self.root.overrideredirect(True)

        self.generateWidgets()
        self.buttonBind()
        self.tagInitiation()
        self.root.after(10, self.looper.eventWaiting, self.root)
        self.root.after(100, self.DynWidgetsUpdates)
        self.root.mainloop()

        logOutput("UI界面终止")

    def generateWidgets(self):
        self.textShowInfo = MyText(self.root, cursor="arrow", height=8, width=25)
        self.textShowInfo.bind("<Button-1>", lambda _: "break")
        self.textShowInfo.showInfo(
            "Tips:\n按'Q'来获取一些橡树木头...\n按'W'来挖矿...\n按'H'以显示此Tips",
        )
        self.textShowRecipeStatus = MyText(
            self.root, cursor="arrow", height=8, width=25
        )
        self.textShowRecipeStatus.bind("<Button-1>", lambda _: "break")
        self.textShowInfo.pack(side=LEFT, fill="both", expand=True)
        self.textShowRecipeStatus.pack(side="right", fill="both", expand=True)

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
        self.buttonShowCredits = Button(
            self.buttonFrame, text="Credits", command=self.showCredits
        )
        self.darkModeSwitch = Button(
            self.buttonFrame, text="暗色模式开关", command=self.darkMode
        )
        self.buttonShowInventory.pack(side=LEFT)
        self.buttonCraft.pack(side=LEFT)
        self.buttonShowTips.pack(side=LEFT)
        self.buttonShowCredits.pack(side=LEFT)
        self.darkModeSwitch.pack(side=LEFT)
        self.buttonFrame.pack()

        self.clock = Label(self.root, text="")
        self.clock.pack()
        self.tooltip = Label(self.root)

        self.setDarkerTitleBar(self.root)

    # 设置暗色调的标题栏！！
    def setDarkerTitleBar(self, window):
        if operatingSystemName == "nt":
            from ctypes import byref, c_int, windll

            window.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            hwnd = windll.user32.GetParent(window.winfo_id())
            value = c_int(True)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), 4
            )
            window.update()

    def buttonBind(self):
        self.root.bind("<KeyPress-q>", self.qDown)
        self.root.bind("<KeyRelease-q>", self.qRelease)
        self.root.bind("<KeyPress-w>", self.wDown)
        self.root.bind("<KeyRelease-w>", self.wRelease)
        self.root.bind("<Key-e>", self.showInventory)
        self.root.bind("<Key-h>", self.showTips)
        self.root.bind("<Key-d>", self.showRecipes)
        self.root.bind("<Key-esc>")
        self.root.focus_set()

        self.root.bind("<Motion>", self.tooltipMove)

    def showInventory(self, _=None):
        self.textShowInfo.delete(1.0, END)
        self.textShowInfo.showInfo(f"背包: {attributes.inventory}")
        self.root.update()

    def showRecipes(self, _=None):
        recipeStackRecipes = attributes.recipeStack.returnRecipes()
        self.textShowInfo.delete(1.0, END)
        for i in recipeStackRecipes:
            if (
                i.mid is not None
                and i.mid not in attributes.inventory.returnItems().keys()
            ):
                continue
            for j in i.output:
                self.textShowInfo.tag_configure(f"link_{i.name}", underline=True)
                self.textShowInfo.tag_bind(
                    f"link_{i.name}", "<Button-1>", self.showRecipe(i)
                )
                self.textShowInfo.showInfo(j.name, f"link_{i.name}")
        self.root.update()

    def showTips(self, _=None):
        self.textShowInfo.delete(1.0, END)
        self.textShowInfo.showInfo("Tips:\n按'Q'来获取一些橡树木头...\n按'W'来挖矿...")
        self.root.update()

    def qDown(self, _):
        if event.treeButtonDown[1] != -1:
            return

        event.treeButtonDown = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.textShowInfo.showInfo("正在获取橡木...")
        self.root.update()

    def qRelease(self, _):
        if not event.treeButtonDown[0]:
            return

        event.treeButtonRelease = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.textShowInfo.showInfo("橡木获取好了")

    def wDown(self, _):
        if event.mineButtonDown[1] != -1:
            return

        event.mineButtonDown = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.textShowInfo.showInfo("正在挖矿...")
        self.root.update()

    def wRelease(self, _):
        if not event.mineButtonDown[0]:
            return

        event.mineButtonRelease = [True, time()]
        self.textShowInfo.delete(1.0, END)
        self.textShowInfo.showInfo("矿挖好了")

    def showRecipe(self, recipe: Recipe):
        def callback(_):
            self.textShowInfo.delete(1.0, END)
            if recipe.mid is not None:
                self.textShowInfo.showInfo(
                    f"{', '.join([i.name for i in recipe.input])}通过{recipe.mid.name}来合成{', '.join([i.name for i in recipe.output])}",
                )
            else:
                self.textShowInfo.showInfo(
                    f"用{', '.join([i.name for i in recipe.input])}制作{', '.join([i.name for i in recipe.output])}",
                )
            self.textShowInfo.tag_config("back", underline=True)
            self.textShowInfo.tag_bind(
                "back", "<Button-1>", lambda _: self.showRecipes()
            )
            self.textShowInfo.tag_configure("craft", underline=True)
            self.textShowInfo.tag_bind("craft", "<Button-1>", self.doRecipe(recipe))
            self.textShowInfo.showInfo("合成", "craft")
            self.textShowInfo.showInfo("返回", "back")

        return callback

    def doRecipe(self, recipe: Recipe):
        self.textShowInfo.showInfo(f"需要{recipe.time / 1000}s来完成这个合成...")

        def showRecipeStatus(_) -> None:
            inventoryCpy = attributes.inventory
            for item, number in recipe.input.items():
                if not inventoryCpy.loseItem(item, number):
                    if item in attributes.inventory.returnItems():
                        self.textShowRecipeStatus.showInfo(
                            f"合成失败! 缺失{number - attributes.inventory.returnItems()[item]}个{item.name}!",
                        )
                    else:
                        self.textShowRecipeStatus.showInfo(
                            f"合成失败! 缺失{number}个{item.name}!"
                        )
                    return
            self.textShowRecipeStatus.showInfo(
                f"开始合成{', '.join([i.name for i in recipe.output.keys()])}"
            )

            def startRecipeTimedTask() -> None:
                for ipt in recipe.input:
                    attributes.inventory.loseItem(ipt, 1)
                for opt in recipe.output:
                    attributes.inventory.getItem(opt, 1)
                self.textShowRecipeStatus.showInfo(
                    f"{', '.join([i.name for i in recipe.output.keys()])}合成成功!"
                )

            self.root.after(recipe.time, startRecipeTimedTask)

        return showRecipeStatus

    def DynWidgetsUpdates(self):
        self.clock["text"] = ctime()
        self.root.update()
        self.root.after(100, self.DynWidgetsUpdates)

    def showCredits(self):
        Messagebox.show_info("All By Adentent")

    def tagInitiation(self):
        items = attributes.itemStack.returnAllItems()
        for i in items:
            self.textShowInfo.tag_configure(
                f"item_{i}", font=("MiSans Normal", 12, ITALIC)
            )
            self.textShowInfo.tag_bind(f"item_{i}", "<Enter>", self.enterItemTag(i))
            self.textShowInfo.tag_bind(f"item_{i}", "<Leave>", self.leaveItemTag)
            self.textShowRecipeStatus.tag_configure(
                f"item_{i}", font=("MiSans Normal", 12, ITALIC)
            )
            self.textShowRecipeStatus.tag_bind(
                f"item_{i}", "<Enter>", self.enterItemTag(i)
            )
            self.textShowRecipeStatus.tag_bind(
                f"item_{i}", "<Leave>", self.leaveItemTag
            )

    def enterItemTag(self, name: str):
        def callback(e: Event):
            global image
            image = PhotoImage(file=f"assets/resources/{name}.png").subsample(2)
            self.tooltip.configure(image=image)
            self.tooltip.place(
                x=e.x_root - self.root.winfo_rootx() + 5,
                y=e.y_root - self.root.winfo_rooty() + 5,
            )

        return callback

    def leaveItemTag(self, _):
        self.tooltip.place_forget()

    def tooltipMove(self, e):
        if not self.tooltip.winfo_ismapped():
            return
        self.tooltip.place(
            x=e.x_root - self.root.winfo_rootx() + 5,
            y=e.y_root - self.root.winfo_rooty() + 5,
        )

    def darkMode(self):
        if self.ifDarkMode:
            self.style = Style(theme="flatly")
        else:
            self.style = Style(theme="darkly")
        self.ifDarkMode = not self.ifDarkMode
