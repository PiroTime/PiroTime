from django import forms
from .models import Trend, Comment

class TrendForm(forms.ModelForm):
    class Meta:
        model = Trend
        fields = ['title', 'content', 'refer_url']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'writer']
        
class TrendSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')