from pip import main as pipInstall

import MainLoop
import UserInterface
from LogOutput import logOutput

logOutput("配置Python运行时环境")
pipInstall(["install", "-r", "requirements.txt"])

looper = MainLoop.Loop()

UserInterface.UserInterfaceGenerator(looper)
