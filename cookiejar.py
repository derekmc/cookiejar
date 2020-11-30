
import pickledb

# load 
import data
data.loadAll()

# Please see README.md for definitions on all the hashes and cookies, how they are computed, etc.

from cmd import addCommand, evalLoop, setPrompt

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
def createCheck(args):
    print("TODO")

# Accept a check
def acceptCheck(args):
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
        ["connect", connectPeer, "connect (peer) ('invoice' | 'pay')"],
        ["disconnect", disconnectPeer, "disconnect (peer) ('invoice' | 'pay')"],
        ["pay", payPeer, "give (peer) (currency) (amount)"],
        ["invoice", invoicePeer, "invoice (peer) (currency) (amount)"],
        ["check", createCheck, "check (name) (amount) -> checkid. Creates a check for amount specified."],
        ["accept", acceptCheck, "take (checkid)"],
        ["split", splitCheck, "split (checkid) (amount...) - Split a check into n smaller checks."],
        ["join", joinCheck, "join (checkid) (checkid) - Join two or more checks into 1 large check."],
        ["joinsplit", joinSplitCheck, "joinsplit (checkid) (checkid...) (amount...)"],
        ["supply", showSupply, "show the supply of all currencies"],
        ["account", showAccount, "show all your account balances"],
        ["backup", backupData, "get all the 'backup' hash fields"],
        ["claim", claimBackup, "claim backed up accounts"],
        # ["loadbackup", loadBackupData, "loads a backup into a new subspace"],
    ]
    setPrompt("cookiejar> ")
    for command in commands:
        addCommand(*command)

    evalLoop(after=lambda x: savedb(datafile))

