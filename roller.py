import random
import re

def eval_roll(foo):
  lexer = lex.Lexer(foo)
  parser = parse.Parser(lexer)
  expr = parser.parse()
  return expr.eval()

class Lexer:
  regexes = [
    ('NUM', re.compile("\d+")),
    ('STR', re.compile("[a-z]+")),
    ('OP', re.compile("[-+]"))
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
        self.current_token = Token(token_type[0], token)
        return self.current_token
    if len(self.input) == 0:
      self.current_token = Token('EOI', None)
      return self.current_token
    else:
      raise Exception

class Token:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __eq__(self, other):
    if other.__class__ != Token:
      return False
    if self.type != other.type:
      return False
    if self.value != other.value:
      return False
    return True

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
    types = list(types)
    self.ensure(len(types))
    return types == [x.type for x in self.tokens[:len(types)]]

  def chomp(self):
    if len(self.tokens) > 0:
      token = self.tokens[0]
      self.tokens = self.tokens[1:]
    else:
      token = self.lexer.advance()
    return token

  def parse(self):
    expr = Expression()
    if self.accept('OP'):
      op = self.op()
    else:
      op = Op('+')
    term = self.term()
    expr.append(Modifier(op, term))
    while self.accept('OP'):
      expr.append(self.modifier())
    return expr

  def modifier(self):
    op = self.op()
    term = self.term()
    return Modifier(op, term)

  def op(self):
    return Op(self.chomp().value)

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

class Int:
  def __init__(self, token_str):
    self.value = int(token_str)

  def eval(self):
    return self.value

class Op:
  def __init__(self, op_str):
    if op_str == '+':
      self.multiplier = 1
    elif op_str == '-':
      self.multiplier = -1
    else:
      raise Exception

class Modifier:
  def __init__(self, op, term):
    self.op = op
    self.term = term

  def eval(self):
    return self.op.multiplier * self.term.eval()

class Expression:
  def __init__(self):
    self.modifiers = []

  def append(self, modifier):
    self.modifiers.append(modifier)

  def eval(self):
    sum = 0
    for m in self.modifiers:
      sum += m.eval()
    return sum
