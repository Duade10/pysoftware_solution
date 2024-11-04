from django import forms

from .models import Question


class QuestionUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Select PDF File')

    def __init__(self, *args, **kwargs):
        super(QuestionUploadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['pdf_file'].widget.attrs['accept'] = 'application/pdf'


class QuestionEditForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
