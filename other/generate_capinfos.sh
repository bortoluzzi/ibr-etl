#!/bin/bash

mkdir -p capinfos

echo "capinfos start"
	echo "generating capinfos from pcaps in capinfos/*"
for f in *.pcap.gz
do
    echo "Processing ${f}"
	capinfos ${f} > "capinfos/${f}.capinfos.txt"
done
echo "capinfos end"
