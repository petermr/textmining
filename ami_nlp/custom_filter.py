from abc import abstractmethod
import re





class CustomFilter:
    """Not yet finished and tested"""
    def __init__(self):
        self.reg_min = 1
        self.reg_max = 999



    @property
    @abstractmethod
    def regex(self):
        pass

    def search_in_list(self, strings):
        """re.search() applied to list of strings. returns at first match
        :param strings: list of strings to search
        :return: first match or None"""
        for string in strings:
            if res := self.search_string(string):
                return res
        return None


    def search_string(self, string):
        """searched string against regex
        :param string: word or sentence
        :return: search result or None
        """
        return re.search(self.regex, string) if string else None

    @classmethod
    def make_count(cls, min_, max_):
        return f"{{{min_},{max_}}}" if max_ else f"{{{min_},}}"


class Aa1Filter(CustomFilter):
    def __init__(self):
        super().__init__()
        self.min = 10
        self.max = 9999

    @classmethod
    def create_filter(cls, min_=10, max_=9999):
        ami_filter = Aa1Filter()
        ami_filter.min = min_
        ami_filter.max = max_
        return ami_filter

    @property
    def regex(self):
        aa = "[ACDEFGHIKLMNPQRSTVWY]"
        count = self.make_count(self.min, self.max)
        print(f"|{count}|")
        reg = f"{aa}{count}"
        return reg

class Aa1MutFilter(CustomFilter):
    def __init__(self):
        def __init__(self):
            super().__init__()

    @property
    def regex(self, min=1, max=''):
        reg = f"[ACDEFGHIKLMNPQRSTVWY]\d{{{min},{max}}}[ACDEFGHIKLMNPQRSTVWY]"
        return reg

    @classmethod
    def create_filter(cls):
        filter = Aa1MutFilter()
        return filter


class Aa3Filter(CustomFilter):
    def __init__(self):
        def __init__(self):
            super().__init__()

    @property
    def regex(self, min=1, max='', case="camel"):
        """matches SINGLE 3-letter AminoAcid
        :param uppercase: ALA oherwise Ala
        :returns: regex
        """

        reg = "(Ala|Cys|Asp|Glu|Phe|Gly|His|Ile|Lys|Leu|Met|Asn|Pro|Gln|Arg|Ser|Thr|Val|Trp|Tyr)"
        if case =="upper":
            reg = reg.upper()
        aa3_re = f"{reg}"
        aa3_re = r"\b" + aa3_re + r"\b"
        return aa3_re

    @classmethod
    def create_filter(cls, case="camel"):
        filter = Aa3Filter()
        return filter


class DnaFilter(CustomFilter):
    def __init__(self):
        def __init__(self):
            super().__init__()

    @property
    def regex(self, min=10, max='', case="lower"):
        reg0 = f"[acgt]" if case == "lower" else "[ACGT]"
        return rf"\b{reg0}{{{min},{max}}}\b"

    @classmethod
    def create_filter(cls):
        filter = DnaFilter()
        return filter


class RnaFilter(CustomFilter):
    def __init__(self):
        def __init__(self):
            super().__init__()

    @property
    def regex(self, min=10, max='', case="lower"):
        reg0 = f"[acgt]" if case == "lower" else "[ACGT]"
        return rf"\b{reg0}{{{min},{max}}}\b"

    @classmethod
    def create_filter(cls):
        filter = RnaFilter()
        return filter




