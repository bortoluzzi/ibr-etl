#!/usr/bin/bash

# This file only makes sense if you want to produce individual analyses, one per cloud region.
# In that case, create one sub-directory for each region and place the compressed pcap of interest inside it.
# Example: mkdir af-south-1; mv af-south-1.pcap.gz af-south-1;
# Once that is done for all cloud regions, proceed as follows.

# This script assumes the following. Please read carefully!
# 1) Your home directory contains the ibr-data folder as fetched with "git clone https://github.com/bortoluzzi/ibr-etl"
# 2) Your home directory contains the ibr-venv folder populated as follows:
#     sudo apt install python3-full
#     python3 -m venv ~/ibr-venv
#     ~/ibr-venv/bin/python -m pip install awsipranges
#     ~/ibr-venv/bin/python -m pip install geoip2
# 3) The existence of GeoIP2-City.mmdb in each region's subdirectory (better, a symlink to it)


for d in * ; do
	if [ -d "$d" ]; then
		echo "Entering ${d}";
		cd ${d};

		echo "Step 1: Generating CSV"
		~/ibr-etl/1_generate_tshark_csv.sh

		echo "Step 2: Enriching CSV"
		zcat output.csv.gz | ~/ibr-venv/bin/python ~/ibr-etl/2_enrich_csv.py | gzip > ${d}.rich.csv.gz

		echo "Step 3: Summarising LaTeX tables"
		zcat ${d}.rich.csv.gz | ~/ibr-venv/bin/python ~/ibr-etl/3_summarize_radiation.py > ${d}.tex	

		cd ..;
		echo "Leaving ${d}";
	fi
done
