import unittest
import numpy as np


class NumpyUniTest(unittest.TestCase):

    def test_nd_iter(self):
        a = np.arange(0, 60, 5)
        a = a.reshape(3, 4)
        print('原始数组是：')
        print(a)
        print('\n')
        for x in np.nditer(a, op_flags=['readwrite']):
            # x[...] = 2 * x
            x[...] = 2 * x
        print('修改后的数组是：')
        print(a)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
