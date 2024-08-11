from django import forms
from apps.corboard.models import Corboard, Comment

class CorboardForm(forms.ModelForm):
    class Meta:
        model = Corboard
        fields = ['title', 'content', 'corboardImg']

class CorCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']

    def __init__(self, *args, **kwargs):
        super(CorCommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget = forms.HiddenInput()

class CorSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')