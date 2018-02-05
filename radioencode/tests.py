import os
import unittest

import numpy

from radioencode import Morse


class RadioEncodeTest(unittest.TestCase):
    def test_enc(self):
        arr = numpy.load(os.path.join('radioencode', 'data', 'hello.npy'))
        morse = Morse()
        self.assertTrue(numpy.allclose(
            arr, morse.encode('hello')
        ))


if __name__ == '__main__':
    unittest.main()
