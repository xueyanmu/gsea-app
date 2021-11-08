from django.conf import settings
# import sys
# sys.path.insert(0, 'C:/Users/xueya/PycharmProjects/v1/v1')
# import settings
settings.configure(default_settings=settings, DEBUG=True)
from collections import defaultdict
from genes.models import Gene
from organisms.models import Organism
from a1.models import Geneset, Geneset_membership, OrganismGS

class GMT:

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
                else:
                   break
                # TODO: probs dont need this
                self._genesets[gsid] = set(genes)
                self._setnames[gsid] = name
                self._genes |= self._genesets[gsid]


                #create many2many relationships btwn gene, gs, and org
                for g in genes:
                    g = Gene(entrezid=g)
                    o = Organism(taxonomy_id=9606)
                    gs = Geneset(id=gsid,
                                 GStype="GO Biological Process",
                                 organism=o,
                                 setname=name)
                    gs_membership = Geneset_membership(g, gs)
                    org_membership = OrganismGS(o, gs)

                    print("gs objects= " + gs)
                    g.save()
                    gs.save()
                    o.save()
                    gs_membership.save()
                    org_membership.save()
if __name__ == '__main__':
    tester = GMT("hsaTest.txt")

