#!/usr/bin/bash

mkdir archive
mv public/ archive/
mv private/ archive/

python cookiejar.py << EOF > /tmp/cookiejar-testfile
 1 signup peanutnutter carver
 1 login peanutnutter
EOF

cat /tmp/cookiejar-testfile
