from sleekxmpp import ClientXMPP

from config import Config

class Channel(object):
  channels = {}
  
  def __init__(self, client, jid, allowed_plugins):
    self.client = client
    self.jid = jid
    self.plugins = allowed_plugins
    
  @staticmethod
  def join(client, jid, allowed_plugins=[], nick=''):
    if nick is '':
      nick = Config.get('auth.user')

    ch = Channel(client, jid, allowed_plugins)
    ch.nick = nick
    
    Channel.channels[jid] = ch
    
    client.plugin['xep_0045'].joinMUC(jid, nick, wait=True)
    
  def leave(self):
    del Channel.channels[self.jid]
    client.plugin['xep_0045'].leaveMUC(self.jid, self.nick, 'leaving..')