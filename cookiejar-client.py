
import os
from collections import namedtuple
from table import Table
from cmd import addCommand, evalLoop, setPrompt
from util import randstr

Site = namedtuple("site", "alias siteid url")
Root = namedtuple("root", "alias url")


CLIENT = "client"

if not os.path.exists(CLIENT):
    os.makedirs(CLIENT)

SITES = os.path.join(CLIENT, "sites.csv")
ROOTS = os.path.join(CLIENT, "roots.csv")
ROOTS = os.path.join(CLIENT, "roots.csv")

ROOTCOOKIELEN = 20

def newRoot(args):
    rootcookie = randstr(ROOTCOOKIELEN)
    print("root-cookie: " + rootcookie)
    print("TODO save")


def setRoot(args):
    print("TODO")

def selectRoot(args):
    print("TODO")

def addSite(args):
    print("TODO")

def listsites(args):
    print("TODO")

def siteCookie(args):
    print("TODO")

def sitePreCookie(args):
    print("TODO")

def backupSecret(args):
    print("TODO")

def authHash(args):
    print("TODO")

def encryptStore(args):
    print("TODO")

def loadStore(args):
    print("TODO")


# TODO standalone client commands
# newroot
# setroot
# addsite (site-id) [alias] [site-url]
#  Note: all further commands require the client's rootcookie to be set.
# sitecookie (siteid or alias)
# siteprecookie (siteid or alias) -- only used the first time you connect to a new service
# authhash (siteid or alias) (salt-_n) (siteid or alias)  -- prompts to mark the authhash as used.
# backupsecret -- (backup-version-id) (
#  Save/Load:
# encryptstore -- (key) encrypts and writes the current client state to a datastore 
# loadstore -- (key) loads an encrypted datastore.


if __name__ == "__main__":
    commands = [
        # ["loadbackup", loadBackupData, "loads a backup into a new subspace"],
        ["new", newRoot, "new [alias] - randomly generates a new rootcookie."],
        ["set", setRoot, "set (token) [alias] - sets the root cookie to the specified token."],
        ["select", selectRoot, "select (root-coookie-id alias) - select the alias as the active rootcookie."],
        ["addsite", addSite, "addsite [alias] - randomly generates a new rootcookie."],
        ["listsites", listsites, "listsite [aliasprefix] - list all site aliases starting with the prefix."],
        ["sitecookie", siteCookie, "sitecookie (site-id or alias)"],
        ["precookie", sitePreCookie, "precookie (site-id or alias)"],
        ["backupsecret", backupSecret, "backupsecret (site-id or alias) (backup-version-id)"],
        ["authhash", authHash, "authhash (site-id or alias) (salt-_n)"],
        ["encryptstore", encryptStore, "encryptstore (key) - encrypts and writes client state"],
        ["loadstore", loadStore, "loadstore (key) - loads an encrypted datastore."],
    ]
    setPrompt("cookiejar client> ")
    for command in commands:
        addCommand(*command)

    evalLoop()

