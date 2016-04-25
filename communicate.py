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
    if len(ms) == 0:
        logging.info("Received nothing, exiting")
        return
    for m in ms:
        m = m['message'].lower()
        logging.debug('Parsing %s' % m)
        if 'temp' in m or 'temperature' in m:
            logging.info('Got a temperature request')
            parse_temp(m)
            return
        elif 'light' in m:
            parse_lights(m)
            return
        elif 'lamp' in m:
            parse_lights(m)
            return
        elif 'lock the door' in m:
            outstr = 'OK, the door is locked now'
            interface.send_message(outstr)
            return
        elif 'unlock' in m:
            outstr = 'OK, resetting the door lock'
            interface.send_message(outstr)
            return
        elif 'fan' in m:
            if 'turn on' in m:
                outstr = 'Turning on the fan'
                interface.send_message(outstr)
                return
            if 'turn off' in m:
                outstr = 'Turning off the fan'
                outstr += '\nDo you want to open the window?'
                interface.send_message(outstr)
                return
    logging.debug('jarvis status')
    outstr = 'Hello, Jarvis is here. %s' % people_at_home()
    interface.send_message(outstr)
    give_notice()

def people_at_home():
    return "There are 3 people at home"

def parse_temp(instr):
    if 'what' in instr:
        look_up_temp()
        return
    to_tmp = -1
    if 'set' in instr and 'to ' in instr:
        logging.debug('Set to a temperature')
        for i in instr.split(' '):
            try:
                to_tmp = int(i)
            except:
                pass
        if to_tmp == -1:
            outstr = 'I don\'t understand you command. Remember to add spaces between numbers and words.'
            interface.send_message(outstr)
            return
        else:
            outstr = 'Set temperature to %sC' % str(to_tmp)
            c = db.cursor()
            import datetime
            c.execute('insert into airdata values ("%s","%s","%s","%s","%s")' % (datetime.datetime.now().strftime('%s'),0,to_tmp,0,nodeIDs['temp']))
            db.commit()
            interface.send_message(outstr)
            return

def parse_lights(instr):
    from colour import Color
    c = db.cursor()
    logging.info('Got a light request')
    have_color = 0
    to_color= ''
    turn_on = 1
    turn_off = 0
    outstr = ''
    c.execute('select color from lightdata order by timestamp desc limit 1')
    try:
        orig_color = color(str(c.fetchall()[0][0]))
    except:
        orig_color = color()
    logging.debug('original color is '+str(orig_color))
    if 'what color' in instr:
        logging.debug('What color')
        outstr = 'The current light color is %s' % str(orig_color)
        interface.send_message(outstr)
        return
    if 'shuffle' in instr or 'random' in instr:
        logging.debug('Changing to random color')
        import random
        to_color = color(pick_for=random.random())
        outstr = 'Changing light color to a random one...'
        outstr += '\nThe new color is '+str(to_color)
        import datetime
        timestamp = datetime.datetime.now().strftime('%s')
        c.execute('insert into lightdata values (\'\',\'%s\',\'%s\',\'%s\',\'%s\');' % (to_color.get_hex_l(),turn_on,timestamp,nodeIDs['light']))
        db.commit()
        interface.send_message(outstr)

    for w in instr.split(' '):
        try:
            to_color = color(w)
            have_color = 1
        except ValueError:
            pass
    if 'brighter' in instr:
        to_color = orig_color if have_color == 0 else to_color
        have_color=1
        if to_color.luminance < 0.8:
            to_color.luminance += 0.2
        else:
             to_color.luminance = 1
    if 'darker' in instr:
        to_color = orig_color if have_color == 0 else to_color
        have_color=1
        if to_color.luminance > 0.2:
            to_color.luminance -= 0.2
        else:
            to_color.luminance = 0
    if 'turn on' in instr:
        turn_on = 1
    elif 'turn off' in instr:
        turn_off = 1
    if turn_off or to_color == 'black':
        turn_on = 0
        outstr += 'Turning off light\n'
    if have_color and to_color != 'black':
        outstr += 'Changing light color to %s\n' % to_color
    if outstr == '':
        outstr += 'I don\'t know what you mean\n'
    logging.debug('new color is '+str(to_color))
    import datetime
    timestamp = datetime.datetime.now().strftime('%s')
    c.execute('insert into lightdata values (\'\',\'%s\',\'%s\',\'%s\',\'%s\');' % (to_color.get_hex_l(),turn_on,timestamp,nodeIDs['light']))
    db.commit()
    interface.send_message(outstr)

def look_up_temp():
    c = db.cursor()
    c.execute('select * from airdata;')
    airs = c.fetchall()
    outstr = 'The temperature at home is '+str(airs[-1][2])+'°C'
    interface.send_message(outstr)

def give_notice():
    logging.info('Giving notice')
    c = db.cursor()
    outstr = ''
    if c.execute('select * from airdata where odor != 0'):
        logging.info('Someone farted')
        outstr += '\nSomeone farted\nTurning on exhaust...'
        c.fetchall()
        c.execute('delete from airdata where odor != 0')
        db.commit()
        interface.send_message(outstr)
    if not c.execute('select success from lockdata order by timestamp desc limit 3') == 0:
        if sum(zip(*c.fetchall())[0]) == 0:
            # 3 failed attempts
            outstr += '\n The door has been locked due to failed attempts. Say "unlock jarvis" to reset the lock'
            import datetime
            c.execute('insert into lockdata values (\'%s\',0,1)' % datetime.datetime.now().strftime('%s'))
            db.commit()
        interface.send_message(outstr)
        


database.connect_db()
db = database.db
o,e = interface.receive_messages()
logging.debug(o)
ms = look_for_incoming_messages(o)
parse_messages(ms)
give_notice()
