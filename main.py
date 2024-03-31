from src import MainLoop, UserInterface

if __name__ == "__main__":
    looper = MainLoop.Loop()

    UserInterface.UserInterfaceGenerator(looper)
