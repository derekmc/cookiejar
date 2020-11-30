
# Cookie Jar
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



