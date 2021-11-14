"""
   This command parses gene info file(s) and saves the corresponding
   gene and geneset objects into the database. It takes 1 arg: file

      # Call genes_load_geneinfo to populate the database:
      python manage.py gsp --input_file=data/hsaTest.txt
"""

import logging

from django.core.exceptions import ObjectDoesNotExist
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
                #     header = False
                #     continue

                # parse geneset type, geneset name, and genes
                tok = line.strip().split('\t')
                if len(tok) > 3:  # tab delim genes column
                    (gsid, name, genes) = tok[0], tok[1], tok[2:]
                elif (len(tok)) == 3:  # space delim genes column
                    (gsid, name, genes) = tok[0], tok[1], tok[2].strip().split(" ")
                else:
                    break

                # create many2many relationships btwn gene, gs, and org
                # todo: i made all the organism attrs the same lmao
                for g in genes:

                    try:
                        o = Organism.objects.filter(taxonomy_id=9606)[0]
                    except ObjectDoesNotExist:
                        o = Organism.objects.create(taxonomy_id=9606)

                    try:
                        gs = Geneset.objects.get(id=gsid)

                    except ObjectDoesNotExist:
                        name = name.split("(")[0]


                        gs = Geneset(id=gsid,
                                     grouping="GO Biological Process",
                                     )
                        gs.setname = str(name)
                        gs.save()

                    # get all the genes
                    try:
                        #todo: here
                        g = Gene.objects.filter(entrezid=g).update(geneset_name=gsid)

                    except ObjectDoesNotExist:  # gene doesnt exist yet
                        g = Gene.objects.create(entrezid=g, standard_name=name, organism=o, geneset_name=gsid)

                    try:
                        # todo: need try/except here too?
                        gs_membership = Geneset_membership(gene=g, geneset=gs)
                        gs_membership.save()

                        org_membership = OrganismGS(organism=o, geneset=gs)
                        org_membership.save()


                    except ObjectDoesNotExist:
                        pass
