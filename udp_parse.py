import sys
from hashlib import sha256
import hashlib 
seg = sys.argv[1]
s_ip = sys.argv[2]
d_ip=sys.argv[3]
s_port=seg[:4]
d_port=seg[4:8]
length=seg[8:12]
checksum=seg[12:16]
data=seg[16:]
# print seg
# print s_ip
# print d_ip
# print s_port
# print d_port
# print length
# print checksum
# print data
s_port=int(s_port,16)#-->print
#print s_port
d_port=int(d_port,16)#-->print
#print d_port
length=int(length,16)
#print length#-->compare1-->print
seg_len=len(seg)/2
#print seg_len#-->compare1


source_ip = s_ip
source_port = s_port
dest_ip=d_ip
dest_port = d_port
hdata=data
hdata2=hdata
hdata=hdata.decode('hex')
#print hdata
l=len(hdata)
#print l
if(l%2!=0):
	hdata=hdata+chr(0)
#print len(hdata)
	hdata=hdata.encode('hex')#hex data after appending 0 
else:
	hdata=hdata.encode('hex')#hex data without appending zero
s_ip_bin=' ' .join(format(int(x), '08b') for x in source_ip.split('.'))#binary of source ip
#print s_ip_bin
d_ip_bin=' ' .join(format(int(x), '08b') for x in dest_ip.split('.'))#binary of dest ip
#print d_ip_bin


s_ip_bin_1=s_ip_bin[:17]#first 16 bits
#print s_ip_bin_1
s_ip_bin_2=s_ip_bin[18:]#last 16 bits
#print s_ip_bin_2
num1=s_ip_bin_1.replace(' ','')
num2=s_ip_bin_2.replace(' ','')
sum1 = bin(int(num1,2) + int(num2,2))
source_sum = sum1[2:]#sum of 16 bit+16bit of source ip
#print source_sum
#x=bin(1)#binary one
while len(source_sum)>16:#carry addition
	a=len(source_sum)
	a=a-16
	x=source_sum[:a]
	source_sum=source_sum[a:]
	
	source_sum=bin(int(source_sum,2) + int(x,2))
	source_sum=source_sum[2:]
#source_sum=''.join('1' if x == '0' else '0' for x in source_sum)#ones cmplmnt result(final)
#print source_sum
source_sumhex=hex(int(source_sum,2))
source_sumhex=source_sumhex[2:]
source_sumhex=source_sumhex.zfill(4)#-->1
#print source_sumhex


###dest ip calculation
d_ip_bin_1=d_ip_bin[:17]
d_ip_bin_2=d_ip_bin[18:]
num3=d_ip_bin_1.replace(' ','')
num4=d_ip_bin_2.replace(' ','')
sum2 = bin(int(num3,2) + int(num4,2))
dest_sum = sum2[2:]#sum of 16 bit+16bit of source ip
#print dest_sum
while len(dest_sum)>16:#ones complement loop
	a=len(dest_sum)
	a=a-16
	x=dest_sum[:a]
	dest_sum=dest_sum[a:]
	# x=bin(a)
	# x=x[2:]
	dest_sum=bin(int(dest_sum,2) + int(x,2))
	dest_sum=dest_sum[2:]
#dest_sum=''.join('1' if x == '0' else '0' for x in dest_sum)#ones cmplmnt result(final)
#print dest_sum
dest_sumhex=hex(int(dest_sum,2))
dest_sumhex=dest_sumhex[2:]
dest_sumhex=dest_sumhex.zfill(4)#-->2
#print dest_sumhex


udp_num=bin(17)
udp_num=udp_num[2:]
udp_num=udp_num.zfill(16)
#print udp_num
udp_sumhex=hex(int(udp_num,2))
udp_sumhex=udp_sumhex[2:]
udp_sumhex=udp_sumhex.zfill(4)#-->3
#print udp_sumhex


udp_len=l+8
udp_len_hex=hex(udp_len)
# udp_len_hex=udp_len.encode('hex')
#print udp_len_hex
udp_len_bin=bin(udp_len)
udp_len_bin=udp_len_bin[2:]
udp_len_bin=udp_len_bin.zfill(16)
#print udp_len_bin#--->0000d
udp_lenhex=hex(int(udp_len_bin,2))
udp_lenhex=udp_lenhex[2:]
udp_lenhex=udp_lenhex.zfill(4)#-->4-->append
#print udp_lenhex

# tot_se_len=udp_len+8
# tot_se_len=hex(tot_se_len)
#print tot_se_len

sp_bin=bin(int(source_port))
sp_bin=sp_bin[2:]
sp_bin=sp_bin.zfill(16)
#print sp_bin
sp_hex=hex(int(sp_bin,2))

sp_hex=sp_hex[2:]
sp_hex=sp_hex.zfill(4)#-->5-->append
#print sp_hex


dp_bin=bin(int(dest_port))
dp_bin=dp_bin[2:]
dp_bin=dp_bin.zfill(16)
#print dp_bin
dp_hex=hex(int(dp_bin,2))

dp_hex=dp_hex[2:]
dp_hex=dp_hex.zfill(4)#-->6-->append
#print dp_hex


sum56=(hex(int(dp_hex,16)+int(sp_hex,16)))#-->5+6
sum56=sum56[2:]
sum56=sum56.zfill(4)

while len(sum56)>4:
	l=len(sum56)
	l=l-4
	x=sum56[:l]
	sum56=sum56[l:]
	sum56=(hex(int(sum56,16)+int(x,16)))
	sum56=sum56[2:]
	sum56=sum56.zfill(4)
#print sum56


sum34=(hex(int(udp_lenhex,16)+int(udp_sumhex,16)))#-->3+4
sum34=sum34[2:]
sum34=sum34.zfill(4)

while len(sum34)>4:
	l=len(sum34)
	l=l-4
	x=sum34[:l]
	sum34=sum34[l:]
	sum34=(hex(int(sum34,16)+int(x,16)))
	sum34=sum34[2:]
	sum34=sum34.zfill(4)
#print sum34


sum12=(hex(int(source_sumhex,16)+int(dest_sumhex,16)))#-->1+2
sum12=sum12[2:]
sum12=sum12.zfill(4)

while len(sum12)>4:
	l=len(sum12)
	l=l-4
	x=sum12[:l]
	sum12=sum12[l:]
	sum12=(hex(int(sum12,16)+int(x,16)))
	sum12=sum12[2:]
	sum12=sum12.zfill(4)
#print sum12


sum7=(hex(int(sum12,16)+int(sum34,16)))#-->7
sum7=sum7[2:]
sum7=sum7.zfill(4)

while len(sum7)>4:
	l=len(sum7)
	l=l-4
	x=sum7[:l]
	sum7=sum7[l:]
	sum7=(hex(int(sum7,16)+int(x,16)))
	sum7=sum7[2:]
	sum7=sum7.zfill(4)
#print sum7


sum8=(hex(int(sum7,16)+int(sum56,16)))#-->8
sum8=sum8[2:]
sum8=sum8.zfill(4)

while len(sum8)>4:
	l=len(sum8)
	l=l-4
	x=sum8[:l]
	sum8=sum8[l:]
	sum8=(hex(int(sum8,16)+int(x,16)))
	sum8=sum8[2:]
	sum8=sum8.zfill(4)
#print sum8

sum9=(hex(int(sum8,16)+int(udp_lenhex,16)))#-->9
sum9=sum9[2:]
sum9=sum9.zfill(4)

while len(sum9)>4:
	l=len(sum9)
	l=l-4
	x=sum9[:l]
	sum9=sum9[l:]
	sum9=(hex(int(sum9,16)+int(x,16)))
	sum9=sum9[2:]
	sum9=sum9.zfill(4)
#print sum9

#print hdata
hdata1='0'

while len(hdata)!=0:#-->data addition
	hdata1=(hex(int(hdata[:4],16)+int(hdata1,16)))
	hdata1=hdata1[2:]
	while len(hdata1)>4:
		l=len(hdata1)
		l=l-4
		x=hdata1[:l]
		hdata1=hdata1[l:]
		hdata1=(hex(int(hdata1,16)+int(x,16)))
		hdata1=hdata1[2:]
		hdata1=hdata1.zfill(4)	
	hdata=hdata[4:]
	# print hdata
#print hdata1


sum10=(hex(int(sum9,16)+int(hdata1,16)))#-->10
sum10=sum10[2:]
sum10=sum10.zfill(4)

while len(sum10)>4:
	l=len(sum10)
	l=l-4
	x=sum10[:l]
	sum10=sum10[l:]
	sum10=(hex(int(sum10,16)+int(x,16)))
	sum10=sum10[2:]
	sum10=sum10.zfill(4)
#print sum10
sum10=bin(int(sum10,16))
sum10=sum10[2:].zfill(16)
#print sum10
sum11=''.join('1' if x == '0' else '0' for x in sum10)
#print sum11
sum11=hex(int(sum11,2))
sum11=sum11[2:].zfill(4)#checksum
#print sum11

if(length==seg_len and checksum==sum11 and length>=9):
	print s_port
	print d_port
	print length
	print '0x'+checksum
	data=data.decode("hex")
	hashedWord=hashlib.sha256(data).hexdigest()
	print hashedWord 

else:
	print "Invalid UDP segment"

