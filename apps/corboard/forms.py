from django import forms
from apps.corboard.models import Corboard, Comment

class CorboardForm(forms.ModelForm):
    class Meta:
        model = Corboard
        fields = ['title', 'content', 'corboardImg']

class CorCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CorSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')