import json

class Config:
  file = ""
  data = None
  
  @staticmethod
  def get(keys, alt=None):
    tmp = Config.data
    
    for key in keys.split('.'):
      if key in tmp:
        tmp = tmp[key]
        continue
        
      try:
        tmp = tmp[int(key)]
        
      except:
        return alt
      
    return tmp
  
  @staticmethod
  def load(fn): # TODO: ... and check
    try:
      Config.data = json.load(open(fn))
      Config.file = fn
      
    except:
      pass
      
    finally:
      return Config.data != None