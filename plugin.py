import os
import imp

from channel import Channel

class Command:
  name = "cmd"
  desc = "cmddesc"
  privileged = False
  
  ScopeMUC = 1
  ScopePrivate = 3
  
  scope = [ScopeMUC, ScopePrivate]
  
  def handle(self, msg):
    pass
  
  
class Plugin(object):
  plugins = []

  name = "plugin"

  def __init__(self):
    pass
    
  def handle(self, client, msg):
    if self.__class__ is not Plugin:
      return
      
    for plugin in Plugin.plugins:
      try:
        if msg['mucroom'] in Channel.channels:
          if False == Channel.channels[msg['mucroom']].is_plugin_allowed(plugin.name):
            continue

      except:
        pass
        
      plugin.handle(client, msg)
        
  @staticmethod
  def load_all():
    plugins = filter(lambda x: '.py' not in x, os.listdir('plugins'))
    
    for plugin in plugins:
      plgctx = imp.load_source(plugin, 'plugins{0}{1}{0}{1}.py'.format(os.sep, plugin))
      
      if hasattr(plgctx, 'inst'):
        Plugin.plugins.append(plgctx.inst)
