#!/usr/bin/bash

mkdir archive
mv public/ archive/
mv private/ archive/

script -c "python cookiejar.py" /tmp/testoutput.log << EOF
 1 signup peanutnutter carver
 1 login peanutnutter
EOF

cat /tmp/testoutput.log
