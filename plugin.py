import os
import imp

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

  def __init__(self):
    pass
    
  def handle(self, client, msg):
    if self.__class__ is not Plugin:
      return
      
    for plugin in Plugin.plugins:
      plugin.handle(client, msg)
        
  @staticmethod
  def load_all():
    plugins = filter(lambda x: '.py' not in x, os.listdir('plugins'))
    
    for plugin in plugins:
      plgctx = imp.load_source(plugin, 'plugins{0}{1}{0}{1}.py'.format(os.sep, plugin))
      
      if hasattr(plgctx, 'inst'):
        Plugin.plugins.append(plgctx.inst)
