import re

class Lexer:
  regexes = [
    ('NUM', re.compile("\d+")),
    ('STR', re.compile("[a-z]+")),
    ('MINUS', re.compile("-")),
    ('PLUS', re.compile("\+"))
  ]

  def __init__(self, input):
    self.input = input
    self.current_token = None

  def token(self):
    return self.current_token

  def advance(self):
    for token_type in Lexer.regexes:
      result = token_type[1].match(self.input)
      if result != None:
        token = result.group(0)
        self.input = self.input[len(token):]
        self.current_token = (token_type[0], token)
        return self.current_token
    if len(self.input) == 0:
      self.current_token = ('EOI', None)
      return self.current_token
    else:
      raise Exception
