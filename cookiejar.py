
datafile = "cookiejardata.txt"
from cmd import addCommand, evalLoop, setPrompt

### field, key, ...
### fields: user, currency, check, account, info

data = {}
current_user = -1


# sets the appropriate item and returns the item index.
def setitem(row):
    column = row[0]
    key = row[1]
    rest = row[2:]
    if not column in data:
        data[column] = {}
    items = data[column]
    items[key] = rest

# returns the 'nth' item.
def getitem(column, key):
    if not column in data:
        return None
    items = data[key]
    if not items:
        return None
    if not key in items:
        return None
    row = items[key]
    return [column, key] + row

# CSV single file database
def loaddb(filename):
    f = open(filename, "r")
    for line in f:
        row = line.split(", ")
        setitem(row)
        
def savedb(filename):
    f = open(filename, "w")
    for k in data:
        rows = data[k]
        for row in rows:
            f.write(k + ", " + ", ".join(row))

def userSignup(args):
    # user, name, passwd
    name = args[0]
    passwd = args[1]
    coin = ""
    uid = setitem(['user', name, passwd, coin])
    print(f" New user '{name}' successfully created.");
    return uid

def userLogin(args):
    user = args[0]
    passwd = args[1]
    #user = getitem('user', current_user)
    setPrompt(f"{user}@cookiejar> ")
    pass

def userLogout(args):
    current_user = -1
    print(" User logged out.")
    setPrompt("cookiejar> ")
    

def mintCoin(args):
    # anonymously issued coins are all deposited into a bearer check.
    name = args[0]
    supply = int(args[1])
    issuer = current_user
    locked = false if issuer >= 0 else true # anonymously created currencies must be locked.
    n = setitem(['coin', name, supply, locked])
    if locked:
        pass #TODO give check
        

# TODO none of these commands should run until the user has specified their cookie.
def issueCurrency(args):
    print("TODO")

# Issues a new check
def giveCheck(args):
    print("TODO")

# Accept a check
def takeCheck(args):
    print("TODO")

def splitCheck(args):
    print("TODO")

def joinCheck(args):
    print("TODO")
    

def showSupply(args):
    print("TODO")

def showAccount(args):
    print("TODO")

# returns the anonymized backup for all data.
def backupData(args):
    print("TODO")

def showSiteId(args):
    print("TODO")

def setUserCookie(args):
    print("TODO")


if __name__ == "__main__":
    commands = [
        ["id", showSiteId, "show the 'Site Id' which serves as a salt for generating the 'user cookie' and other data."],
        ["signup", userSignup, "signup (name) (password)"],
        ["cookie", setUserCookie, "cookie (cookie) - sets the \"User Cookie\" which should be generated from a \"User Secret\"\n UserCookie = hash(UserSecret + siteId)"],
        ["login", userLogin, "login (name) (password)"],
        ["logout", userLogout, "logout"],
        ["mint", mintCoin, "mint (name) [supply] - mints an amount of a coin if possible (ie you are the issuer and it is not locked)."],
        ["give", giveCheck, "give (name) (amount) -> checkid. Creates a check for amount specified."],
        ["take", takeCheck, "take (checkid)"],
        ["split", splitCheck, "split (checkid) (amounta) - Split a check into 2 smaller checks."],
        ["join", joinCheck, "join (checkid) (checkid) - Join two checks into 1 large check."],
        ["supply", showSupply, "show the supply of all currencies"],
        ["account", showAccount, "show all your account balances"],
        ["backup", backupData, "get all the 'backup' hash fields"],
    ]
    setPrompt("cookiejar> ")
    for command in commands:
        addCommand(*command)

    evalLoop(after=lambda x: savedb(datafile))

