import unittest
import roller
import random

class TestInt(unittest.TestCase):
  def test_eval(self):
    expr = roller.Int('123')
    self.assertEqual(expr.eval(), 123)

class TestRandomInt(unittest.TestCase):
  def test_eval_3d6_with_seed(self):
    random.seed(1)
    expr = roller.RandomInt('3', '6')
    self.assertEqual(expr.eval(), 12)

  def test_eval_3d6_max_with_seed(self):
    random.seed(23)
    expr = roller.RandomInt('3', '6')
    self.assertEqual(expr.eval(), 18)

  def test_memoize_eval(self):
    expr = roller.RandomInt('20', '20')
    self.assertEqual(expr.eval(), expr.eval())

class TestOp(unittest.TestCase):
  def test_plus(self):
    op = roller.Op('+')
    self.assertEqual(op.multiplier, 1)

  def test_minus(self):
    op = roller.Op('-')
    self.assertEqual(op.multiplier, -1)

  def test_invalid_op(self):
    with self.assertRaises(Exception):
      roller.Op('%')
