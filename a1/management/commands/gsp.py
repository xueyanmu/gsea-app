"""
   This command parses gene info file(s) and saves the corresponding
   gene and geneset objects into the database. It takes 1 arg: file

      # Call genes_load_geneinfo to populate the database:
      python manage.py gsp --input_file=data/hsaTest.txt
"""

import logging
from django.core.management.base import BaseCommand
from genes.models import Gene
from organisms.models import Organism
from a1.models import OrganismGS, Geneset, Geneset_membership

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Command(BaseCommand):
    help = ('Add standards from stds_file with the associations from ' +
            'assoc_file.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--input_file',
            help="Load predictions into the database",
            required=True
        )

    def handle(self, *args, **options):

        fn = options.get('input_file', None)

        with open(fn, "r") as f:
            gsid = None
            name = None
            genes = None

            for line in f:
                # get rid of header
                # if header:
                #     header = False
                #     continue

                # parse geneset type, geneset name, and genes
                tok = line.strip().split('\t')
                if len(tok) > 3:  # tab delim genes column
                    (gsid, name, genes) = tok[0], tok[1], tok[2:]
                elif (len(tok)) == 3:  # space delim genes column
                    # print(tok)
                    (gsid, name, genes) = tok[0], tok[1], tok[2].strip().split(" ")
                else:
                    break

                # create many2many relationships btwn gene, gs, and org
                for g in genes:
                    #todo: i made all the organism attrs nonunique lmao
                    o = Organism(taxonomy_id=9606)
                    o.save()
                    #uniqueness error
                    g = Gene(entrezid=g, standard_name=name, organism=o)
                    g.save()

                    name.save()
                    print("poop")
                    gs = Geneset(id=gsid,
                                 grouping="GO Biological Process",
                                 organism=o,
                                 setname=str(name))
                    gs_membership = Geneset_membership(g, gs)
                    org_membership = OrganismGS(o, gs)
                    print("11111")
                    print("gs objects= " + str(gs))

                    gs.save()

                    gs_membership.save()
                    org_membership.save()


