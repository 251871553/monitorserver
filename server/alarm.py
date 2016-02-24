#!/usr/bin/env python`
import redis
import json
import commands
import time
import sys

import  send_mail


cpu_idlerange=[30.0,10.0]

loop=0

def  alarm_mail(subject,context):
     send_mail.send_mail(send_mail.mailto_list,subject,context)
     print  'send  ok'
#     time.sleep(30)


while  True:
   r=redis.Redis(host='127.0.0.1',port=6379,db=0)
   host_list=r.keys()
   for  i  in host_list:        
       msg=json.loads(r.get(i))
       print  '%s   info'   % i
       for  k,v in msg.items():
           cpuidle=v.get('system').get('cpu')[1]
           if cpu_idlerange[0]  <=  cpuidle:
              print  'cpu idle is ok'
           elif cpu_idlerange[1]  >=  cpuidle:
              loop=loop + 1
              print  'is  buzy'
              if  loop == 3:
                print  'alarm'
             #   send_mail.send_mail(send_mail.mailto_list,'alarm_cpuidle',str(cpuidle))
                alarm_mail('cpu_alarm',str(cpuidle))
                loop=0
           else:
              print  'warning'

#############################mem#######################
           mem_avg=v.get('system').get('mem')[2]
           if mem_avg  >=  20.0:
              print  'mem  is ok'
           else:
              print  'mem  is alarm'   

#############################disk#######################
           disk_used=v.get('system').get('disk')[1]
           if disk_used  <=  80.0:
              print  'disk  is ok'
           else:
              print  'alarm'   

#############################swap#######################
           swap_used=v.get('system').get('swap')[0]
           if swap_used  <=  80.0:
              print  'swap  is ok'
           else:
              print  'alarm'   


#############################http#######################
           http_code=v.get('service').get('http')[0]
           if http_code  <=  200:
              print  'http  is ok'
           else:
              print  'alarm'   

############################mysql####################### 
       
           mysql_status=v.get('service').get('mysql')[0]
           if mysql_status >= 1:
              print   'mysql  is  ok'
           else:
              print  'mysql  is  error'

#########################redis###########################
           redis_status= v.get('service').get('redis')[0]
           if redis_status == True:
              print  'redis  is   ok'
           else:
              print  'redis  is  error'
 #       print redis_status

#########################tomcat##########################
           try:
              tomcat_status= v.get('service').get('tomcat')[0]
              if tomcat_status == True    :
                 print  'tomcat  is   ok'
              else:
                 print  'tomcat  is  error'
           except Exception,e:
                 print  'tomcat  is  error'

           print  '########################################################'


   time.sleep(5)
   print  '########################################################'
