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

  def next_token(self):
    return ''

  def advance(self):
    for token_type in Lexer.regexes:
      result = token_type[1].match(self.input)
      if result != None:
        return token_type[0], result.group(0)
