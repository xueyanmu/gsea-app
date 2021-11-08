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

