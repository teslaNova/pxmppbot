from sleekxmpp import Message

from plugin import Command, Plugin
from channel import Channel
from config import Config
  
class PluginCommand(Command):
  name = "plugin"
  
  privileged = True
  
  def handle(self, client, msg):
    token = msg['body'].split(' ')
    
    if len(token) != 3:
      return
    
    try:
      if token[0] == '+':
        print "+", " ", Channel.channels[token[1]]
        Channel.channels[token[1]].plugins.append(token[2])
    
      elif token[0] == '-':
        print "-", " ", Channel.channels[token[1]]
        Channel.channels[token[1]].plugins.remove(token[2])
        
    except:
      pass
      
class QuitCommand(Command):
  name = "quit"
  
  privileged = True
  
  def handle(self, client, msg):
    quit()
      
class AdminPlugin(Plugin):
  name = "admin"
  
  commands = {'plugin': PluginCommand(), 'quit': QuitCommand()}
  
  def handle(self, client, msg):
    self.handle_commands(client, msg)
  
inst = AdminPlugin() 