import unittest
import roller.parse
import roller.lex
import random

def make_parser(input):
  lexer = roller.lex.Lexer(input)
  return roller.parse.Parser(lexer)

class TestInt(unittest.TestCase):
  def test_eval(self):
    expr = roller.parse.Int('123')
    self.assertEqual(expr.eval(), 123)

class TestRandomInt(unittest.TestCase):
  def test_eval_3d6_with_seed(self):
    random.seed(1)
    expr = roller.parse.RandomInt('3', '6')
    self.assertEqual(expr.eval(), 12)

  def test_eval_3d6_max_with_seed(self):
    random.seed(23)
    expr = roller.parse.RandomInt('3', '6')
    self.assertEqual(expr.eval(), 18)

  def test_memoize_eval(self):
    expr = roller.parse.RandomInt('20', '20')
    self.assertEqual(expr.eval(), expr.eval())

class TestPlus(unittest.TestCase):
  def test_add_ints(self):
    plus = roller.parse.Plus()
    left = roller.parse.Int('5')
    right = roller.parse.Int('6')
    self.assertEqual(plus.op(left, right), 11)

  def test_add_int_and_random(self):
    plus = roller.parse.Plus()
    left = roller.parse.RandomInt('1', '6')
    right = roller.parse.Int('3')

    left_val = left.eval()

    self.assertEqual(plus.op(left, right), 3 + left_val)
