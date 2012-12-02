from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions
from sqk.datasets.models import *


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
    # TODO: allow creation of new species object
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

class LabelNameForm(forms.ModelForm):
    name = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))
    value1 = forms.CharField(required=True,)
    value2 = forms.CharField(required=True,)
    value3 = forms.CharField(required=False,)

    class Meta:
        model = LabelName
        fields = ('name', 'value1', 'value2', 'value3')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'labelNameForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(LabelNameForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name, created = LabelName.objects.get_or_create(
            name=self.cleaned_data['name'])
        
        return name

    def clean_value1(self):
        value1, created = LabelValue.objects.get_or_create(
            value=self.cleaned_data['value1'])
        return value1

    def clean_value2(self):
        value2, created = LabelValue.objects.get_or_create(
            value=self.cleaned_data['value2'])
        return value2

    def clean_value3(self):
        if self.cleaned_data['value3']:
            value3, created = LabelValue.objects.get_or_create(
                value=self.cleaned_data['value3'])
            return value3
        else: return None


    



