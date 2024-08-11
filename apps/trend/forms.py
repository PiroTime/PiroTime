from django import forms
from .models import Trend, Comment

class TrendForm(forms.ModelForm):
    class Meta:
        model = Trend
        fields = ['title', 'content', 'refer_url']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'writer', 'parent']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget = forms.HiddenInput()
        
class TrendSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')