from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from sepal.datasets.models import *


class DatasetForm(forms.ModelForm):
    '''Form for creating a new dataset.
    '''
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))
    species = forms.CharField(required=False,)

    class Meta:
        model = Dataset
        fields = ('name', 'species', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetForm, self).__init__(*args, **kwargs)


class DatasetEditForm(forms.ModelForm):
    '''Form for editing the title, species, and description
    of a dataset.
    '''
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Dataset
        fields = ('name', 'species', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'datasetEditForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetEditForm, self).__init__(*args, **kwargs)
