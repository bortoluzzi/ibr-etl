#!/bin/bash

sum=0

for file in *.txt; do
	count=$(cat $file | grep "Number of packets" | tail -n 1 | awk '{print $NF}')
	echo "file $file contains $count packets"
	sum=$(expr $sum + $count)
done

echo -e
echo "Total packet count:"
echo $sum
