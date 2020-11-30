
# Cookie Jar

"Cookie Jar" is a simple "semi-distributed" digital currency platform.

# Semi-Distributed

Writing a centralized currency server is a straightforward task, as it only requires what would be necessary for any other website or webservice.
Most webservices use email, usernames and passwords, although a securely generated "cookie" is generally sufficient.
This mean it can rely exclusively on "cookies" for identifying users, and doesn't directly need to use any cryptographic algorithms, only
relying on the existing security infrastructure for the web.

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


# Prototype Implementation

Priorities

 * Correct
 * Simple
 * Clear
 * Efficient

Simplicity and Clarity are prioritized over efficiency, and that's why I created a custom "CSV" table based database,
and implemented this in python, so it would be accessible to as many people as possible.

To use the prototype server, create a custom ssh user, and use the "chsh" command to change their shell to "cookiejar.py"

You may need to take additional steps to secure that user's account against escalation.

For reference, please see the following question on stack overflow:

* [How can I lock down an SSH and/or Telnet user to only run a custom shell and no other commands or programs](https://serverfault.com/questions/1043751/how-can-i-lock-down-an-ssh-and-or-telnet-user-to-only-run-a-custom-shell-and-no)

If you have comments to add on the security or administration of this prototype service, any additional answers are appreciated.

Once you have set the user'

There may also be a daemon program written to handle scheduled backups and batching of account transactions. (TODO, maybe)

# Semi-Distributed

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
 * site-pre-cookie : h(site-id + root-cookie) -- shared with 'host' only once, not stored permanently
 * site-cookie : h(site-pre-cookie)
 * site-post-cookie : h(site-cookie) -- because the site-cookie should never be shared with other hosts, this token is used instead for generating backup-secrets.
 * site-temp-cookie : an independently generated cookie token, so that clients don't have to send their site-cookie to the host every time.
 * auth-cookie-_n : h(site-cookie-pre + salt-n) -- the host generates these using site-pre-cookie, but does not store either.
 * auth-hash-_n : h(auth-cookie-_n)  -- the host both stores and shares these, along with all salt-_n's so that sites can authenticate account claims.
 * backup-secret : h(backup-version-id + site-post-cookie) -- the primary token used to claim accounts.
 * backup-hash : h(backup-secret) -> user-hash -- the backup hash is linked to a specific user by linking it to a user-hash.
 * user-hash : h(backup-version + backup-secret + user-id) -- this is used to link all backuped up accounts to a given user,
                                                           without being able to trace that link until the user claims their accounts using the backup-secret.
 * acct-hash : h(acct-id + backup-secret) -- the publicly shared token associated with every account.
 * acct:  <acct-id, acct-hash, currency-descriptor(including prime host and scope), balance>

To claim an account, or cross authenticate, the user must reveal the following to "new-host":
 * user-id (on the original "host")
 * backup-secret 
 * auth-hash-(_n)

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
