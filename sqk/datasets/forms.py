from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions
from sqk.datasets.models import *


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
        fields = ('name','species', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'datasetEditForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetEditForm, self).__init__(*args, **kwargs)

class DatasourceForm(forms.Form):
    '''Form for uploading audio or csv files.
    '''
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
                'Extract audio features',
                Div(
                    'audio',
                    # 'sample_rate',
                    css_class='inline'
                    ),
                'csv',
            ),
            FormActions(
                Submit('submit', 'Submit')
            )
        )
        super(DatasourceForm, self).__init__(*args, **kwargs)
    
    # def clean_sample_rate(self):
    #     if self.cleaned_data['sample_rate'] and not self.cleaned_data['audio']:
    #         raise forms.ValidationError('No audio file selected.')
    #     return self.cleaned_data['sample_rate']

class LabelNameForm(forms.Form):
    '''Form for creating a new independent variable for a
    dataset.
    '''
    name = forms.CharField(required=False,)
    value1 = forms.CharField(required=True,)
    value2 = forms.CharField(required=True,)
    # value3 = forms.CharField(required=False,)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'labelNameForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(LabelNameForm, self).__init__(*args, **kwargs)

class LabelValueForm(forms.Form):
    '''Form for creating a new label value. Should associate
    the new label value with the instance upon save.
    '''
    # TODO: 

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'labelValueForm'
        self.helper.form_method = 'post'
        super(DatasetForm, self).__init__(*args, **kwargs)

    



    



