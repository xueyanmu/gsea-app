from django.db import models
from django.core.exceptions import FieldError
from genes.models import Gene, CrossRef, CrossRefDB
from organisms.models import Organism

"""
Upload a document
"""
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

#TODO: ensure Organism is loaded first
class Geneset(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    size = models.IntegerField(default=0)
    grouping = models.CharField(max_length=64)
    # organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    organism = models.ManyToManyField(Organism, through='OrganismGS')
    function_database = models.CharField(max_length=200)
    genes = models.ManyToManyField(Gene, through='Parentset')
#todo: use Organism in the manytomany with geneset?
    class Meta:
        ordering = ['id']
    def __str__(self):
        return str(self.id)

class Parentset(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    geneset = models.ForeignKey(Geneset, on_delete=models.CASCADE)

class OrganismGS(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    geneset = models.ForeignKey(Geneset, on_delete=models.CASCADE)


#gs = Geneset(id="lung gene set", size=10, grouping="GO term", organism="homo sapiens", function_database="crossRef")