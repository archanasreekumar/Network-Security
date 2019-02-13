from collections import OrderedDict 
import json
import math
import socket, struct 
import sys

# ntwk={}
ntwk_start={}
ntwk_stop={}
file_name=sys.argv[1]
f = open(file_name, "r")
jdata=f.readline()
#print jdata
#jdata='{"network_addr": "192.168.128.0","subnets": {"1": 13, "2": 11, "3": 12},"netmask": "255.255.224.0"}'
pdata=json.loads(jdata)
#print pdata
net_add_int=[]
net_add=pdata['network_addr']
net_add_copy=net_add#192.168.128.0
net_add=net_add.split('.')
for i in net_add:
	net_add_int.append(int(i))#[192, 168, 128, 0]--->use
net_add_intcopy=net_add_int
ntwk_dec=(net_add_int[0]*(256**3))+(net_add_int[1]*(256**2))+(net_add_int[2]*(256**1))+(net_add_int[3]*(256**0))

#print net_add_int
#print ntwk_dec

subnet=pdata['subnets']
netmask=pdata['netmask']
#print subnet
sorted_subnets=sorted(subnet.items(), key=lambda x: x[1],reverse=True)
#print sorted_subnets


number_of_subnets = len(sorted_subnets)
for i in range(number_of_subnets):
	subnet_id = sorted_subnets[i][0]
	total_hosts = sorted_subnets[i][1] + 2				

	exp = 0												
	while 2**exp < total_hosts:
		exp += 1

	sorted_subnets[i] = (subnet_id, 2**exp)				

#print sorted_subnets





for i in range(number_of_subnets):
	ntwk_stop[sorted_subnets[i][0]]=ntwk_dec+(int(sorted_subnets[i][1]))-1#-->15
	ntwk_start[sorted_subnets[i][0]]=ntwk_dec#-->0
	ntwk_dec+=int(sorted_subnets[i][1])
	
#print ntwk_start
#print ntwk_stop
for key in ntwk_start:
	ntwk_start[key]=socket.inet_ntoa(struct.pack('!L', ntwk_start[key]))
#print ntwk_start

for key in ntwk_stop:
	ntwk_stop[key]=socket.inet_ntoa(struct.pack('!L', ntwk_stop[key]))
#print ntwk_stop
h_list=[]
h_num=0
for i in range(number_of_subnets):
	h_list.append(int(sorted_subnets[i][1]))
for i in range(len(h_list)):
	h_num+=h_list[i]
#print h_num#--->tot host calculated
netmask_str=''

netmask_bin=[bin(int(x)+256)[3:] for x in netmask.split('.')]
#print netmask_bin
for i in netmask_bin:
	netmask_str+=i
#print netmask_str
count=0

for i in netmask_str:
	if i=='0':
		count+=1
#print count
net_host=2**count
#print net_host#--->host count from netmask##compare it with h_num


sub_internal={}
rounded={}
sub_extrnl={}
#unicod={}

for i in range(number_of_subnets):
	rounded[sorted_subnets[i][0]]=sorted_subnets[i][1]
	

#print rounded

i=0
mask_string=''
mask={}
for key in rounded:
	while((2**i)<rounded[key]):
		if rounded[key]!=2**i:
			i+=1
	#print 'i of '+str(key)+'  is  '+str(i)
	
	for j in range(32-i):
		mask_string+='1'
	for j in range(i):
		mask_string+='0'
	#print mask_string
	mask[key]=int(mask_string,2)
	i=0
	mask_string=''
#print mask
mask_ip={}
for key in mask:
	mask_ip[key]='.'.join([str(mask[key] >> (i << 3) & 0xFF)
          for i in range(4)[::-1]])
#print mask_ip
for key in ntwk_start:#--->key: 1,2,3
	#print key
	sub_internal["network_addr"]=str(ntwk_start[key])
	sub_internal["netmask"]=str(mask_ip[key])
	sub_internal["start_addr"]=str(ntwk_start[key])
	sub_internal["end_addr"]=str(ntwk_stop[key])
	sub_internal["total_host_count"]=int(rounded[key])-2
	#print sub_internal
	sub_extrnl[str(int(key))]=sub_internal
	sub_internal={}
	#print sub_extrnl
#print sub_extrnl

#dict_success={"success": true}
#dict_subnet={"subnets":sub_extrnl}
dict_fail={"success": False}
dict_final={"success": True,"subnets":sub_extrnl}
#print dict_final

if(net_host>=h_num):
	print json.dumps(dict_final)+"\n"
else:
	print json.dumps(dict_fail)+"\n"


