from sleekxmpp import Message

from plugin import Command, Plugin
from channel import Channel
from config import Config
  
import sqlite3  
  
class RegexQuizCommand(Command):
  name = "rqz"
  
  scope = [Command.ScopeMUC]
  
  def __init__(self):
    self.con = sqlite3.connect('rgxquiz.db')
    cur = self.con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS ''') # TODO: erstellen der tabellen für die user und deren fortschritte und die regex-rätsel

    self.con.commit()
    
  def __del__(self):
    self.con.close()
  
  def handle(self, client, msg):
    token = msg['body'].split(' ')
    
    try:
      
      if token[0] == 'status':
        pass
        
    except:
      pass
      
      
class RegexQuizPlugin(Plugin):
  name = "regex_quiz"
  
  commands = {
    'rqz': RegexQuizCommand()
  }
  
  def handle(self, client, msg):
    self.handle_commands(client, msg)
  
inst = RegexQuizPlugin() 