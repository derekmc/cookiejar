
# Cookie Jar

"Cookie Jar" is a simple "semi-distributed" digital currency platform.

# Semi-Distributed

Writing a centralized currency server is a straightforward task, as it only requires what would be necessary for any other website or webservice.
Most webservices use email, usernames and passwords, although a securely generated "cookie" is always sufficient to reliably and securely
identify users, provided that a user wishes to be identified this way, and uses the same browser "client", or otherwise syncs their sessions
between browsers/clients.
Such services can rely on "cookies" as a universal method for identifying users.  Cookie Jar, similarly, doesn't require 
a public key, password, or anything else, but instead uses a "rootcookie" which is hashed with a site specific salt, to 
create a unique "sitecookie" for each particular site.

Cookie Jar doesn't directly use any cryptographic algorithms besides basic hashing, it only
relies on the existing security infrastructure for the web.

While such a service is fairly straightforward, cookiejar has an additional goal, that "backups" for the main services "database" are publicly available,
In order to anonymize data, different "records" are all linked by hashes, and a user shares the matching *pre-hash* when they want to claim 
a backed up account on a replacement host.

Semi-distributed services offer some of the pros and cons of both centralized and distributed systems.

Because the host is centralized, you can achieve quick transaction speeds and it is easy for new users to join the network,

Because the backups are shared publicly, there is a degree of censorship resistance and resiliency to service failure.

# Host Replacement

There is intentionally no set protocol for choosing or replacing hosts.  Any such protocol established a priori, would tend
to introduce vulnerabilities, and not adapt well to changing needs.

While it would be possible to establish a fixed protocol for replacing hosts, this is not recommended.  The best way,
is for someone to simply startup the replacement service, and prove themselves reliable over time.

# Reduced security infrastructure for implementers

One of the principal advantage of cookiejar, is because it simply uses standard security infastructure for the
web, it is much easier to create tools and APIs.  So tools do not have to handle things like public key
cryptography directly, they can simply rely on SSL for secure connections to a specific service provider.

This makes it easier to design, publish, update and maintain tools that interact with cookiejar.

Obviously, the drawback is that cookie jar is not fully distributed, and if a service provider needs to be
replaced, there may be uncertainty about who should replace them, and whether they can be trusted as a host,
both for service and data integrity, and uptime reliability.  The benefit is significantly reduced transaction
costs, improved speed and clearance, a diverse community of service providers and associated value networks.

Traditional banking relies on a similar model, in that banks service a specific set of customers,
often in a specific locale, and can interface with specific legal, cultural and investment needs.

Cookiejar is not well suited for high finance, but for small web-based projects like donations,
game currencies, etc. it can potentially be useful.  It is fast, easy to use, and easy to
adapt to your project needs. Most importantly, the host is intentionally replaceable, and they
make all the data necessary to replace them, ie anonymized user account and active check
information, available.



# Prototype Implementation

Priorities

 * Correct
 * Simple
 * Clear
 * Efficient

## No external dependencies

The protocol implementation intentionally uses no external dependencies.  There is a custom data storage class in
"table.py", and a custom command line parser/runner in "cmd.py".  These are both as simple as possible.

Simplicity and Clarity are prioritized over efficiency, and that's why I created a custom "CSV" table based database,
and implemented this in python, so it would be accessible to as many people as possible.

To use the prototype server, create a custom ssh user, and use the "chsh" command to change their shell to "cookiejar.py"

You may need to take additional steps to secure that user's account against escalation.

For reference, please see the following question on stack overflow:

* [How can I lock down an SSH and/or Telnet user to only run a custom shell and no other commands or programs](https://serverfault.com/questions/1043751/how-can-i-lock-down-an-ssh-and-or-telnet-user-to-only-run-a-custom-shell-and-no)

If you have comments to add on the security or administration of this prototype service, any additional answers are appreciated.

Once you have set the user'

There may also be a daemon program written to handle scheduled backups and batching of account transactions. (TODO, maybe)

## Prototype TODO

Figure out how to use the python file as a "shell" program: Do we want to bundle and/or amalgamate it into a single file?

# Client and Server Functions

please refer to cookiejar.py and cookiejar-client.py respectively to see the various server and client calls available.

# Algorithms and hashes
CookieJar is the world's first semi-distributed digital currency.
It is not a proper "crypto" currency, as it does not use cryptographic algorithms besides basic 
hashing functions, as well as established infrastructure for creating secure channels.

"Claiming" an account, requires issuing and recoginizing "cross-authenticating" tokens,
 between an original host, and a replacement host, designated 'host' and 'new-host.

In case a given replacement host does not work out, multiple "auth-hashes" are generated from distinct
salts, and associated with a specific user-id (all user ids are relative to a specific original host).
Having many differnt "auth-hashes" mitigates against replay attacks in case a replacement host's security is compromised.

To backup a server, the auth-hashes, the checks, and the account records are backed up separately.
Optionally, account records can be split into smaller sub-balances, and cycled on regularly intervals,
in "transaction pools", in order to obfuscate anonymous account balances and when transactions occur or specfic accounts.

Backing up of checks is more selective, and only shared with select peers, as only the check hash is stored to verify check
redemption.  For this reason as well, people storing money in only check form, should wait until the replacement host
has stabilized, to ensure that their check will not be lost or stolen.

Each user has a root-cookie, known only to them, and not shared with any service. From this rootcookie, various
other cookies and tokens are generated, often salting the rootcookie with a specific token or otherwise combining
it.  These tokens serve various different functions which are explained below.

The user's root-cookie is combined with a site-id to generate site-pre-cookie.
site-pre-cookie is hashed again to generate site-cookie.  Also, site-cookie-pre
is combined with various salt-_n's to generate auth-cookie-_n and auth-hash-_n.

For any given account, on any given host, several auth-hash-_n's are shared, which is designed
to prevent replay attacks, if a user authenticates with a 'new-host', but then deems to authenticate
with another 'new-host' instead.  The highest numbered auth-hash-_n always takes precedent.

All of the following tokens play some specific role in cross authentication... it may look complicated,
but it is easier than trying to maintain the necessary secure update infastructure for potentially 
constantly evolving  public-key algorithms. Also, end users only have to store their 

Also, cookies are more resilient to the cryptographic "worst case" scenario, in which case, then the way backups
are stored will have to be adjusted, and you simply negotiate a different mutually shared secret with all the backups.
Thus, cookiejar can be redesigned to work 100%, even in a complete cryptographic apocalypse, ie all encryption fails
besides the one time pad, ie some constructable solution for P = NP is found.


 * site-id : the id of the site, which is used as a salt with the root-cookie.
 * salt-_n : Every auth-cookie requires a unique salt.
 * root-cookie : the primary secret token owned by the user, used to generate all other cookies in combination with various salts, etc.
 * site-pre-cookie : h(site-id + root-cookie) -- shared with 'host' only once, not stored permanently, interchangeable with a password.
 * password : a manually chosen host specific alternative to pre-cookies
 * site-cookie : h(site-pre-cookie or password)
 * site-post-cookie : h(site-cookie) -- because the site-cookie should never be shared with other hosts, this token is used instead for generating backup-secrets.
 * site-temp-cookie : an independently generated cookie token, so that clients don't have to send their site-cookie to the host every time.
 * auth-cookie-_n : h(site-cookie-pre + salt-n) -- the host generates these using site-pre-cookie, but does not store either.
 * auth-hash-_n : h(auth-cookie-_n)  -- the host both stores and shares these, along with all salt-_n's so that sites can authenticate account claims.

#### TODO no more "backup version" data used in hashes.
#### instead, every account has a non-linear account version to prevent replay attacks.
 * backup-secret : h(acct-id + site-post-cookie) -- the primary token used to claim accounts.
 * backup-hash : h(backup-secret) -> user-hash -- the backup hash is linked to a specific user by linking it to a user-hash.
 * user-hash : h(backup-version + backup-secret + user-id) -- this is used to link all backuped up accounts to a given user,
                                                           without being able to trace that link until the user claims their accounts using the backup-secret.

### Note: acct-id are slots which may correspond to different users over time, if accounts are obfuscated.
### So in one release, an account may correspond to one user(with the right site-post-cookie), while in another release, it may correspond to another user.
### because the username (which is collated to a user id)
 * acct-id : unique identifier for the account.  When pubaccounts are obfuscated, this is a slot only, and users balances may be moved between one or multiple slots.
 * acct-version : a randomly generated version code, must be unique per acct-id at least.
 * acct-secret : h(acct-id + acct-version + site-post-cookie)
 * acct-hash : h(acct-id + userid + acct-secret) -- the publicly shared token associated with every account. userid is included, so that authhashes can be matched and verified.
 * acct:  <acct-id, acct-hash, currency-descriptor(including prime host and scope), balance>


To claim an account, or cross authenticate, the user must reveal the following to "new-host":
 * user-id (on the original "host", in order to lookup the auth-hashes)
 * backup-secret 
 * auth-hash-(_n)

Assuming a user only keeps track of their cookie or password,
they will need to "re-discover" their userid.  This can
be done by generating their auth-hashes, to rediscover their userid.
Note that rainbow tables may be necessary to do this, as the
salts for the auth-hashes are mostly secret, in order to make
it more difficult for random attackers to attack a user's
password.  A "forgotten salt" or "half-forgotten" salt,
multiplies the effort required for both legitimate users and attackers.

# TODO, successive authhashes should use more entropy.
# Nevermind, that doesn't work, because this is a "weakest link" issue.
# maybe, successive authhashes could use **less** entropy?
# No, that also doesn't really work, because they have to be public
# for recovery purposes. That would only make sense, with timed releases.
# TODO, we should **definitely** have the option, for accounts
# secured with a public key.  No, the entire purpose of this,
# is to avoid that.  Public key based cryptos already exist, and
# you can transfer stuff to one of those.
# Cookie jar should really be for small amounts,
# like video game currencies or starbucks cards, that you
# spend or trade frequently, and might not mind losing.
# Furthermore, you only potentially lose something,
# if your auth-hashes get cracked, thereby discovering your
# password, or if you are unable to claim an account on
# a replacement host.

This also makes it more difficult for actual users to discover
the correct salt, as well as their user-id, if that information
is no longer available from the original host.
this means that the user's cookiejar-client, must use guess and check to 
the correct auth-hash, and also which accounts they own.

To claim accounts on a new service, ie cross-authenticate, a user must reveal the correct backup-secret to 'new-host',
along with some "auth-cookie" and their user-id on the original host.
Auth cookies is required, to prevent the case where a 'new-host' goes rogue, and attempts
replay attacks.  In this case, the highest indexed auth


# Cryptographic Apocalypse

Cookie-jar, because of its simplicity, is well suited for a "cryptographic apocalypse"... This would essentially be if it is discovered that P = NP, 
and specific algorithms are found to attack these problems.  Other methods for secure channels can be adopted, and cookie-jar will work with the
new infrastructure, with the simple modification that cross-authenticating cookies must be mutually negotatied, instead of computed from hashes.

Even if such an unlikely scenario never happens,  Cookie-jar's simplicity-- only relying on a single hash function and infastructure for secure channels,
will make it easy to update when new cryptographic algorithms are created.

# Crypto Concerns and Other Feedback

As a prototype, I can promise perfect security, but the basic idea is sound.  If you have any potential weaknesses or vulnerabilities,
feedback would be appreciated "derek7mc" at the email host "gmail".
