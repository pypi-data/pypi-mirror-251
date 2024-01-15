from disortify.formats import *

def test_asc():
  assert asc([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

def test_desc():
  assert desc([3, 1, 4, 1, 5, 9, 2, 6]) == [9, 6, 5, 4, 3, 2, 1, 1]
def test_caps():
  assert caps(['apple', 'banana', 'cherry']) == ['Apple', 'Banana', 'Cherry']

def test_lows():
  assert lows(['Apple', 'Banana', 'Cherry']) == ['apple', 'banana', 'cherry']

def test_ups():
  assert ups(['apple', 'banana', 'cherry']) == ['APPLE', 'BANANA', 'CHERRY']