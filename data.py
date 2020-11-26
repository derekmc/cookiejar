
import pickledb
DATAFILE = "cookiejardata.txt"

# User: (id, name, sitecookie)
# UserAuthHash (n, salt, value)


# key prefixes
USER = "user:"
COIN = "coin:"
CHECK = "check:"

# list indices
USERS = "(userlist)"
COINS = "(coinlist)"
CHECKS = "(checklist)"

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

def getCheck(checkid):
    pass

def newCheck(checkid, currency, amount):
    pass



