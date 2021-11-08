import argparse
from collections import defaultdict


class GMT:

    '''
    Builds a GMT object given a file.
    Forked from FunctionLab/flib.
    '''

    def __init__(self, filename=None):
        self._genesets = defaultdict(set)
        self._setnames = {}
        self._genes = set()

        if filename:
            gmtfile = filename

            for line in gmtfile:
                tok = line.strip().split('\t')
                if len(tok) > 3:  # tab delim genes column
                    (gsid, name, genes) = tok[0], tok[1], tok[2:]
                elif(len(tok)) == 3:  # space delim genes column
                    #print(tok)
                    (gsid, name, genes) = tok[0], tok[1], tok[2].strip().split(" ")
                else: #TODO: FIX THE WORKAROUND HERE
                   break
                self._genesets[gsid] = set(genes)
                self._setnames[gsid] = name
                self._genes |= self._genesets[gsid]

    def ids(self):
        return self.genesets.keys()

    @property
    def genesets(self):
        return self._genesets

    @property
    def genes(self):
        return self._genes

    @property
    def setnames(self):
        return self._setnames

    def get_genes(self, gsid):
        return self._genesets[gsid]

    def get_genes_str(self, gsid):
        return " ".join(self._genesets[gsid])

    def add_geneset(self, gsid=None, name=None):
        self._setnames[gsid] = name
        self._genesets[gsid] = set()

    def add_gene(self, gsid, gene):
        self._genesets[gsid].add(gene)

    def add_genes(self, gsid, genes):
        for gene in genes:
            self._genesets[gsid].add(gene)

    def add(self, gmt):
        for gsid, genes in gmt.genesets.items():
            self._genesets[gsid] |= genes
        for gsid, name in gmt.setnames.items():
            if gsid not in self._setnames:
                self._setnames[gsid] = gmt.setnames[gsid]

    def write(self, outfile):
        outf = outfile
        for gsid, genes in self._genesets.items():
            outf.write(gsid + '\t' + self._setnames[gsid] +
                       '\t' + ' '.join(list(genes)) + '\n')
        outf.close()

    def write_as_long(self, outfile):
        '''
        writes a GMT file as an association ("long") file format
        '''
        gnames = self._setnames
        for gset in self._genesets:
            for gene in self.get_genes(gset):
                outfile.write(gset + "\t" + gnames[gset] + "\t" + gene + "\n")
        outfile.close()

    def __repr__(self):
        return self._genesets.__repr__()

    @staticmethod
    def convert_to_gmt(infile, gsc=0, gdc=1, gc=2):
        '''
        takes an association file or a file in "long" format
        and returns a GMT object
        gsc - column in file containing the geneset ids
        gdc - column in file containing the geneset descriptions / names
        gc - column in file containing the genes
        '''
        gs = GMT()
        for line in infile:
            words = line.strip().split("\t")
            if words[gsc] not in gs.genesets:
                gs.add_geneset(gsid=words[gsc], name=words[gdc])
            gs.add_gene(words[gsc], words[gc])

        return gs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='extra functionality for building and working with genesets in GMT format')
    parser.add_argument('-i', '--infile', dest='infile', type=argparse.FileType('r'),
                        help="path to input file")
    parser.add_argument('-a', '--association', dest='wide', action='store_true', default=False,
                        help="convert the input file from an association file\
                        (where each gene is on a separate line) to GMT format.\
                        Association file must be tab delimited.")
    parser.add_argument('-l', '--to-long', dest='long', action='store_true', default=False,
                        help="convert from a GMT file to an association file\
                        (where each gene is on a separate line).")
    parser.add_argument('-g', '--gene-col', dest='gc', default=2, type=int,
                        help="The column position of genes in a file when an association\
                        file is given. Assumes columns are zero indexed.")
    parser.add_argument('-s', '--geneset-col', dest='gsc', default=0, type=int,
                        help="The column position of geneset identiifers in a file when an association\
                        file is given. Assumes columns are zero indexed and takes the first column\
                        by default.")
    parser.add_argument('-d', '--gene-desc-col', dest='gdc', default=1, type=int,
                        help="The column position of geneset names/descriptions in a file when an association\
                        file is given. Assumes columns are zero indexed and takes the second column\
                        by default.")
    parser.add_argument('-o', '--output-file', dest='outfile', type=argparse.FileType('w'),
                        help="File to write. If missing, output will be directed to\
                        stdout.")
    options = parser.parse_args()

    if options.wide:
        gs = GMT.convert_to_gmt(options.infile, options.gsc, options.gdc, options.gc)
    else:
        if options.infile:
            gs = GMT(options.infile)

    if options.long:
        if options.outfile:
            gs.write_as_long(options.outfile)
        else:
            print("outfile parameter needed to export to long")
    else:  # handle all other outputs as they will be GMTs
        if options.outfile:
            gs.write(options.outfile)
        else:
            for gset in gs.setnames:
                print(gset + "\t" + gs.setnames[gset] + "\t" + gs.get_genes_str(gset))