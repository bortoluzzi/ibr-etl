#!/bin/bash

if [ -f nohup.out ]; then
	rm nohup.out
fi


if [ -f output.csv.gz ]; then
	mv output.csv.gz output.csv.gz.old
fi

if [ -f output.csv ]; then
	mv output.csv.gz output.csv.old
fi

echo "tshark start"
for f in *.pcap.gz
do
	echo "extracting data from ${f}"
	time tshark -r $f -M 100000 -t ad -T fields -e _ws.col.Time -e ip.src -e ip.dst -e tcp.dstport -e udp.dstport -e icmp.type -Eseparator=, --log-level "critical" >> output.csv
done
echo "tshark end"

echo "gzipping output.csv"
gzip output.csv
echo "gzip end"
