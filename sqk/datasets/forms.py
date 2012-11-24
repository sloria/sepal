from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from sqk.datasets.models import Dataset, Label

class DatasetForm(forms.ModelForm):
    source = forms.FileField(required=True, label='Data file',
        help_text='Must be a .csv file.')
    feature_row = forms.IntegerField(required=False,
        help_text='Specify the header row. Defaults to first row.')
    label_col = forms.IntegerField(required=False,
        help_text='Optionally specify which column contains class labels.',
        label='Label column')
    class Meta:
        model = Dataset
        fields = ('source', 'name', 'description', 'feature_row', 'label_col')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create'))
        super(DatasetForm, self).__init__(*args, **kwargs)

    def clean_label_col(self):
        # TODO: label_col shouldn't be > # of columns
        col = self.cleaned_data['label_col']
        if col <= 0:
            return -1
        else:
            return col-1

    def clean_feature_row(self):
        # TODO: row shouldn't be > # of rows
        row = self.cleaned_data['feature_row']
        if row <= 0:
            return 0
        else:
            return row-1
