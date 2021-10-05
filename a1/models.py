from django.db import models
from django.core.exceptions import FieldError
from genes.models import Gene, CrossRef, CrossRefDB
from organisms.models import Organism

"""
Upload a document
"""
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    docfile = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

#TODO: ensure Organism is loaded first
class Geneset(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    size = models.IntegerField(default=0)
    grouping = models.CharField(max_length=64)
    # organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    organism = models.ManyToManyField(Organism, through='OrganismGS')
    function_database = models.CharField(max_length=200)
    genes = models.ManyToManyField(Gene, through='Geneset_membership')
#todo: use Organism in the manytomany with geneset?
    class Meta:
        ordering = ['id']
    def __str__(self):
        return str(self.id)
    def add_genes(self):
        geneset = self  #name of the geneset, ie. GOterm
        geneset_name = self.id
        genes = Gene.objects.filter(geneset_name=geneset_name)
        self.size = len(genes)
        self.grouping = "GO term"

        for g in genes:
            gm = Geneset_membership(geneset=geneset, gene=g)
            gm.save()


class Geneset_membership(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    geneset = models.ForeignKey(Geneset, on_delete=models.CASCADE)


class OrganismGS(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    geneset = models.ForeignKey(Geneset, on_delete=models.CASCADE)


#gs = Geneset(id="lung gene set", size=10, grouping="GO term", organism="9606", function_database="crossRef")