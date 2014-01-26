import os
import imp
import copy

from channel import Channel
from config import Config

class Command:
  name = "cmd"
  desc = "cmddesc"
  privileged = False
  
  ScopeMUC = 1
  ScopePrivate = 3
  
  scope = [ScopeMUC, ScopePrivate]
  
  Prefix = '!'
  
  def handle(self, msg):
    pass
  
class Plugin(object):
  plugins = []
  commands = {}

  name = "plugin"
  
  def __str__(self):
    return name

  def __init__(self):
    pass
    
  def handle(self, client, msg):
    if self.__class__ is not Plugin:
      return
      
    for plugin in Plugin.plugins:
      room_short = msg['mucroom'].split('@')[0]
      
      if msg['type'] in ('groupchat'):
        if room_short in Channel.channels:
          if plugin.name not in Channel.channels[room_short].plugins and plugin.name not in Config.get('misc.master_plugins'):
            continue
        
      plugin.handle(client, msg)
        
  def handle_commands(self, client, msg):
    def _check_priviledge(client, msg):
      if msg['from'] in Config.get('privileged'):
        return True
        
      try:  
        if msg['type'] == 'groupchat':
          room = client.plugin['xep_0045'].rooms[msg['from'].bare]
          mucuser = room[msg['from'].resource]
        
          if mucuser['jid'].bare in Config.get('privileged'):
            return True

      except:
        pass
        
      return False
    
    cmd = msg['body'].split(' ')[0]
    
    if cmd[0] != Command.Prefix:
      return
    
    if cmd[1:] not in self.commands:
      return

    cmd = self.commands[cmd[1:]]

    if msg['type'] == 'groupchat':
      if Command.ScopeMUC not in cmd.scope:
        return
      
      if cmd.privileged and not _check_priviledge(client, msg):
        return
    
    elif msg['type'] in ('normal', 'chat'):
      if Command.ScopePrivate not in cmd.scope:
        return
      
      jid = str(msg['from']).split(u'/')[0]
        
      if cmd.privileged and jid not in Config.get('privileged'):
        return
    
    new_msg = copy.copy(msg)
    new_msg['body'] = ' '.join(new_msg['body'].split(' ')[1:])
    cmd.handle(client, new_msg)
        
  @staticmethod
  def load_all():
    plugins = filter(lambda x: '.py' not in x, os.listdir('plugins'))
    
    for plugin in plugins:
      plgctx = imp.load_source(plugin, 'plugins{0}{1}{0}{1}.py'.format(os.sep, plugin))
      
      if hasattr(plgctx, 'inst'):
        Plugin.plugins.append(plgctx.inst)
