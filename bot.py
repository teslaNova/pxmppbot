import sleekxmpp

from config import Config
from plugin import Plugin
from channel import Channel

class Bot(sleekxmpp.ClientXMPP):
  def __init__(self):
    jid = "{0}@{1}/{2}".format(Config.get('auth.user'), Config.get('auth.server'), Config.get('auth.resource', ''))
    sleekxmpp.ClientXMPP.__init__(self, jid, Config.get('auth.pwd', ''))
    
    self.add_event_handler('session_start', self.start)
    self.add_event_handler('message', self.message_private)
    self.add_event_handler('groupchat_message', self.message_muc)
    
    self.register_plugin('xep_0030')
    self.register_plugin('xep_0045')
    self.register_plugin('xep_0199')
    
  def run(self):
    if self.connect((Config.get('auth.server'), 5222)):
      self.process(block=True)   
      
  def start(self, event):
    self.send_presence()
    self.get_roster()
    
    for channel in Config.get('channels'):
      Channel.join(self, channel['jid'], channel['plugins'])
    
  def message_private(self, msg):
    Plugin().handle(self, msg)
    
  def message_muc(self, msg):
    pass

if __name__ == '__main__':
  config_fn = "default.conf" # Later: Pass as Argument to script 
  Config.load(config_fn)
  
  Plugin.load_all()
  
  bot = Bot()
  
  try:
    bot.run()
  except KeyboardInterrupt:
    quit()