import unittest
import roller.lex

class TestLex(unittest.TestCase):
  def test_num(self):
    lexer = roller.lex.Lexer('123')
    self.assertEqual(lexer.advance(), ('NUM', '123'))

  def test_str(self):
    lexer = roller.lex.Lexer('asdf')
    self.assertEqual(lexer.advance(), ('STR', 'asdf'))

  def test_plus(self):
    lexer = roller.lex.Lexer('+')
    self.assertEqual(lexer.advance(), ('PLUS', '+'))

  def test_minus(self):
    lexer = roller.lex.Lexer('-')
    self.assertEqual(lexer.advance(), ('MINUS', '-'))

  def test_read_start(self):
    lexer = roller.lex.Lexer('-123')
    self.assertEqual(lexer.advance(), ('MINUS', '-'))

  def test_multiple_tokens(self):
    lexer = roller.lex.Lexer('123abc')
    self.assertEqual(lexer.advance(), ('NUM', '123'))
    self.assertEqual(lexer.advance(), ('STR', 'abc'))

  def test_end_of_input(self):
    lexer = roller.lex.Lexer('5+6')
    self.assertEqual(lexer.advance(), ('NUM', '5'))
    self.assertEqual(lexer.advance(), ('PLUS', '+'))
    self.assertEqual(lexer.advance(), ('NUM', '6'))
    self.assertEqual(lexer.advance(), ('EOI', None))

  def test_illegal_syntax(self):
    lexer = roller.lex.Lexer('foo(123)')
    self.assertEqual(lexer.advance(), ('STR', 'foo'))
    with self.assertRaises(Exception):
      lexer.advance()

  def test_token_uninitialized(self):
    lexer = roller.lex.Lexer('asdf')
    self.assertEqual(lexer.token(), None)

  def test_initialized(self):
    lexer = roller.lex.Lexer('a+b')
    self.assertEqual(lexer.advance(), ('STR', 'a'))
    self.assertEqual(lexer.token(), ('STR', 'a'))
    self.assertEqual(lexer.advance(), ('PLUS', '+'))
    self.assertEqual(lexer.token(), ('PLUS', '+'))

  def test_token_end_of_input(self):
    lexer = roller.lex.Lexer('a1')
    self.assertEqual(lexer.advance(), ('STR', 'a'))
    self.assertEqual(lexer.advance(), ('NUM', '1'))
    self.assertEqual(lexer.advance(), ('EOI', None))
    self.assertEqual(lexer.token(), ('EOI', None))

