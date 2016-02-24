#!/usr/bin/env  python
#this is socketserver
import SocketServer,json
import redis
r=redis.Redis(host='127.0.0.1',port=6379,db=0)

HOST='10.10.1.56'
PORT=6001
addr=(HOST,PORT)
class mysocket(SocketServer.BaseRequestHandler):
      def handle(self):
        try: 
           while True:
             data=self.request.recv(1024).strip()
             r[self.client_address[0]]=data
             data=json.loads(data)
             print 'msg: %s from %s' % (data,self.client_address[0])
             if not data:
                break
           #  self.request.sendall(json.dumps(data))
             self.request.sendall('recv ok!')
             print '--------------------send OK !--------------------'
        except ValueError:
           print ' %s has gone  ' % self.client_address[0]

server=SocketServer.ThreadingTCPServer(addr,mysocket)
server.serve_forever()

