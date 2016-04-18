# coding=utf8
from constants import *
import database
import interface
from dateutil.parser import parse # magical date parser

def look_for_incoming_messages(stdout):
    messages = []
    lines = stdout.split('\n')
    for l in lines:
        if magic_word.lower() in l.lower():
            messages.append({
                'sender': l.split(']')[1][2:].split('@')[0],
                'message': l.split(']')[-1].strip()
            })
    return messages

def parse_messages(ms):
    for m in ms:
        if 'weather'.lower() in m['message'].lower():
            outstr = 'I don\'t have a weather sensor installed.'
            interface.send_message(outstr)
            return
        if 'temperature'.lower() in m['message'].lower():
            look_up_temp()
            return
    else:
        outstr = 'What can I help you?'
        interface.send_message(outstr)

            

def look_up_temp():
    c = db.cursor()
    c.execute('select * from airdata;')
    airs = c.fetchall()
    outstr = 'The temperature at home is '+str(airs[-1][2])+'°C and the humidity at home is '+str(airs[-1][1])+'.'
    if airs[-1][2] > aircon_on_threshold:
        outstr += '\nYou may want to turn on the aircon.'
    elif airs[-1][1] > dehum_on_threshold:
        outstr += '\nYou may want to turn on the humidifier.'
    else:
        pass
    interface.send_message(outstr)

database.connect_db()
db = database.db
o,e = interface.receive_messages()
ms = look_for_incoming_messages(o)
parse_messages(ms)
