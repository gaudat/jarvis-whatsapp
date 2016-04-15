"""Yowsup interface"""

import subprocess

yowsup_cli = "/home/me/jarvis-whatsapp/yowsup-cli"
yowsup_conf = "/home/me/jarvis-whatsapp/yowsup.conf"
args = [yowsup_cli,"demos","-y","-e","-c",yowsup_conf]
timeout = 5
group_jid = "85268794568-1453974029@g.us"


def get_cmd_receive_message():
    return """
/L
/inbox print
/sleep %s
/disconnect
/quit
""" % timeout

def get_cmd_send_message(recipient,message):
    return """
/L
/message send %s %s
/sleep %s
/disconnect
/quit
""" % (recipient,message,timeout)

def receive_messages():
    p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o,e = p.communicate(input=get_cmd_receive_message())
    print((o,e))

def send_message(message,recipient=group_jid):
    p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o,e = p.communicate(input=get_cmd_send_message(recipient,message))
    print((o,e))