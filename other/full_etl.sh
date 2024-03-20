#!/bin/bash

#Set this to the base directory containing the scripts
prefix=/home/fabricio/ibr-etl/

step0=' nohup '
step1=' ${prefix}1_generate_tshark_csv.sh &&'
step2=' zcat output.csv.gz | python3 ${prefix}2_enrich_csv.py | gzip > output.rich.csv.gz &&'
step3=' zcat output.rich.csv.gz | python3 ${prefix}3_summarize_radiation.py > output.tex '

etl=${step0} + ${step1} + ${step2} + ${step3}'

echo $etl
