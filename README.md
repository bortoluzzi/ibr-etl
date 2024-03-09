# ibr-etl
## Cloud Telescope - Internet Background Radiation - PCAP Enrichment procedure

### Requirements:
This works in Linux or Linux within WSL (Windows Subsystem for Linux)

Copy the files the directory containing all your pcap files all in a single directory.

Requirements:
- Standard unix binaries: gzip and cat.
- tshark i.e. sudo apt install tshark
- GeoIP2-City.mmdb, which can be obtained at: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
- Python 3 and the following pip packages.
    - geoip2
    - awsipranges
$ sudo apt install python3-pip
pip install geoip2 awsipranges

### Neo4J cypher syntax query generation
If you are going to play with Neo4J, then uncomment the relevant lines in 2_enrich_csv.py. 

### Working with a small sample to test everything
If you want to test the pipeline with 100 packets before running a large batch:
zcat big.pcap.gz | editcap -r - sample.pcap 1-100
gzip sample.pcap 
Ensure no big pcap exists in this test directory, otherwise it will be processed.
Test the sample:
tshark -r sample.pcap


### Quick sample ETL (Extract-Transform-Load) commands

Delete previous output.csv or output.csv.gz files in case they exist from previous processing.

1_generate_tshark_csv.sh expects to find a set of gzip compressed pcap files in the same directory. It produces a single compressed output.csv.gz as a result. Adjust accordingly.

### Sample ETL sequential commands keeping track of time on each step
time ./1_generate_tshark_csv.sh
time zcat output.csv.gz | python3 2_enrich_csv.py | gzip > output.csv.enriched.gz
time zcat output.csv.enriched.gz | python3 3_summarize_radiation.py > output.tex

### if you produced graphs in 2_enrich_csv.py:
$ zcat output_enriched.csv.gz | python 4_generate_graph.py | gzip > output.cypher.cql.gz
