#!/usr/bin/python3
# coding=utf-8

import sys
import mysql.connector

host="localhost"
user=""
password=""

dataset_name="e3"
drop_database="DROP DATABASE IF EXISTS " + dataset_name
create_database="CREATE DATABASE IF NOT EXISTS " + dataset_name
#use_database="USE DATABASE " + dataset_name

create_table="CREATE TABLE IF NOT EXISTS " + dataset_name + " ("
create_table=create_table + '''
    packetdatetime          datetime not null,
    ipsrc                   int unsigned not null,
    ipdst                   int unsigned not null,
    protocol                char(10) not null,
    tcpflags                varchar(50),
    portortype              smallint unsigned not null,
    isosourcecountry        char(2)  not null,
    sourcecountry           varchar(100)  not null,
    sourcecity              varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci not null default 'Unknown',
    source_latitude         varchar(20) not null,
    source_longitude        varchar(20) not null,
    sourcecoordinates       point,
    isodestinationcountry   char(2)  not null,
    destinationcountry      varchar(100)  not null,
    destinationcity         varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci not null default 'Unknown',
    destination_latitude    varchar(20) not null,
    destination_longitude   varchar(20) not null,
    destinationcoordinates  point,
    awsregion               varchar(50) not null
)
'''

try:
    conn = mysql.connector.connect(host=host,user=user,password=password)
except:
    print("FAILED connecting to MySQL")
else:
    print("SUCCESS connecting to MySQL")
    cursor=conn.cursor()
    try:
        cursor.execute(drop_database)
        cursor.execute(create_database)
        conn.close()
    except:
        print("FAILED",create_database)
    else:
        print("SUCCESS",create_database)
        try:
            conn = mysql.connector.connect(host=host,user=user,password=password,database=dataset_name)
        except:
            print("FAILED connecting to database ",dataset_name)
        else:
            print("SUCCESS Connecting to database ",dataset_name)
            try:
                cursor=conn.cursor()
                cursor.execute(create_table)
                conn.close()
            except:
                print("FAILED ",create_table)
            else:
                print("SUCCESS",create_table)
    conn.close()

try:
    conn = mysql.connector.connect(host=host,user=user,password=password,database=dataset_name)
except:
    print("FAILED connecting to ",dataset_name)
else:
    counter=0
    cursor=conn.cursor()
    for rawline in sys.stdin:
        line=rawline.rstrip()
        line=line.split(',')
        timestamp=str(line[0])
        ipsrc=str(line[1])
        ipdst=str(line[2])
        tcpdstport=str(line[3])
        tcpdstflags=str(line[4])
        udpdstport=str(line[5])
        icmptype=str(line[6])
        src_iso_code=str(line[7])
        src_country_name=str(line[8])
        src_city_name=str(line[9])
        src_lat=str(line[10])
        src_lon=str(line[11])
        dst_iso_code=str(line[12])
        dst_country_name=str(line[13])
        dst_city_name=str(line[14])
        dst_lat=str(line[15])
        dst_lon=str(line[16])
        awsregion=str(line[17])
        #debug_string = timestamp + ipsrc + ipdst + tcpdstport + tcpdstflags + udpdstport + icmptype + src_iso_code + src_country_name + src_city_name + src_lat + src_lon + dst_iso_code + dst_country_name + dst_city_name + dst_lat + dst_lon + awsregion

        ipsrc="INET_ATON('" + ipsrc + "')"
        ipdst="INET_ATON('" + ipdst + "')"

        if tcpdstport:
            protocol="TCP"
            portortype=tcpdstport
        else:
            if udpdstport:
                protocol="UDP"
                portortype=udpdstport
            else:
                if icmptype:
                    protocol="ICMP"
                    portortype=icmptype
                else:
                    protocol="UNKN" # This should never happen!
                    portortype="0"

        if len(src_iso_code) > 2:
                src_iso_code = 'UN'

        if len(dst_iso_code) > 2:
                dst_iso_code = 'UN'

        sourcecoordinates = "POINTFROMTEXT('POINT(" + src_lon + " " + src_lat + ")')"
        destinationcoordinates = "POINTFROMTEXT('POINT(" + dst_lon + " " + dst_lat + ")')"

        insert_command = "INSERT INTO " + dataset_name + " "
        insert_command = insert_command + '''
        (
            packetdatetime,
            ipsrc,
            ipdst,
            protocol,
            tcpflags,
            portortype,
            isosourcecountry,
            sourcecountry,
            sourcecity,
            source_latitude,
            source_longitude,
            sourcecoordinates,
            isodestinationcountry,
            destinationcountry,
            destinationcity,
            destination_latitude,
            destination_longitude,
            destinationcoordinates,
            awsregion
        )

        VALUES
        (
        '''
        insert_values = "'" + timestamp + "',"
        insert_values = insert_values + ipsrc + ","
        insert_values = insert_values + ipdst + ","
        insert_values = insert_values + "'" + protocol + "',"
        insert_values = insert_values + "'" + tcpdstflags + "',"
        insert_values = insert_values + "'" + portortype + "',"
        insert_values = insert_values + "'" + src_iso_code + "',"
        insert_values = insert_values + "'" + src_country_name + "',"
        insert_values = insert_values + "'" + src_city_name + "',"
        insert_values = insert_values + "'" + src_lat + "',"
        insert_values = insert_values + "'" + src_lon + "',"
        insert_values = insert_values + sourcecoordinates + ","
        insert_values = insert_values + "'" + dst_iso_code + "',"
        insert_values = insert_values + "'" + dst_country_name + "',"
        insert_values = insert_values + "'" + dst_city_name + "',"
        insert_values = insert_values + "'" + dst_lat + "',"
        insert_values = insert_values + "'" + dst_lon + "',"
        insert_values = insert_values + destinationcoordinates + ","
        insert_values = insert_values + "'" + awsregion + "'"
        insert_values = insert_values + ')'

        insert_command = insert_command + insert_values

        #print(insert_values)
        cursor.execute(insert_command)
        counter=counter+1
        commit=100000
        if counter % commit == 0:
                print("Inserted and committed " + str(counter) + " rows")
                conn.commit()

print("Inserted and committed a total amount of " + str(counter) + " rows")
conn.commit()
conn.close()
