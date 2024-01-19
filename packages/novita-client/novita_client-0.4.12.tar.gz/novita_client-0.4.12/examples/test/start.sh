#!/bin/bash

/usr/sbin/sshd &
/usr/local/bin/npipe p -s kcp://k8s-npipe-npiperel-0d8d225ac0-0ec90ff4d05a715d.elb.ap-southeast-1.amazonaws.com:7184 -n huggingface-001 &

python app.py 