import unittest

from comtypes.safearray import numpy

from GMT import GMT



class TestGMT(unittest.TestCase):

    def setUp(self):
        self.gmt_file = 'test_data/test_gmt.gmt'
        self.assoc_file = 'test_data/test_assoc_file.txt'
        self.assoc_file_scrambled_cols = 'test_data/test_assoc_file.txt'

    def tearDown(self):
        return


    def test_open_dab(self):
        # Test the total number of loaded genes
        self.assertEqual(len(self.dab.gene_list), 16)

        # Test the total number of values (16 choose 2)
        self.assertEqual(len(self.dab.dat), 120)

    def test_get_value(self):
        # Test the values from Dab class with values from dab exported as dat
        for l in self.dat:
            g1, g2, value = l.strip().split('\t')
            val = float(value)
            dat_val = self.dab.get_value_genestr(g1, g2)
            assert numpy.isclose(val, dat_val, rtol=1e-05, atol=1e-08)

    def test_get(self):
        for i, g1 in enumerate(self.dab.gene_list):
            vals = self.dab.get(g1)
            for j, g2 in enumerate(self.dab.gene_list):
                if g1 == g2:
                    # Self interaction should be 1
                    self.assertEqual(vals[j], 1)
                else:
                    # Test the values from dab.get match dab.get_value
                    self.assertEqual(
                        vals[j], self.dab.get_value_genestr(g1, g2))

    def test_open_qdab(self):
        # Test the total number of loaded genes
        self.assertEqual(len(self.qdab.gene_list), 16)

        # Test the total number of values (16 choose 2)
        self.assertEqual(len(self.qdab.dat), 120)

    def test_qdab_get_value(self):
        # Test the values from Dab class with values from dab exported as dat
        for l in self.qdab_dat:
            g1, g2, value = l.strip().split('\t')
            val = float(value)
            dat_val = self.qdab.get_value_genestr(g1, g2)
            assert numpy.isclose(val, dat_val, rtol=1e-05, atol=1e-08)

    def test_qdab_get(self):
        for i, g1 in enumerate(self.qdab.gene_list):
            vals = self.qdab.get(g1)
            for j, g2 in enumerate(self.qdab.gene_list):
                if g1 == g2:
                    # Self interaction should be 1
                    self.assertEqual(vals[j], 1)
                else:
                    # Test the values from dab.get match dab.get_value
                    self.assertEqual(
                        vals[j], self.qdab.get_value_genestr(g1, g2))

if __name__ == '__main__':
    unittest.main()

tester = TestGMT()
