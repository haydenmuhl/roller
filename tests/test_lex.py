import unittest
import roller.lex

class TestLex(unittest.TestCase):
  def test_num(self):
    lexer = roller.lex.Lexer('123')
    self.assertEqual(lexer.advance(), roller.lex.Token('NUM', '123'))

  def test_str(self):
    lexer = roller.lex.Lexer('asdf')
    self.assertEqual(lexer.advance(), roller.lex.Token('STR', 'asdf'))

  def test_plus(self):
    lexer = roller.lex.Lexer('+')
    self.assertEqual(lexer.advance(), roller.lex.Token('PLUS', '+'))

  def test_minus(self):
    lexer = roller.lex.Lexer('-')
    self.assertEqual(lexer.advance(), roller.lex.Token('MINUS', '-'))

  def test_read_start(self):
    lexer = roller.lex.Lexer('-123')
    self.assertEqual(lexer.advance(), roller.lex.Token('MINUS', '-'))

  def test_multiple_tokens(self):
    lexer = roller.lex.Lexer('123abc')
    self.assertEqual(lexer.advance(), roller.lex.Token('NUM', '123'))
    self.assertEqual(lexer.advance(), roller.lex.Token('STR', 'abc'))

  def test_end_of_input(self):
    lexer = roller.lex.Lexer('5+6')
    self.assertEqual(lexer.advance(), roller.lex.Token('NUM', '5'))
    self.assertEqual(lexer.advance(), roller.lex.Token('PLUS', '+'))
    self.assertEqual(lexer.advance(), roller.lex.Token('NUM', '6'))
    self.assertEqual(lexer.advance(), roller.lex.Token('EOI', None))

  def test_illegal_syntax(self):
    lexer = roller.lex.Lexer('foo(123)')
    self.assertEqual(lexer.advance(), roller.lex.Token('STR', 'foo'))
    with self.assertRaises(Exception):
      lexer.advance()

  def test_token_uninitialized(self):
    lexer = roller.lex.Lexer('asdf')
    self.assertEqual(lexer.token(), None)

  def test_initialized(self):
    lexer = roller.lex.Lexer('a+b')
    self.assertEqual(lexer.advance(), roller.lex.Token('STR', 'a'))
    self.assertEqual(lexer.token(), roller.lex.Token('STR', 'a'))
    self.assertEqual(lexer.advance(), roller.lex.Token('PLUS', '+'))
    self.assertEqual(lexer.token(), roller.lex.Token('PLUS', '+'))

  def test_token_end_of_input(self):
    lexer = roller.lex.Lexer('a1')
    self.assertEqual(lexer.advance(), roller.lex.Token('STR', 'a'))
    self.assertEqual(lexer.advance(), roller.lex.Token('NUM', '1'))
    self.assertEqual(lexer.advance(), roller.lex.Token('EOI', None))
    self.assertEqual(lexer.token(), roller.lex.Token('EOI', None))

class TestToken(unittest.TestCase):
  def test_different_class(self):
    token = roller.lex.Token('foo', 'bar')
    self.assertNotEqual(token, 'doot')

  def test_different_type(self):
    me = roller.lex.Token('one', 'two')
    you = roller.lex.Token('yo', 'two')
    self.assertNotEqual(me, you)

  def test_different_value(self):
    me = roller.lex.Token('one', 'two')
    you = roller.lex.Token('one', 'three')
    self.assertNotEqual(me, you)

  def test_equal(self):
    me = roller.lex.Token('one', 'two')
    you = roller.lex.Token('one', 'two')
    self.assertEqual(me, you)
