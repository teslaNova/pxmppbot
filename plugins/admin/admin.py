from sleekxmpp import Message

from plugin import Command, Plugin
from channel import Channel
from config import Config
  
class PluginCommand(Command):
  name = "plugin"
  
  privileged = True
  
  def handle(self, client, msg):
    token = msg['body'].split(' ')
    
    try:
      if token[0] == '+':
        Channel.channels[token[1]].plugins.append(token[2])
        
        msg.reply("Plugin {0} in {1} has beend activated".format(token[2], token[1])).send()
    
      elif token[0] == '-':
        Channel.channels[token[1]].plugins.remove(token[2])
        
        msg.reply("Plugin {0} in {1} has beend deactivated".format(token[2], token[1])).send()
      
      elif token[0] == 'reload':
        Plugin.plugins = []
        Plugin.load_all()
        
        msg.reply("Plugins reloaded!").send()
        
      elif token[0] == 'list':
        plugins = []
        
        for p in Plugin.plugins:
          plugins.append(p.name)
        
        msg.reply("Plugins loaded: {0}".format(', '.join(plugins))).send()
        
      elif token[0] == 'active':
        msg.reply("Plugins active in {0}: {1}".format(Channel.channels[token[1]].jid, ', '.join(Channel.channels[token[1]].plugins))).send()
        
    except:
      pass
      
class QuitCommand(Command):
  name = "quit"
  
  privileged = True
  
  def handle(self, client, msg):
    msg.reply("Quitting..").send()
    quit()
      
class RosterCommand(Command):
  name = "roster"
  
  privileged = True
  
  def handle(self, client, msg):
    client.send_message(mto=msg['from'].bare, mbody=str(client.roster), mtype=msg['type'])

class ChannelCommand(Command):
  name = "channel"
  
  privileged = True
  
  def handle(self, client, msg):
    token = msg['body'].split(' ')
    
    try:
      if token[0] == 'list':
        msg.reply("Channels I'm in: {0}".format(', '.join(Channel.channels.keys()))).send()
        
      elif token[0] == 'roster':
        channel_jid = "{0}@{1}".format(token[1], Config.get('auth.muc', 'conference.jabber.de'))
        
        for nick in client.plugin['xep_0045'].rooms[channel_jid]:
          entry = client.plugin['xep_0045'].rooms[channel_jid][nick]
          
          client.send_message(mto=msg['from'].bare, mbody=str(entry), mtype=msg['type'])
      
      elif token[0] == 'rejoin':
        self.handle(client, client.make_message(msg['to'], "leave {0}".format(token[1]), None, msg['type'], None, msg['from'], None))
        self.handle(client, client.make_message(msg['to'], "join {0}".format(token[1]), None, msg['type'], None, msg['from'], None))
      
      elif token[0] == 'join':
        if token[1] not in Channel.channels.keys():
          channel_jid = "{0}@{1}".format(token[1], Config.get('auth.muc', 'conference.jabber.de'))
          Channel.join(client, channel_jid)
          
          if len(token) > 2:
            client.send_message(mto=channel_jid, mbody=' '.join(token[2:]), mtype='groupchat')
        
      elif token[0] == 'leave':
        if token[1] in Channel.channels.keys():
          channel_jid = "{0}@{1}".format(token[1], Config.get('auth.muc', 'conference.jabber.de'))
          
          if len(token) > 2:
            client.send_message(mto=channel_jid, mbody=' '.join(token[2:]), mtype='groupchat')
          
          Channel.channels[token[1]].leave()

    except:
      pass
      
class EvalCommand(Command):
  name = "eval"
  
  privileged = True
  
  def __init__(self):
    self.buf = {}
  
  def handle(self, client, msg):
    try:
        res = eval(msg['body'])
      
    except:
      return
      
    msg.reply("Result: {0}".format(res)).send()
    
class ConfigCommand(Command):
  name = "config"
  
  privileged = True
  
  def handle(self, client, msg):
    token = msg['body'].split(' ')
    
    try:
      if token[0] == 'reload':
        Config.load(Config.file)
        
      elif token[0] == 'save':
        pass
        
    except:
      pass
      
class AdminPlugin(Plugin):
  name = "admin"
  
  commands = {
    'plugin': PluginCommand(),
    'quit': QuitCommand(),
    'roster': RosterCommand(),
    'channel': ChannelCommand(),
    'eval': EvalCommand(), # evil, just for development purpose
    'config': ConfigCommand()
  }
  
  def handle(self, client, msg):
    self.handle_commands(client, msg)
  
inst = AdminPlugin() 