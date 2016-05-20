#! /bin/bash

for i in 0 1 `seq 3 36`
do
    ssh "cms$i" "pkill -9 -U ald77"
done
