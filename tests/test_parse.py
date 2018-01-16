import unittest
import roller.lex
import roller.parse
import random

def make_parser(input):
  lexer = roller.lex.Lexer(input)
  return roller.parse.Parser(lexer)

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

class TestExpressions(unittest.TestCase):
  def test_int(self):
    parser = make_parser('42')
    integer = parser.int()
    self.assertEqual(integer.__class__, roller.parse.Int)
    self.assertEqual(integer.value, 42)

  def test_random_int(self):
    parser = make_parser('8d4')
    random_integer = parser.random_int()
    self.assertEqual(random_integer.__class__, roller.parse.RandomInt)
    self.assertEqual(random_integer.num_dice, 8)
    self.assertEqual(random_integer.magnitude, 4)

  def test_invalid_random_int(self):
    parser = make_parser('8x4')
    with self.assertRaises(Exception):
      parser.random_int()

  def test_term_int(self):
    parser = make_parser('22')
    term = parser.term()
    self.assertEqual(term.__class__, roller.parse.Int)
    self.assertEqual(term.value, 22)

  def test_term_random(self):
    parser = make_parser('3d4')
    term = parser.term()
    self.assertEqual(term.__class__, roller.parse.RandomInt)
    self.assertEqual(term.num_dice, 3)
    self.assertEqual(term.magnitude, 4)

  def test_invalid_term(self):
    parser = make_parser('foo')
    with self.assertRaises(Exception):
      parser.term()

