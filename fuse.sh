#! /bin/bash

sshfs "$1:/" "/Users/adam/mnt/$1" -o IdentityFile=/Users/adam/.ssh/id_rsa -o uid=501 -o gid=20 -o follow_symlinks -o umask=0 -o reconnect -o allow_other
