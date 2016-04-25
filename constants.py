
yowsup_cli = "/home/me/jarvis-whatsapp/yowsup-cli"
yowsup_conf = "/home/me/jarvis-whatsapp/yowsup.conf"
yowsup_args = [yowsup_cli,"demos","-y","-e","-c",yowsup_conf]
timeout = 3
group_jid = "85268794568-1453974029@g.us"
stfu = False

hostname = 'localhost'
user = 'root'
password = 'memememe'
dbname = 'idpdatabase'


magic_word = 'jarvis'

aircon_on_threshold = 25
dehum_on_threshold = 80

import colour
color = colour.Color

import logging
logging.basicConfig(level='DEBUG')

nodeIDs = {'jarvis':0,'air':1,'light':2,'temp':2,'doorlock':3,'pir':4,'camera':5}

def yowsup_send(message,recipient):
    return [yowsup_cli,"demos","-c",yowsup_conf,"-s",recipient,message]
