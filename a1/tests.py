from django.test import TestCase
import unittest

from comtypes.safearray import numpy


# Create your tests here.
class TestCases(unittest.TestCase):

    def setUp(self):
        self.gsList = " "
        self.gList = ""
        self.missingGList = " "

    def tearDown(self) -> None:
        return

    # see a gene in mulitple genesets is truly in all the genesets
    def test_multiGene_in_all_GS(self):
