
# if a command is invoked without any arguments, all arguments are
# prompted to the user one at a time, and any may be left blank.
# if a command is invoked with at least one argument, there are
# no prompts.

from collections import namedtuple
import traceback
#import file

Command = namedtuple('Command', 'f args help')
promptline = "> "

commands = {}
DEBUG = True
#DEBUG = False

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

def addCommand(cmd, f, helpstr):
    args = cmd.split()
    if len(args) < 1:
        raise ValueError("addCommand: no command given")
    name = args[0]
    args = args[1:]
    commands[name] = Command(f, args, helpstr)

def setPrompt(s):
    global promptline
    promptline = s

def isNonNegativeInteger(s):
    try:
        n = int(s)
        return False if n < 0 else True
    except ValueError:
        return False

# preserve sessid, until it is unset.
sessid = 0
def setSessionId(_sessid):
    global sessid
    sessid = _sessid

def runCommand(args):
    global sessid
    if len(args) == 0:
        return
    if isNonNegativeInteger(args[0]):
        sessid = int(args[0])
        args = args[1:]

    if len(args) == 0:
        return

    cmdname = args[0]
    if cmdname == "help":
        if len(args) > 1:
            commandHelp(args[1])
        else:
            commandHelp("commands")
            print(" Type 'help (command)' to get more information about a command.")
    elif cmdname in commands:
        try:
            cmd = commands[cmdname]
            cmdargs = cmd.args
            Arguments = namedtuple('Arguments', cmdargs)
            arglist = [None] * len(cmdargs)
            if len(cmdargs) > 0 and len(args) == 1:
                # prompt for each argument.
                for i, argname in enumerate(cmdargs):
                    print(argname + ": ", end="")
                    arglist[i] = input().strip()
            else:
                for i in range(min(len(cmdargs), len(args) - 1)):
                    arglist[i] = args[i+1]
            namedargs = Arguments(*arglist)
            commands[cmdname].f(namedargs, sessid=sessid)
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
        command = commands[name]
        print(" %s: %s\n %s" % (name, (" ").join(command.args), command.help))
    else:
        print(" Unknown Command: '%s'" % name)

if __name__ == "__main__":
    def greet(args, sessid=0):
        name = args.name or "there"
        if len(args) > 0:
            name = args[0]
        print("Hello, %s." % name)
    addCommand("greet name", greet, "Greet someone")
    evalLoop()

