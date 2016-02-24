#coding:utf-8
import  psutil
import socket
#import fcntl
#import struct
import  json
import  time
import  sys
import MySQLdb
import pycurl
from io import BytesIO
import  redis
import  re


#pip  install   psutil  before run   this  script


class  system:
    def __init__(self):
         pass
    def  check_cpu(self):
         cpuall=psutil.cpu_times_percent(interval=1)
         cpu_iowait=cpuall.iowait
         cpu_idle=cpuall.idle
         cpuinfo=[cpu_iowait,cpu_idle]
         return cpuinfo


    def  check_mem(self):
      #  meminfo=psutil.virtual_memory()
         mem_total=psutil.virtual_memory().total
         mem_free=psutil.virtual_memory().free
     #    mem_free_percent= float(  "%.2f" % (float(mem_free)/float(mem_total))  )
         mem_free_percent= float(  "%.1f" % (float(mem_free)/float(mem_total) *100 )  )
         meminfo=[mem_total,mem_free,mem_free_percent]
         return  meminfo

    def  check_disk(self):
         disk_part=psutil.disk_partitions()
         disk_root_free=psutil.disk_usage('/').percent
         diskinfo=[disk_part,disk_root_free]
         return  diskinfo

    def  check_swap(self):
         swapall= psutil.swap_memory()
         swap_total=swapall.total
         swap_used=swapall.used
         swap_percent=swapall.percent
         swapinfo=[swap_percent,swap_total,swap_used]
         return  swapinfo


    def  check_net(self):
        net_io1=psutil.net_io_counters(pernic=True).get('eno16777736')
        net_io_sent1=net_io1.bytes_sent
        net_io_recv1=net_io1.bytes_recv
    #    print net_io_sent1,net_io_recv1

        time.sleep(1)

        net_io2=psutil.net_io_counters(pernic=True).get('eno16777736')
        net_io_sent2=net_io2.bytes_sent
        net_io_recv2=net_io2.bytes_recv
    #    print net_io_sent2,net_io_recv2
        net_io_sent=net_io_sent2-net_io_sent1
        net_io_recv=net_io_recv2-net_io_recv1
        netinfo=[net_io_sent,net_io_recv]
        return netinfo
    

    def info_machine(self):
        cpuinfo=self.check_cpu()
        meminfo=self.check_mem()
        swapinfo=self.check_swap()
        diskinfo=self.check_disk()
        netinfo=self.check_net()
        machine_info={'cpu':cpuinfo,'mem':meminfo,'swap':swapinfo,'disk':diskinfo,'net':netinfo}
        return  machine_info

system=system()

class  service:
    def __init__(self):
         pass
    def  mysql(self,command):
       try:
          conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='',db='mysql',charset='utf8')
          cur=conn.cursor()
          cur.execute(command)
          info=cur.fetchall()
          cur.close()
          conn.close()
          for  i  in  info:
               info=i
          return  info
       except Exception,e:
          return e

    def  check_mysql(self):
       try:
          a= self.mysql("show  status  like 'Uptime'")[1]
          time.sleep(1)
          b= self.mysql("show  status  like 'Uptime'")[1]
          c=int(b)-int(a)
          d= int(self.mysql("show  status  like 'Threads_connected'")[1])
          mysqlinfo=[c,d]
          return mysqlinfo
       except Exception,e:
          mysqlinfo=[0,str(e)]
          return mysqlinfo

    def  check_http(self):
          buffer = BytesIO()
          c = pycurl.Curl()
          c.setopt(c.URL, 'http://www.baidu.com/')
       #   c.setopt(c.URL, 'http://127.0.0.1/')
          c.setopt(c.WRITEFUNCTION, buffer.write)
          c.perform()
          status=c.getinfo(c.RESPONSE_CODE)
          time_used=c.getinfo(c.TOTAL_TIME)
          httpinfo=[status,time_used]
          return httpinfo

    def  check_tomcat(self):
         tomcatinfo=['haimei','wancheng']
         re_java=re.compile('java')
         pid_list = psutil.pids()
         for  i  in pid_list:
            processname = psutil.Process(i).name()
            result = re.findall(re_java,processname)
            if  result:
               return [True,i]
  
    def  check_redis(self):
       try: 
          r = redis.Redis(host='localhost', port=6379, db=0) 
          status=r.ping()
          key_count=r.dbsize()
          redisinfo=[status,key_count]
          return  redisinfo
       except Exception,e:
          e= str(e)
          redisinfo=[False,e]
          return redisinfo

    def info_service(self):
        mysqlinfo=self.check_mysql()
        httpinfo=self.check_http()
        redisinfo=self.check_redis()
        tomcatinfo=self.check_tomcat()
        service_info={'mysql':mysqlinfo,'http':httpinfo,'redis':redisinfo,'tomcat':tomcatinfo}
        return  service_info

service=service()

#sys.exit()

#if __name__ == "__main__":

HOST='10.10.1.56'
PORT=6001
myip='10.10.1.119'


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
while  True:
#     send=raw_input('please enter:').strip()
     machineinfo=system.info_machine()
     serviceinfo=service.info_service()
     send={myip:{'system':machineinfo,'service':serviceinfo}}
     s.sendall(json.dumps(send))
     print 'send ok !'
   #  data=json.loads(s.recv(1024))
     data=s.recv(1024)
     print 'recv msg: %s ' %  data
     time.sleep(5)
s.close()
