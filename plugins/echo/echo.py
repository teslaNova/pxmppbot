from sleekxmpp import Message

from plugin import Command, Plugin
from config import Config
  
class EchoCommand(Command):
  name = "echo"
  
  def handle(self, client, msg):
    try:
     if Config.get('auth.user') in msg['from']:
        return
        
    except:
      pass
    
    if "has set the subject" in msg['body']: # should only in msg['type'] as headline, but it is not
      return
    
    if msg['type'] in ('normal', 'chat', 'groupchat'):
      msg.reply(msg['body']).send()
      
class EchoPlugin(Plugin):
  def handle(self, client, msg):
    EchoCommand().handle(client, msg)
  
inst = EchoPlugin() 