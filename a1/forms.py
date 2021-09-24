from django import forms
from .models import Document, Gene
from django.forms import ModelForm
from searchableselect.widgets import SearchableSelect



class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
    )
    class Meta:
        model = Document
        fields = ('description', 'docfile', )


class GeneCheckForm(forms.ModelForm):
    entrez_id = forms.CharField(label = 'gene entrez ID', max_length=100)
    def clean(self):
        cleaned_data = super(GeneCheckForm, self).clean()
        entrez_id = cleaned_data.get("entrez_id")
        try:
            p = Gene.objects.get(id=entrez_id)
        except Gene.DoesNotExist:
            raise forms.ValidationError("Gene entrez ID is not in database.")