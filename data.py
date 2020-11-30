
from collections import namedtuple
import os
import csv
from table import Table

# TODO set update interval for all public files
PUBLIC = "public"
PRIVATE = "private"
BACKUP = "backup" # this is the actual public folder for backups

if not os.path.exists(PUBLIC):
    os.makedirs(PUBLIC)

if not os.path.exists(PRIVATE):
    os.makedirs(PRIVATE)

if not os.path.exists(BACKUP):
    os.makedirs(BACKUP)


   
# TODO handle claiming accounts


USERS = os.path.join(PRIVATE, "users.csv")
NAMES = os.path.join(PRIVATE, "names.csv")
EMAILS = os.path.join(PRIVATE, "emails.csv")
PRIVACCTS = os.path.join(PRIVATE, "privaccts.csv")
NAMESPACES = os.path.join(PUBLIC, "namespaces.csv")
HOSTS = os.path.join(PUBLIC, "hosts.csv")
CURRENCIES = os.path.join(PUBLIC, "currencies.csv")
AUTH_HASHES = os.path.join(PUBLIC, "auth-hashes.csv")
CHECKS = os.path.join(PUBLIC, "checks.csv")
PUBACCTS = os.path.join(PUBLIC, "pub-accounts.csv")
BACKUPS = os.path.join(PUBLIC, "backups.csv")

User = namedtuple("User", "UserId SiteCookie")
Name = namedtuple("Name", "UserName UserId")
Email = namedtuple("Email", "Email UserId")
PrivAcct = namedtuple("PrivAcct", "UserIdCurrencyId Amount")
Namespace = namedtuple("Namespace", "NamespaceName AuthorityUrl")
Host = namedtuple("Host", "HostName Url SiteId")
Currency = namedtuple("Currency", "CurrencyId Namespace Name Issuer Supply")
AuthHash = namedtuple("AuthHash", "CurrencyId Namespace Name Issuer Supply")
Check = namedtuple("Check", "CheckHash CurrencyId Amount")
PubAcct = namedtuple("PubAcct", "AcctId AcctHash CurrencyId Balance")
Backup = namedtuple("Backup", "TableName BackupVersion Datetime")


users = Table(User, USERS)
names = Table(Name, NAMES)
emails = Table(Email, EMAILS)
privaccts = Table(PrivAcct, PRIVACCTS)
namespaces = Table(Namespace, NAMESPACES)
hosts = Table(Host, HOSTS)
currencies = Table(Currency, CURRENCIES)
authhashes = Table(AuthHash, AUTH_HASHES)
checks = Table(Check, CHECKS)
pubaccts = Table(PubAcct, PUBACCTS)
backups = Table(Backup, BACKUPS)

# this publishes the table, increments the version number, etc.
def publishBackup(tablename):
    # copy the public table to the web servered backup directory, prepending the version number.
    pass
 
def saveAll():
    users.save()
    names.save()
    emails.save()
    privaccts.save()
    namespaces.save()
    hosts.save()
    currencies.save()
    authhashes.save()
    checks.save()
    pubaccts.save()
    backups.save()

def loadAll():
    users.load()
    names.load()
    emails.load()
    privaccts.load()
    namespaces.load()
    hosts.load()
    currencies.load()
    authhashes.load()
    checks.load()
    pubaccts.load()
    backups.load()

