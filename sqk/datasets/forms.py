from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from sqk.datasets.models import Dataset, Label

class DatasetForm(forms.ModelForm):
    source = forms.FileField(required=True, label='Data file',
        help_text='Must be a .csv file.')
    feature_row = forms.IntegerField(required=False, initial=1,
        help_text='Specify the header row. Defaults to first row.')
    label_col = forms.IntegerField(required=False,
        help_text='Optionally specify which column contains class labels.',
        label='Label column')
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))
    class Meta:
        model = Dataset
        fields = ('source', 'name', 'description', 'feature_row', 'label_col')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetForm, self).__init__(*args, **kwargs)

    def clean_label_col(self):
        col = self.cleaned_data['label_col']
        if col <= 0:
            return -1
        else:
            return col-1 # 0-indexed column value

    def clean_feature_row(self):
        row = self.cleaned_data['feature_row']
        if self.cleaned_data.has_key('source'):
            source = self.cleaned_data['source']
            n_rows = len(source.readlines())
            if row > n_rows:
                raise forms.ValidationError('Cannot be greater than number of rows in dataset')
        if row <= 0:
            raise forms.ValidationError('Must be 1 or greater')
        else:
            return row-1 # 0-indexed row value

class DatasetEditForm(forms.ModelForm):
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5}))
    class Meta:
        model = Dataset
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DatasetEditForm, self).__init__(*args, **kwargs)

