#! /bin/bash

temp=$(mktemp ~/tmp.XXXXXXXXXXXX)
chmod 644 $temp
for i in `seq 0 36`
do
    ssh "cms$i" "ls /net/cms27/cms27r0 &> /dev/null && [[ \$HOSTNAME == compute* ]] && echo \"Keeping cms$i (\$HOSTNAME, \`cat /etc/redhat-release\`)\" || (echo cms$i >> $temp && echo \"Rejecting cms$i (\$HOSTNAME, \`cat /etc/redhat-release\`)\")" || (echo "cms$i" >> $temp && echo "Rejecting cms$i (could not connect)")
done
mv $temp $JOBS/skippednodes.list
