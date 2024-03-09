#!/bin/bash

echo "capinfos start"
for f in ../*.pcap.gz
do
	echo "generating capinfos from pcaps in parent directory"
	capinfos ${f} > '${f}.capinfos.txt'
done
echo "capinfos end"
