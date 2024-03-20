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
unique_ipsrc=[]
unique_ipsrc_enriched_output=[]
unique_ipdst=[]
unique_ipdst_enriched_output=[]
cachesrc={}
cachedst={}
cachesrchit=0
cachesrcmiss=0
cachedsthit=0
cachedstmiss=0
#cacheglobalcounter=0
cacheinfo=open("cacheinfo.txt","w")
anomalous_entries=open("enrich_tshark_anomalous_entries.csv","w")
trimmed_entries=open("trimmed_entries.csv","w")

for rawline in sys.stdin:
    # cacheglobalcounter+=1
    # if cacheglobalcounter > 250000:
    #     cachesrc.clear()
    #     cachedst.clear()
    #     cacheglobalcounter=0

    line=rawline.rstrip()
    line=line.split(',')
    if len(line) == 6:
        timestamp=str(line[0])
        ipsrc=str(line[1])
        ipdst=str(line[2])
        tcpdstport=str(line[3])
        udpdstport=str(line[4])
        icmptype=str(line[5])

        if not ipsrc in cachesrc.keys():
            cachesrcmiss+=1
            try:
                geoip_source = solver.city(ipsrc)
            except:
                cachesrc[ipsrc] = {}
                cachesrc[ipsrc]['iso_code'] = "ZZ" #6
                cachesrc[ipsrc]['country_name'] = "ZZ Country" #7
                cachesrc[ipsrc]['city_name'] = "Unknown" #8
                cachesrc[ipsrc]['latitude'] = "-99" #9 
                cachesrc[ipsrc]['longitude'] = "-99" #10
            else:
                cachesrc[ipsrc] = {}
                cachesrc[ipsrc]['iso_code'] = str(geoip_source.country.iso_code)#6
                cachesrc[ipsrc]['country_name'] = str(geoip_source.country.name)#7
                if geoip_source.city.name:
                    cachesrc[ipsrc]['city_name'] = str(geoip_source.city.name)
                    cachesrc[ipsrc]['city_name'] = cachesrc[ipsrc]['city_name'].replace("'"," ")#8
                else:
                    cachesrc[ipsrc]['city_name'] = 'Unknown'#8
                cachesrc[ipsrc]['latitude'] = str(geoip_source.location.latitude)#9
                cachesrc[ipsrc]['longitude'] = str(geoip_source.location.longitude)#10
        else:
            cachesrchit+=1

        line.append(cachesrc[ipsrc]['iso_code']) #6
        source_country_iso_code=cachesrc[ipsrc]['iso_code']#6
        line.append(cachesrc[ipsrc]['country_name'])#7
        source_country_name=cachesrc[ipsrc]['country_name']#7
        line.append(cachesrc[ipsrc]['city_name'])#8
        source_city_name=str(cachesrc[ipsrc]['city_name'])#8
        line.append(cachesrc[ipsrc]['latitude'])#9
        source_latitude=cachesrc[ipsrc]['latitude']#9
        line.append(cachesrc[ipsrc]['longitude'])#10
        source_longitude=cachesrc[ipsrc]['longitude']#10

        if not ipdst in cachedst.keys():
            cachedstmiss+=1
            try:
                geoip_destination = solver.city(ipdst)
            except:
                cachedst[ipdst] = {}
                cachedst[ipdst]['iso_code'] = "ZZ" #11
                cachedst[ipdst]['country_name'] = "ZZ Country" #12
                cachedst[ipdst]['city_name'] = "Unknown" #13
                cachedst[ipdst]['latitude'] = "-9999" #14
                cachedst[ipdst]['longitude'] = "-9999" #15
            else:
                cachedst[ipdst] = {}
                cachedst[ipdst]['iso_code'] = str(geoip_destination.country.iso_code)#11
                cachedst[ipdst]['country_name'] = str(geoip_destination.country.name)#12
                if geoip_destination.city.name:
                    cachedst[ipdst]['city_name'] = str(geoip_destination.city.name)
                    cachedst[ipdst]['city_name'] = cachedst[ipdst]['city_name'].replace("'"," ")#13
                else:
                    cachedst[ipdst]['city_name'] = 'Unknown'#13
                cachedst[ipdst]['latitude'] = str(geoip_destination.location.latitude)#14
                cachedst[ipdst]['longitude'] = str(geoip_destination.location.longitude)#15
                try:
                    aws_response = aws_ip_ranges.get(ipdst)
                    cachedst[ipdst]['region'] = str(aws_response.region)
                except:
                    cachedst[ipdst]['region'] = "Unknown" #16

        else:
            cachedsthit+=1
                
        line.append(cachedst[ipdst]['iso_code']) #11
        aws_country_code=cachedst[ipdst]['iso_code'] #11
        line.append(cachedst[ipdst]['country_name']) #12
        aws_country_name=cachedst[ipdst]['country_name'] #12
        line.append(cachedst[ipdst]['city_name']) #13
        aws_city_name=cachedst[ipdst]['city_name']#13
        line.append(cachedst[ipdst]['latitude']) #14
        aws_latitude=cachedst[ipdst]['latitude'] #14
        line.append(cachedst[ipdst]['longitude']) #15
        aws_longitude=cachedst[ipdst]['longitude'] #15
        line.append(cachedst[ipdst]['region']) #16
        aws_region=cachedst[ipdst]['region'] #16


        #generate list of unique source and destination IPs
        # You can comment if not using Neo4j for graph-based analysis
        # if not ipsrc in unique_ipsrc:
        #     unique_ipsrc.append(ipsrc)
        #     enriched_source=ipsrc + "," + source_country_iso_code + "," + source_country_name + "," + source_city_name + "," + source_latitude + "," + source_longitude
        #     unique_ipsrc_enriched_output.append(enriched_source)
        # if not ipdst in unique_ipdst:
        #     unique_ipdst.append(ipdst)
        #     enriched_destination=ipdst + "," + aws_country_code + "," + aws_country_name + "," + aws_city_name + "," + aws_latitude + "," + aws_longitude + "," + aws_region
        #     unique_ipdst_enriched_output.append(enriched_destination)

        # The exclusion list allows for capture trimming. The provided list works with the three first captures conducted in 2023.
        exclude=0
        exclude_timestamp_ranges=['2023-04', '2023-06', '2023-07', '2023-09-16', '2023-09-17', '2023-09-18', '2023-09-19', '2023-09-20', '2023-09-30' , '2024-03']
        for range in exclude_timestamp_ranges:
            if range in timestamp:
                exclude=1

        # Leave a break line above to exit the if condition
        output=timestamp + "," + ipsrc + "," + ipdst + "," + tcpdstport + "," + udpdstport + "," + icmptype + "," + source_country_iso_code + "," + source_country_name + "," + source_city_name + "," + source_latitude + "," + source_longitude + "," + aws_country_code + "," + aws_country_name + "," + aws_city_name + "," + aws_latitude + "," + aws_longitude + "," + aws_region
        if exclude == 0:
            print(output)
        else:
            trimmed_entries.write(output + "\n")
    else:
        anomalous_entries.write(rawline)

solver.close()
anomalous_entries.close()
trimmed_entries.close()

# for ip in unique_ipsrc_enriched_output:
#     ipsrcfile.write(ip)
#     ipsrcfile.write("\n")

# for ip in unique_ipdst_enriched_output:
#     ipdstfile.write(ip)
#     ipdstfile.write("\n")

# ipsrcfile.close()
# ipdstfile.close()

cacheinfo.write("Source IP stats" + "" + "\n")
cacheinfo.write("Source IP addresses cached: " + str(len(cachesrc)) + "\n")
cacheinfo.write("Source IP cache hit: " + str(cachesrchit) + "\n")
cacheinfo.write("Source IP cache miss: " + str(cachesrcmiss) + "\n")
cacheinfo.write("\n")
cacheinfo.write("AWS IP stats" + "" + "\n")
cacheinfo.write("AWS IP addresses cached: " + str(len(cachedst)) + "\n")
cacheinfo.write("AWS IP cache hit: " + str(cachedsthit) + "\n")
cacheinfo.write("AWS IP cache miss: " + str(cachedstmiss) + "\n")
cacheinfo.write("\n")
cacheinfo.close()