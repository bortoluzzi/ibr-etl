import sys

ipsrcfile=open("enriched_source_IPs.csv","r")
ipdstfile=open("enriched_destination_IPs.csv","r")

commit_every=100

print(":begin")

commit_count=commit_every
for line in ipsrcfile:
    commit_count-=1
    if commit_count == 0:
        print(":commit")
        #print(":schema await")        
        print(":begin")
        commit_count = commit_every    
    line=line.rstrip()
    line=line.split(',')
    ipsrc=line[0]
    source_country_iso_code=line[1]
    source_country_name=line[2]
    source_city_name=line[3]
    source_latitude=line[4]
    source_longitude=line[5]
    source_name="IP_" + ipsrc.replace('.','_') #IP_10_0_0_1 - This seems to be unecessary after all
    create_node="create (" + source_name + ":Source{IP:'" + ipsrc + "', Country_ISO_Code:'" + source_country_iso_code + "', Country_Name:'" + source_country_name + "', City_Name:'" + source_city_name + "', Latitude:'" + source_latitude + "', Longitude:'" + source_longitude + "'});"
    print(create_node)

print(":commit")
print(":begin")

commit_count=commit_every
for line in ipdstfile:
    commit_count-=1
    if commit_count == 0:
        print(":commit")
        #print(":schema await")        
        print(":begin")
        commit_count = commit_every
    line=line.rstrip()
    line=line.split(',')
    ipdst=line[0]
    aws_country_code=line[1]
    aws_country_name=line[2]
    aws_city_name=line[3]
    aws_latitude=line[4]
    aws_longitude=line[5]
    aws_region=line[6]
    destination_name="IP_" + ipdst.replace('.','_') 
    create_node="create (" + destination_name + ":Destination{IP:'" + ipdst + "', Country_ISO_Code:'" + aws_country_code + "', Country_Name:'" + aws_country_name + "', City_Name:'" + aws_city_name + "', Latitude:'" + aws_latitude + "', Longitude:'" + aws_longitude + "', AWS_Region:'" + aws_region + "'});"
    print(create_node)

print(":commit")

ipsrcfile.close()
ipdstfile.close()

commit_count=commit_every
print(":begin")
for line in sys.stdin:
    commit_count-=1
    if commit_count == 0:
        print(":commit")
        #print(":schema await")        
        print(":begin")
        commit_count = commit_every
    line=line.rstrip()
    line=line.split(',')
    timestamp=line[0]
    ipsrc=line[1]
    ipdst=line[2]
    tcpdstport=line[3]
    udpdstport=line[4]
    icmptype=line[5]
    source_country_iso_code=line[6]
    source_country_name=line[7]
    source_city_name=line[8]
    source_latitude=line[9]
    source_longitude=line[10]
    aws_country_code=line[11]
    aws_country_name=line[12]
    aws_city_name=line[13]
    aws_latitude=line[14]
    aws_longitude=line[15]
    aws_region=line[16]    
    if tcpdstport:
        protocol="tcp"
        dstport=tcpdstport
    elif udpdstport:
        protocol="udp"
        dstport=udpdstport
    elif icmptype:
        protocol="icmp"
        dstport=icmptype
    else:
        protocol="unknown"
    source_name="IP_" + ipsrc.replace('.','_')
    destination_name="IP_" + ipdst.replace('.','_')
    packet_event=""
    packet_event+="match (source:Source{IP:'" + ipsrc + "'})"
    packet_event+=" match (destination:Destination{IP:'" + ipdst + "'})"
    packet_event+=" merge (source)-[:PACKET{timeStamp:'" + timestamp + "', Protocol:'" + protocol + "', Port:'" + dstport + "'}]->(destination);"
    print(packet_event)

print(":commit")