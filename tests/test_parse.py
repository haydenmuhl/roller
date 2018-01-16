import unittest
import roller.lex
import roller.roller
import random

def make_parser(input):
  lexer = roller.lex.Lexer(input)
  return roller.roller.Parser(lexer)

class TestParserEnsure(unittest.TestCase):
  # ensure method
  def test_ensure_one(self):
    parser = make_parser('5d6+3')
    parser.ensure(1)
    self.assertEqual(len(parser.tokens), 1)
    self.assertEqual(parser.tokens[0], roller.lex.Token('NUM', '5'))

  def test_ensure_two(self):
    parser = make_parser('5d6+3')
    parser.ensure(2)
    self.assertEqual(len(parser.tokens), 2)
    self.assertEqual(parser.tokens[0], roller.lex.Token('NUM', '5'))
    self.assertEqual(parser.tokens[1], roller.lex.Token('STR', 'd'))

  def test_ensure_more(self):
    parser = make_parser('5d6+3')
    parser.ensure(1)
    self.assertEqual(len(parser.tokens), 1)
    parser.ensure(3)
    self.assertEqual(len(parser.tokens), 3)

  def test_ensure_less(self):
    parser = make_parser('5d6+3')
    parser.ensure(3)
    self.assertEqual(len(parser.tokens), 3)
    parser.ensure(1)
    self.assertEqual(len(parser.tokens), 3)

  def test_ensure_too_many(self):
    parser = make_parser('5d6+3')
    parser.ensure(99)
    self.assertEqual(len(parser.tokens), 5)

class TestParserAccept(unittest.TestCase):
  def test_accept_one_type_success(self):
    parser = make_parser('1d4')
    self.assertTrue(parser.accept('NUM'))

  def test_accept_one_type_fail(self):
    parser = make_parser('1d4')
    self.assertFalse(parser.accept('STR'))

  def test_multiple_accepts(self):
    parser = make_parser('1d4')
    self.assertTrue(parser.accept('NUM', 'STR'))
    self.assertFalse(parser.accept('NUM', 'NUM'))
    self.assertTrue(parser.accept('NUM', 'STR', 'NUM'))

  def test_not_enough_tokens(self):
    parser = make_parser('1d4')
    self.assertFalse(parser.accept('NUM', 'STR', 'NUM', 'STR'))

  def test_foo(self):
    parser = make_parser('1+2')
    self.assertFalse(parser.accept('NUM', 'STR'))
    self.assertTrue(parser.accept('NUM'))

class TestParserChomp(unittest.TestCase):
  def test_basic_case(self):
    parser = make_parser('4d8+10')
    token = parser.chomp()
    self.assertEqual(len(parser.tokens), 0)
    self.assertEqual(token.type, 'NUM')
    self.assertEqual(token.value, '4')

  def test_with_buffered_tokens(self):
    parser = make_parser('4d8+10')
    parser.ensure(3)
    token = parser.chomp()
    self.assertEqual(len(parser.tokens), 2)
    self.assertEqual(parser.tokens[0], roller.lex.Token('STR', 'd'))
    self.assertEqual(token, roller.lex.Token('NUM', '4'))

class TestTerms(unittest.TestCase):
  def test_int(self):
    parser = make_parser('42')
    integer = parser.int()
    self.assertEqual(integer.__class__, roller.roller.Int)
    self.assertEqual(integer.value, 42)

  def test_random_int(self):
    parser = make_parser('8d4')
    random_integer = parser.random_int()
    self.assertEqual(random_integer.__class__, roller.roller.RandomInt)
    self.assertEqual(random_integer.num_dice, 8)
    self.assertEqual(random_integer.magnitude, 4)

  def test_invalid_random_int(self):
    parser = make_parser('8x4')
    with self.assertRaises(Exception):
      parser.random_int()

  def test_term_int(self):
    parser = make_parser('22')
    term = parser.term()
    self.assertEqual(term.__class__, roller.roller.Int)
    self.assertEqual(term.value, 22)

  def test_term_random(self):
    parser = make_parser('3d4')
    term = parser.term()
    self.assertEqual(term.__class__, roller.roller.RandomInt)
    self.assertEqual(term.num_dice, 3)
    self.assertEqual(term.magnitude, 4)

  def test_invalid_term(self):
    parser = make_parser('foo')
    with self.assertRaises(Exception):
      parser.term()

class TestOp(unittest.TestCase):
  def test_plus(self):
    parser = make_parser('+')
    op = parser.op()
    self.assertEqual(op.__class__, roller.roller.Op)
    self.assertEqual(op.multiplier, 1)

  def test_minus(self):
    parser = make_parser('-')
    op = parser.op()
    self.assertEqual(op.__class__, roller.roller.Op)
    self.assertEqual(op.multiplier, -1)

class TestModifier(unittest.TestCase):
  def test_plus_int(self):
    parser = make_parser('+5')
    mod = parser.modifier()
    self.assertEqual(mod.__class__, roller.roller.Modifier)
    self.assertEqual(mod.op.multiplier, 1)
    self.assertEqual(mod.term.__class__, roller.roller.Int)

  def test_minus_random_int(self):
    parser = make_parser('-4d3')
    mod = parser.modifier()
    self.assertEqual(mod.__class__, roller.roller.Modifier)
    self.assertEqual(mod.op.multiplier, -1)
    self.assertEqual(mod.term.__class__, roller.roller.RandomInt)

  def test_get_first_modifier(self):
    parser = make_parser('+2+1d8-1')
    mod = parser.modifier()

class TestExpression(unittest.TestCase):
  def test_one_full_int_term(self):
    parser = make_parser('+5')
    expr = parser.parse()
    self.assertEqual(expr.__class__, roller.roller.Expression)
    self.assertEqual(len(expr.modifiers), 1)

  def test_one_full_random_term(self):
    parser = make_parser('+3d6')
    expr = parser.parse()
    self.assertEqual(expr.__class__, roller.roller.Expression)
    self.assertEqual(len(expr.modifiers), 1)

  def test_multiple_full_terms(self):
    parser = make_parser('+2+1d8-1')
    expr = parser.parse()
    self.assertEqual(len(expr.modifiers), 3)

  def test_optional_first_operator(self):
    parser = make_parser('2d10-1')
    expr = parser.parse()
    self.assertEqual(len(expr.modifiers), 2)

    modifier = expr.modifiers[0]
    self.assertEqual(modifier.op.multiplier, 1)
    self.assertEqual(modifier.term.__class__, roller.roller.RandomInt)

    modifier = expr.modifiers[1]
    self.assertEqual(modifier.op.multiplier, -1)
    self.assertEqual(modifier.term.__class__, roller.roller.Int)
