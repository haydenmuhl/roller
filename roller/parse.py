import random

class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.tokens = []

  def ensure(self, size):
    while len(self.tokens) < size:
      if self.lexer.advance().type == 'EOI':
        break
      self.tokens.append(self.lexer.token())

  def accept(self, *types):
    self.ensure(len(types))
    return list(types) == [x.type for x in self.tokens]

  def chomp(self):
    if len(self.tokens) > 0:
      token = self.tokens[0]
      self.tokens = self.tokens[1:]
    else:
      token = self.lexer.advance()
    return token

  def term(self):
    if self.accept('NUM', 'STR'):
      return self.random_int()
    elif self.accept('NUM'):
      return self.int()
    else:
      raise Exception

  def int(self):
    int_str = self.chomp().value
    return Int(int_str)

  def random_int(self):
    num = self.chomp()
    d = self.chomp()
    if d.value != 'd':
      raise Exception
    mag = self.chomp()
    return RandomInt(num.value, mag.value)

### Expression classes ###

class Int:
  def __init__(self, token_str):
    self.value = int(token_str)

  def eval(self):
    return self.value

class RandomInt:
  def __init__(self, num_token, mag_token):
    self.num_dice = int(num_token)
    self.magnitude = int(mag_token)
    self.value = None

  def eval(self):
    if self.value == None:
      self.value = 0
      for x in range(self.num_dice):
        self.value += random.randint(1, self.magnitude)
    return self.value

class Plus:
  def op(self, left, right):
    return left.eval() + right.eval()
