
import pickledb

DATAFILE = "cookiejardata.txt"

# key prefixes
USER = "user:"
COIN = "coin:"
CHECK = "check:"

# list indices
USERS = "(userlist)"
COINS = "(coinlist)"
CHECKS = "(checklist)"

# CookieJar is the world's first semi-distributed digital currency.
# It is not a proper "crypto" currency, as it does not use cryptographic algorithms besides basic 
# hashing functions, as well as established infrastructure for creating secure channels.
#
# "Claiming" an account, requires issuing and recoginizing "cross-authenticating" tokens,
#  between an original host, and a replacement host, designated 'host' and 'new-host.
#
# In case a given replacement host does not work out, multiple "auth-hashes" are generated from distinct
# salts, and associated with a specific user-id (all user ids are relative to a specific original host).
# Having many differnt "auth-hashes" mitigates against replay attacks in case a replacement host's security is compromised.
#
# To backup a server, the auth-hashes, the checks, and the account records are backed up separately.
# Optionally, account records can be split into smaller sub-balances, and cycled on regularly intervals,
# in "transaction pools", in order to obfuscate anonymous account balances and when transactions occur or specfic accounts.
#
# Backing up of checks is more selective, and only shared with select peers, as only the check hash is stored to verify check
# redemption.  For this reason as well, people storing money in only check form, should wait until the replacement host
# has stabilized, to ensure that their check will not be lost or stolen.
#
# Each user has a root-cookie, known only to them, and not shared with any service. From this rootcookie, various
# other cookies and tokens are generated, often salting the rootcookie with a specific token or otherwise combining
# it.  These tokens serve various different functions which are explained below.
#
# The user's root-cookie is combined with a site-id to generate site-pre-cookie.
# site-pre-cookie is hashed again to generate site-cookie.  Also, site-cookie-pre
# is combined with various salt-_n's to generate auth-cookie-_n and auth-hash-_n.
#
# For any given account, on any given host, several auth-hash-_n's are shared, which is designed
# to prevent replay attacks, if a user authenticates with a 'new-host', but then deems to authenticate
# with another 'new-host' instead.  The highest numbered auth-hash-_n always takes precedent.
# 
# All of the following tokens play some specific role in cross authentication... it may look complicated,
# but it is easier than trying to maintain the necessary secure update infastructure for potentially 
# constantly evolving  public-key algorithms. Also, end users only have to store their 
#
# Also, cookies are more resilient to the cryptographic "worst case" scenario, in which case, then the way backups
# are stored will have to be adjusted, and you simply negotiate a different mutually shared secret with all the backups.
# Thus, cookiejar can be redesigned to work 100%, even in a complete cryptographic apocalypse, ie all encryption fails
# besides the one time pad, ie some constructable solution for P = NP is found.
# 
#
# site-id : the id of the site, which is used as a salt with the root-cookie.
# salt-_n : Every auth-cookie requires a unique salt.
# root-cookie : the primary secret token owned by the user, used to generate all other cookies in combination with various salts, etc.
# site-pre-cookie : h(site-id + root-cookie) -- shared with 'host' only once, not stored permanently
# site-cookie : h(site-pre)
# site-post-cookie : h(site-cookie) -- because the site-cookie should never be shared with other hosts, this token is used instead for generating backup-secrets.
# site-temp-cookie : an independently generated cookie token, so that clients don't have to send their site-cookie to the host every time.
# auth-cookie-_n : h(site-cookie-pre + salt-n) -- the host generates these using site-pre-cookie, but does not store either.
# auth-hash-_n : h(auth-cookie-_n)  -- the host both stores and shares these, along with all salt-_n's so that sites can authenticate account claims.
# backup-secret : h(backup-version-id + site-post-cookie) -- the primary token used to claim accounts.
# backup-hash : h(backup-secret) -> user-hash -- the backup hash is linked to a specific user by linking it to a user-hash.
# user-hash : h(backup-version + backup-secret + user-id) -- this is used to link all backuped up accounts to a given user,
#                                                            without being able to trace that link until the user claims their accounts using the backup-secret.
# acct-hash : h(acct-id + backup-secret) -- the publicly shared token associated with every account.
# acct:  <acct-id, acct-hash, currency-descriptor(including prime host and scope), balance>
#
# To claim accounts on a new service, ie cross-authenticate, a user must 
# 
#
# Identifier Definitions:
# old-host-id : the id or global salt of the old host for cross authentication.
# new-host-id : the id or global salt of the old host for cross authentication.
# one-time-salt : a salt used just once for generating a specific cross authenticating token.
# 
# when a user first registers 
# the client is given a number of one-time-salts
#
# old-host-precookie = hash(old-host-id + root-user-secret) -- intermediate value, not shared with anyone
# old-host-cookie = hash(old-host-precookie)
#
# one-secret-old-host = hash(one-time-salt + old-host-precookie) -- only shared with 'new-host'
# one-cookie-old-host = hash(one-secret-old-host) -- shared with 'old-host' when the old-host-cookie is first set on the old-host.
# 
# claim-secret = hash(backup-version-id + one-cookie-old-host) -- shared with 
# claim-token = hash(new-site-id + one-claim-secret) -- old-host shares this with new-host

# one-claim-token = hash(versionid + one-claim-secret
# from-site-cookie = hash(fromsiteid + usersecret)
# one-claim-secret = hash(remoteid + sitecookie)
# one-claim-token = hash(versionid + claimsecret)
# checksum = hash(datakey + versionid + hash(versionid + secret))
# To claim 
# When users cross authenticate, they should use a client that keeps track of which "one-time-salts" have been used,
# in order to identify when a service could potentially be 
#
# The "Version ID" serves as a salt. You can create several possible independent backups at ever backup checkpoint.
# Note: if the 'fromsite' is hacked and not simply taken down,
#  the claim secret may be compromised.  In this case, 

loadData(DATAFILE)


from cmd import addCommand, evalLoop, setPrompt

### field, key, ...
### fields: user, currency, check, account, info

data = {}
current_user = -1

def getUser(name):
    pass

def getCoin(name):
    pass

def setUser(name, user):
    pass

def setCoin(name, coin):
    pass

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

def loadData(filename):
    db = pickledb.load(filename, False)
    #f = open(filename, "r")
    #for line in f:
    #    row = line.split(", ")
    #    setitem(row)
        
def saveData():
    #print(
    db.dump()

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

