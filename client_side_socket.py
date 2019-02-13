import socket
import sys
import json

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 	#creating a tcp socket
server_address = (sys.argv[1],int(sys.argv[2]))
 	#server_ad = (server_name,8080)
sock.connect(server_address)
while True:
  	message = sock.recv(8000)
  	if message=="0\n":
		break 
	x=message.split("||")
	#print x
	d={'S':20,'T':20,'R':20,'W':50,'F':50}
	d1={}
	d2={}
	player =int(x[0])
	rounds =int(x[1])
	#print player
	#print rounds
	del x[0],x[0]
	#print x
	y = []
	i=0
	a = []
	b=[]
	trial=[]
	for key,value in enumerate(x):
		if value=='0':
	 		y.append(key)
	#print y
	for i in range(len(y)):
		if i==0:		
	 		a=x[:y[i]]
	 		#print a
	 		b.append(a)
	 		#print b
		else:
	 		a=x[y[i-1]+1:y[i]]
	 		#print a
	 		b.append(a)
		#print b
	round = []
	#loop starts
	for i in range(rounds):
		round.insert(i,b[i])
		r=round[i]
		#print r
		r1=round[i][0]
		#print r1
		del r[0]
		#print r
		for j in range(len(r)):
			#print r[j]
			p=r[j].split(":")
			card=p[1].split(",")
			#print card
			sum1=0
			#print len(card)
			for k in range(len(card)):
				#print card[k]
				if(card[k]=='S'or card[k]=='T'or card[k]=='R' or card[k]=='W'or card[k]=='F'):
					sum1=sum1+int(d.get(card[k]))
				else:
					sum1=sum1+int(card[k])
			d1[p[0]]=sum1
		d2[r1]=d1
		trial.append(d2)
		trial1=trial
		#print trial1
		d1={}
		d2={}
	#finding round winners
	d3={}
	d4={}
	d5={}
	d6={}
	l1=[]
	l2=[]
	l3=[]
	x={}
	#print trial1
	for i in range(rounds):
		r=i
		d3=trial1[i]
		#print d3
		for key in d3:
			k1=key#round number()
			#print k1
			x=d3[k1]
			#print x
			sum2=0
			for key in x:
				sum2=sum2+x[key]
			#print sum2
			if len(x)!=player:
				l1=[]
				for j in range(1,player+1):
					l1.append(j)
				#print l1
        		l2=[]
        		for key in x:
        			l2.append(int(key))
        		l2.sort()
        		#print l2
        	l3=list(set(l1)^set(l2))
        	#print l3
        	d5[k1]=sum2
        	d4[k1]=l3[0]#round_winners{'1':2,'2':1}
	#print d4  #PRINT ROUND WINNER  
	#print d5
	for p in range(1,player+1):
		p_score=0
 		for k4 in d4:
 			if d4[k4]==p:
 				p_score=p_score+d5[k4]
 		d6[str(p)]=p_score#scores
 	#print d6#PRINT SCORES
	overall1=[]
	#for p in range(1,4):
	overall=max(d6,key=d6.get)
	#print x
	for p in range(1,player+1):
		if d6[overall]==d6[str(p)]:
			overall1.append(p)
	if len(overall1)==1:
		o=overall#PRINT OVERALL WINNER IF ONLY ONE
	else:
		o= overall1#PRINT OVERALL WINNER IF MORE THAN ONE
	#print o
	d_final={}
	d_final["round_winners"]=d4
	if len(o)==1:
		d_final["overall_winner"]=int(o)
	else:
		d_final["overall_winner"]=o
	d_final["scores"]=d6#input dict to json
	#print d_final#print input to json
	sock.send(json.dumps(d_final)+"\n")#addind new line character to json output
	#print j
sock.close()