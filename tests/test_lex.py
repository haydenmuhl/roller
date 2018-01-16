import unittest
import roller

class TestLex(unittest.TestCase):
  def test_num(self):
    lexer = roller.Lexer('123')
    self.assertEqual(lexer.advance(), roller.Token('NUM', '123'))

  def test_str(self):
    lexer = roller.Lexer('asdf')
    self.assertEqual(lexer.advance(), roller.Token('STR', 'asdf'))

  def test_plus(self):
    lexer = roller.Lexer('+')
    self.assertEqual(lexer.advance(), roller.Token('OP', '+'))

  def test_minus(self):
    lexer = roller.Lexer('-')
    self.assertEqual(lexer.advance(), roller.Token('OP', '-'))

  def test_read_start(self):
    lexer = roller.Lexer('-123')
    self.assertEqual(lexer.advance(), roller.Token('OP', '-'))

  def test_multiple_tokens(self):
    lexer = roller.Lexer('123abc')
    self.assertEqual(lexer.advance(), roller.Token('NUM', '123'))
    self.assertEqual(lexer.advance(), roller.Token('STR', 'abc'))

  def test_end_of_input(self):
    lexer = roller.Lexer('5+6')
    self.assertEqual(lexer.advance(), roller.Token('NUM', '5'))
    self.assertEqual(lexer.advance(), roller.Token('OP', '+'))
    self.assertEqual(lexer.advance(), roller.Token('NUM', '6'))
    self.assertEqual(lexer.advance(), roller.Token('EOI', None))

  def test_illegal_syntax(self):
    lexer = roller.Lexer('foo(123)')
    self.assertEqual(lexer.advance(), roller.Token('STR', 'foo'))
    with self.assertRaises(Exception):
      lexer.advance()

  def test_token_uninitialized(self):
    lexer = roller.Lexer('asdf')
    self.assertEqual(lexer.token(), None)

  def test_initialized(self):
    lexer = roller.Lexer('a+b')
    self.assertEqual(lexer.advance(), roller.Token('STR', 'a'))
    self.assertEqual(lexer.token(), roller.Token('STR', 'a'))
    self.assertEqual(lexer.advance(), roller.Token('OP', '+'))
    self.assertEqual(lexer.token(), roller.Token('OP', '+'))

  def test_token_end_of_input(self):
    lexer = roller.Lexer('a1')
    self.assertEqual(lexer.advance(), roller.Token('STR', 'a'))
    self.assertEqual(lexer.advance(), roller.Token('NUM', '1'))
    self.assertEqual(lexer.advance(), roller.Token('EOI', None))
    self.assertEqual(lexer.token(), roller.Token('EOI', None))

class TestToken(unittest.TestCase):
  def test_different_class(self):
    token = roller.Token('foo', 'bar')
    self.assertNotEqual(token, 'doot')

  def test_different_type(self):
    me = roller.Token('one', 'two')
    you = roller.Token('yo', 'two')
    self.assertNotEqual(me, you)

  def test_different_value(self):
    me = roller.Token('one', 'two')
    you = roller.Token('one', 'three')
    self.assertNotEqual(me, you)

  def test_equal(self):
    me = roller.Token('one', 'two')
    you = roller.Token('one', 'two')
    self.assertEqual(me, you)
