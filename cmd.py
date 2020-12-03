
from collections import namedtuple
import traceback
#import file

Command = namedtuple('Command', 'f help')
promptline = "> "

commands = {}
DEBUG = True

def evalLoop(before=None, after=None):
    try:
        while True:
            print(promptline, end="")
            args = input().split()
            if before:
                before(args)
            runCommand(args)
            if after:
                after(args)
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass

    # print("What is your name?")
    # print("Hello, " + input() + ".")

def addCommand(name, f, helpstr):
    commands[name] = Command(f, helpstr)

def setPrompt(s):
    global promptline
    promptline = s

def runCommand(args):
    name = args[0]
    if name == "help":
        if len(args) > 1:
            commandHelp(args[1])
        else:
            commandHelp("commands")
            print(" Type 'help (command)' to get more information about a command.")
    elif name in commands:
        try:
            commands[name].f(args[1:])
        except Exception as e:
            if DEBUG:
                print(" Exception: ", e)
                traceback.print_exc()
            print(" Command error or invalid arguments.")
            commandHelp(name)
    else:
        print(" Unknown Command: '%s'" % name)

def commandHelp(name):
    if name == "commands":
        print(" Available Commands: ", end="")
        for name in sorted(commands.keys()):
            print(name, end=", ")
        print()
    elif name in commands:
        print(" %s: %s" % (name, commands[name].help))
    else:
        print(" Unknown Command: '%s'" % name)

if __name__ == "__main__":
    def greet(args):
        name = "there"
        if len(args) > 0:
            name = args[0]
        print("Hello, %s." % name)
    addCommand("greet", greet, "greet [person] - Say a greeting")
    evalLoop()
