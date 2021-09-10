from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
    )
    class Meta:
        model = Document
        fields = ('description', 'docfile', )