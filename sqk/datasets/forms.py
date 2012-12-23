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
        fields = ('name', 'species', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'datasetEditForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetEditForm, self).__init__(*args, **kwargs)


class DatasourceForm(forms.Form):
    '''Form for uploading audio or csv files.
    '''
    uploaded_file = forms.FileField(label='Audio file (.wav) or csv', required=True,)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'addSourceForm'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Extract audio features',
                Div(
                    'uploaded_file',
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

    def clean_uploaded_file(self):
        ufile = self.cleaned_data.get('uploaded_file', True)
        if ufile:
            # Check file size
            if ufile._size > 5 * 1024 * 1024:
                raise forms.ValidationError("Audio file too large ( > 5mb )")
            if not ufile.content_type in ["audio/wav", "text/csv"]:
                raise forms.ValidationError("Content is not wav or csv")
            return ufile
        else:
            raise forms.ValidationError("Could not read uploaded file")


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
