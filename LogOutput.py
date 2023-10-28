from time import localtime, strftime

def logOutput(context: str):
    for i in context.split("\n"):
        time = strftime("%H:%M:%S", localtime())
        print("[%s] %s" % (time, i))
