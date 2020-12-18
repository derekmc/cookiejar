
from collections import namedtuple
import traceback
#import file

Command = namedtuple('Command', 'f help')
promptline = "> "

commands = {}
DEBUG = True

#
# User "Sessions" can be "multiplexed" into a single stream.
# If the first word of an input line is a number, that is the id of a user session.
# and the command is the second word.
#
# Sessions allow actions to be processed as being run by a particular user/connection.
# which could be useful for writing a game or allowing users to login and then issue
# commands under their account.
# 
# Sessions are multiplexed by an interemediate service.  For example, a web server
# may take web requests, and using cookies, identify which client made that request
# and assign those actions to a particular session.  This way, the service does not
# need to directly process cookies and other meta information, and yet users cannot
# directly dictate what session they are running.
#
# The command framework does not assign the session ids, but rather uses whatever number
# the intermediate service stipulates to identify sessions.  It makes sense to keep
# this number within a 32 bit integer range if possible.
#
# The intermediate service, performing the session multiplexing, should verify that user
# commands do not start with a number, so that users may not hijack another session.
#
# 0 is always a guest session.
#
# Session Example(chess):
# > 0 viewboard
#    (boardstate echoed)
# > 1 move e2 e4
#    (boardstate echoed)
# > 2 move c7 c5
#    (boardstate echoed)

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

def isNonNegativeInteger(s):
    try:
        n = int(s)
        return False if n < 0 else True
    except ValueError:
        return False

def runCommand(args):
    sessid = 0
    if len(args) == 0:
        return
    if isNonNegativeInteger(args[0]):
        sessid = int(args[0])
        args = args[1:]

    cmdname = args[0]
    if cmdname == "help":
        if len(args) > 1:
            commandHelp(args[1])
        else:
            commandHelp("commands")
            print(" Type 'help (command)' to get more information about a command.")
    elif cmdname in commands:
        try:
            commands[cmdname].f(args[1:], sessid=sessid)
        except Exception as e:
            if DEBUG:
                print(" Exception: ", e)
                traceback.print_exc()
            print(" Command error or invalid arguments.")
            commandHelp(cmdname)
    else:
        print(" Unknown Command: '%s'" % cmdname)

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
