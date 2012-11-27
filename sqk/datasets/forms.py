from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions
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
    # TODO: make this a dropdown with a 'new species' choice
    species = forms.CharField(required=False,)
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))
    class Meta:
        model = Dataset
        fields = ('name','species', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'datasetEditForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetEditForm, self).__init__(*args, **kwargs)

    def clean_species(self):
        species, created = Species.objects.get_or_create(
            name=self.cleaned_data['species'])
        return species

class DatasourceForm(forms.Form):
    csv = forms.FileField(label='CSV', required=False,
        help_text='Optional')
    audio = forms.FileField(label='Audio file (.wav)', required=False,)
    # sample_rate = forms.IntegerField(label='Sample rate (Hz)',
    #     required=False,
    #     initial=44100,
    #     help_text='NOTE: Files will be resampled if necessary.')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'addSourceForm'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Add data',
                Div(
                    'audio',
                    # 'sample_rate',
                    css_class='inline'
                    ),
                'csv',
            ),
            FormActions(
                Submit('submit', 'Add')
            )
        )
        super(DatasourceForm, self).__init__(*args, **kwargs)
    
    # def clean_sample_rate(self):
    #     if self.cleaned_data['sample_rate'] and not self.cleaned_data['audio']:
    #         raise forms.ValidationError('No audio file selected.')
    #     return self.cleaned_data['sample_rate']



