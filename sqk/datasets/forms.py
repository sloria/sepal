from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from sqk.datasets.models import Dataset, Species


class DatasetForm(forms.ModelForm):
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

    def clean_species(self):
        species, created = Species.objects.get_or_create(
            name=self.cleaned_data['species'])
        return species

class DatasetEditForm(forms.ModelForm):
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))
    class Meta:
        model = Dataset
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'datasetEditForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetEditForm, self).__init__(*args, **kwargs)

class DatasourceForm(forms.Form):
    csv = forms.FileField(label='Add data from CSV', required=False,)
    audio = forms.FileField(label='Extract data from audio file', required=False,)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'addSourceForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload'))
        super(DatasourceForm, self).__init__(*args, **kwargs)



