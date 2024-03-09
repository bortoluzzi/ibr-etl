import sys
import geoip2.database
#solver = geoip2.database.Reader('GeoLite2-City.mmdb') #FREE
solver = geoip2.database.Reader('GeoIP2-City.mmdb') #LICENSED
import awsipranges
aws_ip_ranges = awsipranges.get_ranges()

#print("timestamp,ip.src,ip.dst,tcp.dstport,udp.dstport,icmp.type,source_country_iso_code,source_country_name,source_city_name,source_latitude,source_longitude,
#aws_country_code,aws_country_name,aws_city_name,aws_latitude,aws_longitude,aws_region")

#ipsrcfile=open("enriched_unique_source_IPs.csv","w")
#ipdstfile=open("enriched_unique_destination_IPs.csv","w")
#unique_ipsrc=[]
#unique_ipsrc_enriched_output=[]
#unique_ipdst=[]
#unique_ipdst_enriched_output=[]

anomalous_entries=open("enrich_tshark_anomalous_entries.csv","w")

for rawline in sys.stdin:
    line=rawline.rstrip()
    line=line.split(',')
    if len(line) == 6:
        timestamp=str(line[0])
        ipsrc=str(line[1])
        ipdst=str(line[2])
        tcpdstport=str(line[3])
        udpdstport=str(line[4])
        icmptype=str(line[5])

        try: #enrich the source with geoip2
            geoip_source = solver.city(ipsrc)# GeoIP resolution
        except:
            line.append("Unknown") #6
            line.append("Unknown") #7
            line.append("Unknown") #8
            line.append("Unknown") #9
            line.append("Unknown") #10
        else:
            line.append(str(geoip_source.country.iso_code)) #6
            source_country_iso_code=str(line[6])
            line.append(str(geoip_source.country.name)) #7
            source_country_name=str(line[7])
            if geoip_source.city.name:
                line.append(str(geoip_source.city.name))
            else:
                line.append("Unknown")
            source_city_name=str(line[8].replace("'"," "))
            line.append(str(geoip_source.location.latitude)) #9
            source_latitude=str(line[9])
            line.append(str(geoip_source.location.longitude)) #10
            source_longitude=str(line[10])

        try: #enrich the destination with geoip2
            geoip_destination = solver.city(ipdst)# GeoIP resolution
        except:
            line.append("Unknown") #11
            line.append("Unknown") #12
            line.append("Unknown") #13
            line.append("Unknown") #14
            line.append("Unknown") #15
        else:
            line.append(str(geoip_destination.country.iso_code)) #11
            aws_country_code=str(line[11])
            line.append(str(geoip_destination.country.name)) #12
            aws_country_name=str(line[12])
            if geoip_destination.city.name:
                line.append(str(geoip_destination.city.name)) #13
            else:
                line.append("Unknown")
            aws_city_name=str(line[13].replace("'"," "))
            line.append(str(geoip_destination.location.latitude)) #14
            aws_latitude=str(line[14])

            line.append(str(geoip_destination.location.longitude)) #15
            aws_longitude=str(line[15])

            try: #enrich the destination with awsipranges
                aws_response = aws_ip_ranges.get(ipdst)
            except:
                line.append("Unknown")
            else:
                line.append(str(aws_response.region)) #16
                aws_region=str(line[16])

        #generate list of unique source and destination IPs
        # This consumes constant O(n) memory!
        # You can comment if not using Neo4j for graph-based analysis
#        if not ipsrc in unique_ipsrc:
#            unique_ipsrc.append(ipsrc)
#            enriched_source=ipsrc + "," + source_country_iso_code + "," + source_country_name + "," + source_city_name + "," + source_latitude + "," + source_longitude
#            unique_ipsrc_enriched_output.append(enriched_source)
#        if not ipdst in unique_ipdst:
#            unique_ipdst.append(ipdst)
#            enriched_destination=ipdst + "," + aws_country_code + "," + aws_country_name + "," + aws_city_name + "," + aws_latitude + "," + aws_longitude + "," + aws_region
#            unique_ipdst_enriched_output.append(enriched_destination)

        # The exclusion list allows for capture trimming. The provided list works with the three first captures conducted in 2023.
        exclude=0
        exclude_timestamp_ranges=['2023-04', '2023-06', '2023-07', '2023-09-16', '2023-09-17', '2023-09-18', '2023-09-30' , '2024-03']
        for range in exclude_timestamp_ranges:
            if range in timestamp:
                exclude=1

        # Leave a break line above to exit the if condition
        if exclude == 0:
            print(timestamp + "," + ipsrc + "," + ipdst + "," + tcpdstport + "," + udpdstport + "," + icmptype + "," + source_country_iso_code + "," + source_country_name + "," + source_city_name + "," + source_latitude + "," + source_longitude + "," + aws_country_code + "," + aws_country_name + "," + aws_city_name + "," + aws_latitude + "," + aws_longitude + "," + aws_region)
    else: #packet is anomalous (doulbe entries or currently unable to handle)
        anomalous_entries.write(rawline)

solver.close()
anomalous_entries.close()

#for ip in unique_ipsrc_enriched_output:
#    ipsrcfile.write(ip)
#    ipsrcfile.write("\n")

#for ip in unique_ipdst_enriched_output:
#    ipdstfile.write(ip)
#    ipdstfile.write("\n")

#ipsrcfile.close()
#ipdstfile.close()
