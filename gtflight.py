# A light-weight gtf parser in python
# BSD 3-Clause License [https://github.com/x-zang/gtflight/blob/main/LICENSE]
# Copyright (c) 2023, Xiaofei (Carl) Zang

import sys
import argparse
import re


class GtfItem:
    def __init__(self):
        self.name = "NameNone"
        self.feature = "FeatureNone"
        self.chr = "chrNone"
        self.lpos = -1
        self.rpos = -2


class GTF:
    def __init__(self):
        self.genes = dict()  # {gene:[txs]}
        self.txs = dict()  # {tx:gene}
        self.exons = dict()  # {exon:[txs]} := one exon can be in 1+ txs
        self.table = []  # table of gtf
        self.header = ""  # header of gtf

    def clear(self):
        self.genes = set()
        self.txs = set()
        self.exons = set()
        self.table = []
        self.header = ""

    def read(self, gtf_file):
        self.clear()
        self.table = ""
        with open(gtf_file, 'r') as fin:
            line = fin.readline()
            if line.startswith("#"):
                self.header = line.strip().split("\t")
                assert len(self.header) == 9
            for line in fin.readlines():
                entries = line.strip().split("\t")
                assert not line.startswith("#")
                assert len(entries) == 9
                entries[3] = int(entries[3])
                entries[4] = int(entries[4])
                entries[5] = int(entries[5])
                assert entries[6] in {'+', '-', '.'}
                assert entries[7] in {'0', '1', '2', '.'}
                if entries[9].strip():
                    entries[9] = GTF.attr_parse(entries[9])
                self.table.append(entries)

    @staticmethod
    def attr_parse(attr):
        if attr:
            assert attr[-1] == ';'
            # TODO: split ; outside quote
            # last one is ';' only thus empty
            s = attr.split(";")[:-1]
            return s
        else:
            return None

    def write(self, outfile):
        pass

    # get feature collections
    def genes(self):
        return self.genes.keys()

    def txs(self):
        return self.txs.keys()

    def exons(self):
        return self.exons.keys()

    def gene2txs(self):
        return self.genes

    def tx2gene(self):
        return self.txs

    def exon2txs(self):
        return self.exons

    # query feature
    # def txs(self, q):
    #     return self.txs.keys()
    #
    # def exons(self, q):
    #     return self.exons.keys()
    #
    # def gene2txs(self, q):
    #     return self.genes
    #
    # def tx2gene(self, q):
    #     return self.txs
    #
    # def exon2txs(self, q):
    #     return self.exons


if __name__ == "__init__":
    argv = sys.argv
    to_check_format = True
    GTF.read(argv[1])
