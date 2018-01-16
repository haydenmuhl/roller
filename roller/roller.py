import lex
import parse

def eval_roll(foo):
  lexer = lex.Lexer(foo)
  parser = parse.Parser(lexer)
  expr = parser.parse()
  return expr.eval()
