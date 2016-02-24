#!/usr/bin/env python3  
#coding: utf-8
# 导入 smtplib 和 MIMEText 
import smtplib 
from email.mime.text import MIMEText 
# 定义发送列表 
#mailto_list=["251871553@qq.com","463759597@qq.com"] 
mailto_list=["chen.tianping@71dai.com"] 
# 设置服务器名称、用户名、密码以及邮件后缀 
mail_host = "smtp.163.com" 
mail_user = "18666553354" 
mail_pass = "tianping360" 
mail_postfix="163.com" 
# 发送邮件函数 
def send_mail(to_list, sub, context): 
   '''''
   to_list: 发送给谁
   sub: 主题
   context: 内容
   send_mail("xxx@126.com","sub","context")
   ''' 
   me = mail_user + "<"+mail_user+"@"+mail_postfix+">" 
   msg = MIMEText(context) 
   msg['Subject'] = sub 
   msg['From'] = me 
   msg['To'] = ";".join(to_list) 
   try: 
      send_smtp = smtplib.SMTP() 
      send_smtp.connect(mail_host) 
      send_smtp.login(mail_user, mail_pass) 
      send_smtp.sendmail(me, to_list, msg.as_string()) 
      send_smtp.close() 
      return True 
   except (Exception, e): 
      print(str(e)) 
      return False 
if __name__ == '__mian__': 
   pass
'''
subject='alarm'
context='this  is a test'
if (True == send_mail(mailto_list,subject,context)): 
   print ("发送成功") 
else: 
   print ("发送失败")   '''
