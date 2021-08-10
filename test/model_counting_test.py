#Copyright 2021 by Matteo Munari

import unittest
from ddt import ddt, data
from pysat.solvers import Solver

from model_counting import count_models
from utils import load
from formulas import *


@ddt
class TestModelCounting(unittest.TestCase):

    @data('test_01.txt',
          'test_02.txt',
          'test_03.txt',
          'test_04.txt',
          'test_05.txt',
          'test_06.txt',
          'test_07.txt',
          'test_08.txt',
          'test_09.txt',
          'test_10.txt')

    def test_model_counting(self, input_file):
        cnf, _, n_variables = load('../test_files/'+input_file)
        n_var_in_cnf = len(cnf.atoms() - {false, true, f, t})
        ignored_vars = n_variables - n_var_in_cnf

        s = Solver(bootstrap_with=list_notation(cnf))
        gt_count = 0
        for _ in s.enum_models():
            gt_count += 1

        ddnnf = to_d_dnnf(cnf, reduction=True)
        count = count_models(ddnnf)

        print(count * 2**ignored_vars)
        self.assertEqual(gt_count * 2 ** ignored_vars, count * 2 ** ignored_vars)


if __name__ == '__main__':
    unittest.main()
