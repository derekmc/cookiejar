# load
from collections import namedtuple
from util import randstr
from hash import hash
from passwords import rare
import data

# whether the service is multiplexed through an intermediate interface(ie a webserver),
# allowing different actions from different users to be invoked over the same connection,
# the user session is indicated with a "sessid", an integer that comes before the command.
# 0 is always a guest session / publicly available calls.
ALLOWUSERPASSWORDS = False
MULTIUSER = True
NAMESPACE = "test"


data.loadAll()
data.saveAll()

__userid = None # only use this if MULTIUSER is False
#sessionid = None
# Sessions do no persist when this is restarted, only data.py csv tables persist.
__sessions = {}  # sessid -> userid


# Please see README.md for definitions on all the hashes and cookies, how they are computed, etc.

from cmd import addCommand, evalLoop, setPrompt, setSessionId

SALTLEN = 5
# Salts are secret, in order to make cracking user passwords more difficult.
# To provide the authhashes, a user must randomly guess the salts, so don't make this too long, but also not too short either.
SALTSECRET = 5
AUTOPASSLEN = 3
#AUTOPASSLEN = 23 

IDLEN = 10
AUTHHASHES = 10
SIGNUPFAIL = "Sorry, that password is not rare enough!"

    
def getUser(sessid=0):
    if not MULTIUSER and sessid > 0:
        raise ValueError("Multiuser not enabled, sessid > 0 not allowed.")
    if MULTIUSER:
        if sessid == 0:
            return None
        global __sessions
        userid = __sessions.get(sessid)
        if userid == None:
            __sessions[sessid] = None
            return None
        return userid
    else:
        return __userid
 
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
    
def autoSignup(args, sessid=0):
    password = randstr(AUTOPASSLEN)
    passwordhash = hash(password)
    while(passwordhash in data.salts): #theoretically this could infinite loop, but when are we gonna have that many users?
        password = randstr(AUTOPASSLEN)
        passwordhash = hash(password)
    SignupArguments = namedtuple('Arguments', "username password email")
    signupargs = SignupArguments(args.username, password, args.email)
    userSignup(signupargs, sessid)
    print(" Password: " + password)

def forbidManualSignup(args, sessid=0):
    print(" Manual password selection disabled. Use 'autosignup' instead.")
    return

def userSignup(args, sessid=0):
    # password or site-precookie
    # password is manually chosen, but site pre-cookie should be computed from hash(siteid + rootcookie)
    if not MULTIUSER and sessid > 0:
        raise ValueError("Multiuser not enabled, sessid > 0 not allowed.")

    password = args.password
    # global userid
    salt = randstr(SALTLEN)
    passwordhash = hash(password)
    # always compute checks to prevent timing attacks,
    # that could guess if password is in use.
    not_new = passwordhash in data.salts
    not_rare = ALLOWUSERPASSWORDS and not rare(password)
    if not_new or not_rare:
        raise ValueError(SIGNUPFAIL)
        return

    userid = randstr(IDLEN)
    while(userid in data.users): #theoretically this could infinite loop, but when are we gonna have that many users?
        userid = randstr(IDLEN)

    username = args.username or ""
    email = args.email or ""

    if username in data.names:
        raise ValueError("Sorry, that username is taken.")
        return

    if email in data.emails:
        raise ValueError("Sorry, that email address is taken.")

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
    # setPrompt(f"{name} @ cookiejar> ")



def userLoginPassword(args, sessid=0):
    if not MULTIUSER and sessid > 0:
        raise ValueError("Multiuser not enabled, sessid > 0 not allowed.")
    password = args.password
    passwordhash = hash(password)
    if not passwordhash in data.salts:
        print("Unknown user password.")
        return
    salt = data.salts[passwordhash][1]
    cookie = hash(password + salt)
    # print("salt", salt)
    # print("cookie", cookie)
    CookieArguments = namedtuple('Arguments', "cookie")
    cookieargs = CookieArguments(cookie)
    userLoginCookie(cookieargs, sessid)

def userLoginCookie(args, sessid=0):
    if not MULTIUSER and sessid > 0:
        raise ValueError("Multiuser not enabled, sessid > 0 not allowed.")
    cookie = args.cookie
    if not (cookie in data.cookies):
        print("Unknown user.")
        # print("cookie: ", cookie)
        # print("cookies: ", str(data.cookies))
        return
    userid = data.cookies[cookie][1]
    name = data.users[userid][1]
    if len(name) == 0:
        name = userid

    if MULTIUSER:
        global __sessions
        if sessid == 0:
            # find an unused sessid.
            sessid = 1
            while(sessid in __sessions):
                sessid += 1
            setSessionId(sessid)
            #raise ValueError("Multiuser is enabled, and this action requires a non-zero sessid.")
        __sessions[sessid] = userid
    else:
        global __userid
        __userid = userid
        setPrompt(f"{name} @ cookiejar> ")


def whoami(args, sessid=0):
    userid = getUser(sessid)
    if userid == None:
        print(" Not logged in.")
    else:
        user = data.users[userid]
        print(f" SiteCookie: '{user[3]}'")
        if len(user[0]):
            print(f" User Id: '{user[0]}'")
        if len(user[1]):
            print(f" Username: '{user[1]}'")
        if len(user[2]):
            print(f" Email: '{user[2]}'")


def userLogout(args, sessid=0):
    userid = getUser(sessid)

    if MULTIUSER:
        del __sessions[sessid]
    else:
        global __userid
        setPrompt("cookiejar> ")
        __userid = None

    print(" User logged out.")
   

def mintCoin(args, sessid=0):
    userid = getUser(sessid)

    # anonymously issued coins are all deposited into a bearer check.
    name = args.coinname
    namespace = NAMESPACE
    supply = int(args.supply)
    issuer = userid

    anonymous = (userid == None)
    locked = True if anonymous else False # anonymously created currencies must be locked.

    lookup = name + ":" + namespace
    if anonymous:
        print("TODO: issue check for supply of anonymous currency.");
        pass #TODO anonymously created currencies have all their balance put into one check.
    elif lookup in data.currencylookup:
        currencyid = randstr(IDLEN)
        while(currencyid in data.currencies): #theoretically this could infinite loop, but when are we gonna have that many users?
            currencyid = randstr(IDLEN)

        #TODO allow issuers to issue more.
        raise ValueError("That currency already exists")
    else:
        data.currencies.addRow(currencyid, NAMESPACE, name, issuer, supply, locked)
        data.currencylookup.addRow(lookup, currencyid)

        user = data.users[userid]
        sitecookie = user[3]
        sitepostcookie = hash(sitecookie)
        # TODO obfuscate pubaccts
        # compute pubacct info
        acctid = randstr(IDLEN)
        while(acctid in data.pubaccts): #theoretically this could infinite loop, but when are we gonna have that many users?
            acctid = randstr(IDLEN)

        acctversion = randstr(IDLEN)
        # for when you update an account, do this.
        # while(acctversion == data.pubaccts[acctid]): # it should be okay, if the account version conflicts with a previous version, as it exists primarily, to make it difficult to track a specific account history, as account versions exist primarily to mitigate against potential replay attacks.
        #   acctversion = randstr(IDLEN)

        data.privaccts.addRow(userid + ":" + currencyid, acctid)

        acctsecret = hash(acctid + ":" + acctversion + ":" + sitepostcookie)
        accthash = hash(acctid + ":" + userid + ":" + acctsecret)
        data.pubaccts.addRow(acctid, acctversion, accthash, currencyid, supply)

        print(f"Minted {supply} units of currency {lookup} to \"{user[1]}\"({userid})")

    data.pubaccts.save()
    data.privaccts.save()
    data.currencies.save()
    data.currencylookup.save()

def setNamespace(args, sessid=0):
    global NAMESPACE
    NAMESPACE = args.namespace
    setPrompt(f"cookiejar @{NAMESPACE} > ")

def showMessages(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def connectPeer(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")
        
def disconnectPeer(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def acceptPeer(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")
    
        
def payPeer(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")
        
def invoicePeer(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")
        

# TODO none of these commands should run until the user has specified their cookie.
def issueCurrency(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

# Issues a new check
def createCheck(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

# Accept a check
def acceptCheck(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def splitCheck(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def joinCheck(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")
    
def showSupply(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def showAccount(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

# returns the anonymized backup for all data.
def backupData(args, sessid=0):
    # userid = getUser(sessid)
    print("TODO")

def showSiteId(args, sessid=0):
    #userid = getUser(sessid)
    host = data.host
    hostname = list(host.keys())[0]
    siteid = host[hostname].SiteId
    print(" Site Id: %s" % siteid)

def connectContractor(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def connectClientPeer(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def listTransactions(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

def claimBackup(args, sessid=0):
    userid = getUser(sessid)
    print("TODO")

# whenver history is enabled, this fact is reminded to the user after they login and after every command.
def enableHistory(args, sessid=0):
    print("TODO")

# clears the users transaction history and disables recording history.
def disableHistory(args, sessid=0):
    print("TODO")
    

if __name__ == "__main__":
    commands = [
        ["id", showSiteId, "show the 'Site Id' which serves as a salt for generating the 'user cookie' and other data."],
        ["autosignup username email", autoSignup, "Signup with an autogenerated password."],
        ["signup username password email" if ALLOWUSERPASSWORDS else "signup",
           userSignup if ALLOWUSERPASSWORDS else forbidManualSignup,
           "Create an account. Note: password must be unique and cannot be changed."],
        ["autosignup username email", autoSignup, "Create an account. Automatically generate the password."],
        ["whoami", whoami, "display info on the logged in user."],
        ["cookie cookie", userLoginCookie, "Login using your cookie."],
        ["login password", userLoginPassword, "Login using your password (recommended to use cookie instead)."],
        ["messages", showMessages, "mssages - show messages, such as peer connect requests, payment or invoice requests, cashed check notifications."],
        ["logout", userLogout, "logout"],
        ["mint coinname supply", mintCoin, "mints an amount of a coin if possible (ie you are the issuer and it is not locked)."],
        ["namespace namespace", setNamespace, "sets the global sitewide namespace, for all coins and currencies."]
        #["contractor peername", connectContractor, "connect to a contractor so they can invoice you."],
        #["client peername", connectClientPeer, "connect to a client peer so they can pay you."],
        #["disconnect peername", disconnectPeer, "disconnect from a peer"],
        #["transactions", listTransactions, "transactions - list pending transactions, invoices and unreceived payments."],
        ## TODO: do we want to allow arbitrary messaging? ["say", speakPeer, "say (peer) (message)"],
        ## no rejecting ["reject", rejectPeer, "reject (peer) [invoice] - reject an outstanding"],
        #["pay peername", payPeer, "pay (peer) (currency) (amount) [message]"],
        #["invoice peername", invoicePeer, "invoice (peer) (currency) (amount) [message]"],
        #["check", createCheck, "check (name) (amount) [message] -> checkid. Creates a check for amount specified."],
        #["accept", acceptCheck, "accept (checkid) | accept (transactionid)"],
        #["split", splitCheck, "split (checkid) (amount...) - Split a check into n smaller checks."],
        #["join", joinCheck, "join (checkid) (checkid) - Join two or more checks into 1 large check."],
        #["supply", showSupply, "show the supply of all currencies"],
        #["account", showAccount, "show all your account balances"],
        #["backup", backupData, "get all the 'backup' hash fields"],
        #["claim", claimBackup, "claim backed up accounts"],
        # ["loadbackup", loadBackupData, "loads a backup into a new subspace"],
    ]

    setPrompt(f"cookiejar @{NAMESPACE} > ")

    for command in commands:
        addCommand(*command)

    evalLoop()
    # evalLoop(after=lambda x: data.saveAll())

