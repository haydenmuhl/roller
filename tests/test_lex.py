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
