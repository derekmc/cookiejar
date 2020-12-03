
import os, csv
from collections import namedtuple
from table import Table

# TODO set update interval for all public files
PUBLIC = "public"
PRIVATE = "private"
#PROTECTED = "protected"

if not os.path.exists(PUBLIC):
    os.makedirs(PUBLIC)

if not os.path.exists(PRIVATE):
    os.makedirs(PRIVATE)

#if not os.path.exists(PROTECTED):
#    os.makedirs(PROTECTED)

   
# TODO handle claiming accounts

# Private Tables
USERS = os.path.join(PRIVATE, "users.csv")
COOKIES = os.path.join(PRIVATE, "cookies.csv")
SALTS = os.path.join(PRIVATE, "salts.csv")
NAMES = os.path.join(PRIVATE, "names.csv")
EMAILS = os.path.join(PRIVATE, "emails.csv")
PRIVACCTS = os.path.join(PRIVATE, "privaccts.csv")

# Public Tables
NAMESPACES = os.path.join(PUBLIC, "namespaces.csv")
HOSTS = os.path.join(PUBLIC, "hosts.csv")
CURRENCIES = os.path.join(PUBLIC, "currencies.csv")
AUTH_HASHES = os.path.join(PUBLIC, "auth-hashes.csv")
PUBACCTS = os.path.join(PUBLIC, "pub-accounts.csv")
CHECKS = os.path.join(PUBLIC, "checks.csv")
BACKUPS = os.path.join(PUBLIC, "backups.csv")

User = namedtuple("User", "UserId Username Email SiteCookie")
Cookie = namedtuple("Cookies", "Cookie UserId Salt")
Salt = namedtuple("Salts", "PasswordHash Salt")
Name = namedtuple("Name", "Username UserId")
Email = namedtuple("Email", "Email UserId Confirmed")
PrivAcct = namedtuple("PrivAcct", "UserIdCurrencyId Amount")
Namespace = namedtuple("Namespace", "NamespaceName AuthorityUrl")
Host = namedtuple("Host", "HostName Url SiteId")
Currency = namedtuple("Currency", "CurrencyId Namespace Name Issuer Supply")
#AuthHash = None
AuthHash = namedtuple("AuthHash", "UserId salt1 hash1 salt2 hash2 salt3 hash3 salt4 hash4 salt5 hash5 salt6 hash6 salt7 hash7 salt8 hash8 salt9 hash9 salt10 hash10")
Check = namedtuple("Check", "CheckHash CurrencyId Amount")
PubAcct = namedtuple("PubAcct", "AcctId AcctHash CurrencyId Balance")
Backup = namedtuple("Backup", "TableName BackupVersion Datetime")


users = Table(User, USERS)
cookies = Table(Cookie, COOKIES)
salts = Table(Salt, SALTS)
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
    cookies.save()
    salts.save()
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
    cookies.load()
    salts.load()
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

