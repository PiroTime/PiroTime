from django import forms
from apps.accounts.sanitize import clean_html
from .models import Trend, Comment

class TrendForm(forms.ModelForm):
    class Meta:
        model = Trend
        fields = ['title', 'content', 'refer_url']

    def clean_content(self):
        return clean_html(self.cleaned_data.get('content'))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget = forms.HiddenInput()
        
class TrendSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')