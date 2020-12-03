
# load 
from util import randstr
from hash import hash
from passwords import rare
import data

data.loadAll()
#data.saveAll()

userid = None

# Please see README.md for definitions on all the hashes and cookies, how they are computed, etc.

from cmd import addCommand, evalLoop, setPrompt

SALTLEN = 5
# Salts are secret, in order to make cracking user passwords more difficult.
# To provide the authhashes, a user must randomly guess the salts, so don't make this too long, but also not too short either.
SALTSECRET = 5

IDLEN = 10
AUTHHASHES = 10
SIGNUPFAIL = "Sorry, that password is not rare enough!"
# TODO use password dictionary
def authHashes(userid, password, n):
    result = []
    result.append(userid)
    for i in range(n):
        salt = randstr(SALTLEN)
        authcookie = hash(password + salt)
        authhash = hash(authcookie)
        publicsalt = salt[:SALTLEN-SALTSECRET]
        result.append(publicsalt)
        result.append(authhash)
    return result
    
def userSignup(args):
    # password or site-precookie
    # password is manually chosen, but site pre-cookie should be computed from hash(siteid + rootcookie)
    password = args[0]
    global userid
    salt = randstr(SALTLEN)
    passwordhash = hash(password)
    # always compute checks to prevent timing attacks,
    # that could guess if password is in use.
    not_new = passwordhash in data.salts
    not_rare = not rare(password)
    if not_new or not_rare:
        print(SIGNUPFAIL)
        return
    username = ""
    email = ""
    userid = randstr(IDLEN)
    while(userid in data.users): #theoretically this could infinite loop, but when are we gonna have that many users?
        userid = randstr(IDLEN)

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

    sitecookie = hash(password + salt) # store this entire salt, because it is strictly private on the server.

    data.authhashes.addRow(*authHashes(userid, password, AUTHHASHES))
    data.authhashes.save()
    data.cookies.addRow(sitecookie, userid, salt)
    data.cookies.save()
    data.salts.addRow(passwordhash, salt)
    data.salts.save()
    data.users.addRow(userid, username, email, sitecookie)
    data.users.save()

    if len(username):
        data.names.addRow(username, userid)
        data.names.save()
    if len(email):
        data.emails.addRow(email, userid, False)
        data.emails.save()
    print(f" New user created.")
    print(f" User Id: '{userid}'")
    print(f" SiteCookie: '{sitecookie}'")
    name = username
    if len(name) == 0:
        name = userid
    setPrompt(f"{name} @ cookiejar> ")



def userLoginPassword(args):
    password = args[0]
    passwordhash = hash(password)
    if not passwordhash in data.salts:
        print("Unknown user password.")
        return
    salt = data.salts[passwordhash][1]
    cookie = hash(password + salt)
    # print("salt", salt)
    # print("cookie", cookie)
    userLoginCookie([cookie])

def userLoginCookie(args):
    cookie = args[0]
    if not (cookie in data.cookies):
        print("Unknown user.")
        # print("cookie: ", cookie)
        # print("cookies: ", str(data.cookies))
        return
    global userid
    userid = data.cookies[cookie][1]
    name = data.users[userid][1]
    if len(name) == 0:
        name = userid
    setPrompt(f"{name} @ cookiejar> ")


def whoami(args):
    global userid
    if userid == None:
        print(" Not logged in.")
    else:
        user = data.users[userid]
        print(f" SiteCookie: '{user[3]}'")
        if len(user[1]):
            print(f" User Id: '{user[0]}'")
        if len(user[1]):
            print(f" Username: '{user[1]}'")
        if len(user[2]):
            print(f" Email: '{user[2]}'")


def userLogout(args):
    global userid
    userid = None
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

def showMessages():
    print("TODO")

def connectPeer():
    print("TODO")
        
def disconnectPeer():
    print("TODO")

def acceptPeer():
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
        ["login", userLoginPassword, "login (password) - Log in using your password (recommended to use cookie instead)."],
        ["cookie", userLoginCookie, "cookie (cookie) - Log in using your cookie."],
        ["messages", showMessages, "mssages - show messages, such as peer connect requests, payment or invoice requests, cashed check notifications."],
        ["logout", userLogout, "logout"],
        ["mint", mintCoin, "mint (name) [supply] - mints an amount of a coin if possible (ie you are the issuer and it is not locked)."],
        ["connect", connectPeer, "connect (peer) - request to connect to a peer, or accept a request to connect. Peers can invoice each other(an invoice must be accepted to initiate payment)."],
        ["disconnect", disconnectPeer, "disconnect (peer)"],
        # TODO: do we want to allow arbitrary messaging? ["say", speakPeer, "say (peer) (message)"],
        # no rejecting ["reject", rejectPeer, "reject (peer) [invoice] - reject an outstanding"],
        ["pay", payPeer, "pay (peer) (currency) (amount)"],
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

    evalLoop()
    # evalLoop(after=lambda x: data.saveAll())

