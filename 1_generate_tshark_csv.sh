#!/bin/bash

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
	# -O ip,tcp,udp,icmp # Barry's advice
	# --log-level "critical" # this works in Ubuntu but not in Rocky
	time tshark -r $f -M 100000 -t ad -T fields -e _ws.col.Time -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags.str -e udp.dstport -e icmp.type -Eseparator=, --log-level "critical" | gzip -c >> output.csv.gz
done
echo "tshark end"
