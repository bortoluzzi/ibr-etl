import sys

count_daily_events={}

for line in sys.stdin:
    line=line.rstrip()
    line=line.split(',')
    day=str(line[0])
    day=day.split()
    day=str(day[0])
    day=day.strip()
    if day in count_daily_events:
        count_daily_events[day] += 1
    else:
        count_daily_events[day] = 1

for day,events in count_daily_events.items():
    print("{},{}".format(day,events))

# This script is meant to be used with an enriched csv file.

# How to use with an entire dataset file (i.e output.rich.csv.gz)
# zcat output.rich.csv.gz | python3 daily_distribution.py > daily_distribution.csv

# How to use for an specific port of interest (You filter the port of interest first. i.e port 10000)
# The example works for TCP because TCP is the fourth field $4 on the CSV file. Adjust accordingly.
# zcat output.rich.csv.gz | awk -F',' '$4 == 10000' | python3 daily_distribution.py > daily_distribution_port_10000_tcp.csv
# Example using UDP on port 5100 (6th field)
# zcat output.rich.csv.gz | awk -F',' '$6 == 5100' | python3 daily_distribution.py > daily_distribution_port_5100_udp.csv
# Example using ICMP type 8 (7th field)
# zcat output.rich.csv.gz | awk -F',' '$7 == 8' | python3 daily_distribution.py > daily_distribution_icmp_type_8.csv
