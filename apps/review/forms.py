from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'giturl']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'writer', 'parent']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget = forms.HiddenInput()

class ReviewSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')