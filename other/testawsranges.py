import sys
import awsipranges
aws_ip_ranges = awsipranges.get_ranges()

for rawline in sys.stdin:
	line=rawline.rstrip()
	line=line.split(',')
	ipdst=str(line[2])
	try:
		aws_response = aws_ip_ranges.get(ipdst)
		print(aws_response.region)
	except:
		print('fail')
