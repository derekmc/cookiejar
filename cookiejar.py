
# load 
from hash import hash
from passwords import rare
import data
data.loadAll()
data.saveAll()

sitecookie = None

# Please see README.md for definitions on all the hashes and cookies, how they are computed, etc.

from cmd import addCommand, evalLoop, setPrompt

SIGNUPFAIL = "Sorry, that password is not rare enough!"
# TODO use password dictionary
def userSignup(args):
    # password or site-precookie
    # password is manually chosen, but site pre-cookie should be computed from hash(siteid + rootcookie)
    password = args[0]
    global sitecookie
    sitecookie = hash(password)
    # always compute checks to prevent timing attacks,
    # that could guess if password is in use.
    not_new = sitecookie in data.users
    not_rare = not rare(password)
    if not_new or not_rare:
        print(SIGNUPFAIL)
        return
    username = ""
    email = ""
    if len(args) > 3:
        print("Sorry, 'signup' accepts at most 3 arguments (password) [username] [email]")
        return
    if len(args) > 1:
        username = args[1]
        if username in data.names:
            print("Sorry, that username is taken.")
            return
    if len(args) > 2:
        email = args[2]
        if email in data.emails:
            print("Sorry, that email address is taken.")
    data.users.addRow(sitecookie, username, email)
    data.users.save()
    if len(username):
        data.names.addRow(username, sitecookie)
        data.names.save()
    if len(email):
        data.emails.addRow(email, sitecookie, False)
        data.emails.save()
    print(f" New user created.");
    print(f" Please use sitecookie: '{sitecookie}'\n to login in the future.")

def whoami(args):
    if sitecookie == None:
        print(" Not logged in.")
    else:
        print(" First 4 characters of SiteCookie: %s" % str(sitecookie[:4]))
        user = data.users[sitecookie]
        if len(user[1]):
            print(" Username: %s" % user[1])
        if len(user[2]):
            print(" Email: %s" % user[2])

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

def connectPeer():
    print("TODO")
        
def disconnectPeer():
    print("TODO")
        
def payPeer():
    print("TODO")
        
def invoicePeer():
    print("TODO")
        

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

def claimBackup(args):
    print("TODO")

if __name__ == "__main__":
    commands = [
        ["id", showSiteId, "show the 'Site Id' which serves as a salt for generating the 'user cookie' and other data."],
        ["signup", userSignup, "signup (password) [username] [email]\n Note: password must be unique and cannot be changed."],
        ["whoami", whoami, "whoami - displays info on the logged in user."],
        ["cookie", setUserCookie, "cookie (cookie) - sets the \"User Cookie\" which should be generated from a \"User Secret\"\n UserCookie = hash(UserSecret + siteId)"],
        ["login", userLogin, "login (password)"],
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
        ["supply", showSupply, "show the supply of all currencies"],
        ["account", showAccount, "show all your account balances"],
        ["backup", backupData, "get all the 'backup' hash fields"],
        ["claim", claimBackup, "claim backed up accounts"],
        # ["loadbackup", loadBackupData, "loads a backup into a new subspace"],
    ]
    setPrompt("cookiejar> ")
    for command in commands:
        addCommand(*command)

    evalLoop(after=lambda x: data.saveAll())

