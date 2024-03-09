#!/bin/bash

mkdir -p capinfos

echo "capinfos start"
for f in ../*.pcap.gz
do
	echo "generating capinfos from pcaps in parent directory"
	capinfos ${f} > 'capinfos/${f}.capinfos.txt'
done
echo "capinfos end"
