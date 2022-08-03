import unittest
# local
from ami_nlp.custom_filter import Aa1Filter, Aa1MutFilter, Aa3Filter


class TestFilters(unittest.TestCase):

    def test_aa1(self):
        ami_filter = Aa1Filter.create_filter()

        assert ami_filter.search_string("ARARARARARAR")
        assert not ami_filter.search_string("ARARARBRARAR")

    def test_aa1_mut(self):
        ami_filter = Aa1MutFilter.create_filter()
        assert ami_filter.search_string("A123K")
        assert ami_filter.search_string("K321Y")
        assert not ami_filter.search_string("B342Y")

    def test_aa3(self):
        ami_filter = Aa3Filter.create_filter()
        assert ami_filter.search_string("Tyr")
        assert ami_filter.search_string(" Met ")
        assert ami_filter.search_string("junk Cys grot")
        assert not ami_filter.search_string("Methyl")
