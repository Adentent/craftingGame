from queue import Queue
from threading import Thread

import MainLoop
import UserInterface
from LogOutput import logOutput

queue = Queue()

ThreaduserInterface = Thread(target=UserInterface.UserInterfaceGenerator, args=(queue,))
ThreadmainLoop = Thread(target=MainLoop.Loop, args=(queue,))

logOutput("正在启动UI线程")
ThreaduserInterface.start()
logOutput("UI线程启动成功")
logOutput("正在启动主循环线程")
ThreadmainLoop.start()
logOutput("主循环线程启动成功")
