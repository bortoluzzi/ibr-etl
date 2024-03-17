#!/bin/bash
workdir=$(pwd)
destination="aggregated"
rm -rf $destination
mkdir -p $destination

echo "Output is at ${destination}"

echo "Step 1: tcprewrite"

for file in *.pcap.gz; do
	output=$destination
	tempfile=$destination
	output+='/'
	tempfile+='/temp_'
	output+=$(echo "$file" | sed 's/.gz$//g')
	tempfile+=$(echo "$file" | sed 's/.gz$//g')	
	ipv4=$(echo $file | grep -oP '\d+\.\d+\.\d+\.\d+')
	echo "Generating temporary file ${file} --> ${tempfile}"
	zcat ${file} > ${tempfile}
	echo "tcprewriting ${tempfile} --> ${output} with public IP ${ipv4}"
	tcprewrite --dstipmap=0.0.0.0/0:${ipv4} --infile=${tempfile} --outfile=${output}
	echo "Deleting temporary file ${tempfile}"
	rm ${tempfile}
	echo "Compressing rewritten TCP file ${output}"
	gzip ${output}
done

echo -e
echo "Step 2: Region split"

cd $destination
for file in *.pcap.gz; do
	IFS='-' read -ra region <<< "${file}"
	regionfile="${region[0]}-${region[1]}-${region[2]:0:1}.pcap"
	echo "Region file is ${regionfile}"
	regiondir="${region[0]}-${region[1]}-${region[2]:0:1}"
	echo "Region directory is ${regiondir}"
	echo "Creating or recreating directory ${regiondir}"
	mkdir -p ${regiondir}
	echo "Moving ${file} to ${regiondir}"
	mv $file $regiondir
done

echo -e
echo "Step 3: Merging"

for dir in *; do
	if [ -d "$dir" ]; then
		echo "Merging ${dir}"
		filename="${dir}.pcap"
		echo "Merging region into ${filename}"
		mergecap -w ${filename} ${dir}/*.pcap.gz
		echo "Deleting temporary data in ${dir}"
        rm ${dir}/*.pcap.gz
        echo "Removing directory ${dir}"
        rmdir ${dir}
	fi
done

echo -e
echo "Step 4: Compressing resulting PCAPs"

for file in *.pcap; do
	echo "Compressing ${file}"
	gzip ${file}
done

echo "Finished. Returning to ${workdir}"
cd ${workdir}
