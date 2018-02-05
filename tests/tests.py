import os
import unittest

import numpy

import radioencode


class RadioEncodeTest(unittest.TestCase):
    def test_enc(self):
        arr = numpy.load(os.path.join('tests', 'data', 'hello.npy'))
        morse = radioencode.Morse()
        self.assertTrue(numpy.allclose(
            arr, morse.encode('hello')
        ))


if __name__ == '__main__':
    unittest.main()
