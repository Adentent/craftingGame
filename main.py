import json

from pip import main as pipInstall

import MainLoop
import UserInterface
from Const import Const
from LogOutput import logOutput

logOutput("配置Python运行时环境")
with open("setups.json", "r+") as f:
    setups = json.load(f)
    Const.version = setups["version"]
    if not setups["pipInstalled"]:
        pipInstall(["install", "-r", "requirements.txt"])
        setups["pipInstalled"] = True
        json.dump(setups, f)
    else:
        logOutput("已经完成安装, 跳过该步骤")


looper = MainLoop.Loop()

UserInterface.UserInterfaceGenerator(looper)
