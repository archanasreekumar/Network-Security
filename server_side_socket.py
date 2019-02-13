import socket
import sys
import os
import json
from collections import OrderedDict 

server_host = ''
server_port = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (server_host, server_port)

sock.bind((server_address))

def snake_ladders_game(conn, jdata):
  d1={} 
  pdata=json.loads(jdata)#converted input string to dict
  #print pdata
  p_count=pdata['player_count']
  b_dim=pdata['board_dimension']
  b_dim*=b_dim
  #print b_dim
  l=pdata['ladders']
  #print l
  s=pdata['snakes']
  #print s
  die={}
  die=pdata['die_tosses']
  #print die
  rounds=len(die)
  #print rounds
  r=[0]
  r1={}
  #r={}
  s1={}
  s2={}
  s3={}
  x=0


  for rnd in range(1,rounds+1):#initializinf dict s1 with zeroes
    r1=die[str(rnd)]
    for k1 in r1:
      s1[k1]=0
      s2[k1]=0
  #print s1

  for rnd in range(1,rounds+1):
    r1=die[str(rnd)]#{u'1':5,u'3':5,u'2':1}
    #print r1
    r1l=len(r1)#3
    #print r1l

    for key in r1:
      #print r1[key]
      sum1=0
      sum1=int(r1[key])
      temp1=int(s1[key])
      s1[key]=sum1+int(s1[key])
      if(s1[key]>b_dim):#checking wthr value exceeds dimension
        s1[key]=int(s1[key])-sum1#34
      if(s1[key]==temp1):
        flag=0
      else: 
        d1.setdefault(key, []).append(s1[key])
      if(s1[key]==b_dim):
        x=str(key)#winner
      for lad in l:#checking ladders
        if(s1[key]==int(lad)):
          temp=int(s1[key])
          s1[key]=int(l[lad])
          if(s1[key]>b_dim):
            s1[key]=temp
          if(s1[key]==b_dim):
            x=str(key)#winner
          d1.setdefault(key, []).append(s1[key])
      #print s1
      for snk in s:#checking snakes
        if(s1[key]==int(snk)):
          temp=int(s1[key])
          s1[key]=int(s[snk])
          if(s1[key]>b_dim):
            s1[key]=temp
          if(s1[key]==b_dim):
            x=str(key)#winner
          d1.setdefault(key, []).append(s1[key])
  #print d1#traversing
  #print s1#final position
  #print 'winner is '+ str(x)
  if x!=0:
    gstate="finished"#Game state
  else:
    gstate="progress"
  final=OrderedDict()
  if gstate=="finished":
    final["winner"]=int(x)
  if gstate=="progress":
    final["winner"]=None
  final["game_state"]=str(gstate)
  final["final_positions"]=s1
  final["squares_traversed"]=d1
  conn.sendall(json.dumps(final)+"\n")

 

sock.listen(3) 
max_clients = 3

for client in range(max_clients):
  try:
    pid = os.fork()
  except OSError:
    sys.stderr.write("Error in creating Child Process\n")
    continue
  
  if pid == 0: # pid is 0 then in the child fork
    
    conn, address = sock.accept()
    #client_input = ''
    while True:
      client_input = conn.recv(8000)
      if client_input.startswith('0'):
        break
      if client_input.endswith('\n'):
        snake_ladders_game(conn, client_input)
        #client_input = ''
    exit()


for client in range(max_clients):
  os.waitpid(0,0)#wait for 3 clients to exit



