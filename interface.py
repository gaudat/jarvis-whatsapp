"""Yowsup interface"""

import subprocess
from constants import *

def get_cmd_receive_message():
    return """
/L
/inbox print
/sleep %s
/disconnect
/quit
""" % timeout

def get_cmd_send_message(recipient,message):
    outstr = """
/L
/inbox print
"""
    outstr += '\n'.join(["/message send %s \"%s\"" % (recipient, m) for m in message.split('\n')])
    outstr += """
/sleep %s
/disconnect
/quit
""" % timeout
    return outstr

def receive_messages():
    p = subprocess.Popen(yowsup_args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o,e = p.communicate(input=get_cmd_receive_message())
    return (o,e)

def send_message(message,recipient=group_jid):
    if flush:
        return
    p = subprocess.Popen(yowsup_args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o,e = p.communicate(input=get_cmd_send_message(recipient,message))
    return (o,e)
