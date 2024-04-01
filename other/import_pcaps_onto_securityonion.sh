#!/bin/bash

echo "Run this as root due to so-import-pcap and sudo timeouts"

for file in *.pcap.gz
do
    basename="${file%%.*}"
    echo "Decompressing ${file} into ${basename}.pcap"
    zcat ${file} > ${basename}.pcap
    echo "Importing ${basename}.pcap"
    so-import-pcap ${basename}.pcap > ${basename}.so.pcap.txt
    rm ${basename}.pcap
done
