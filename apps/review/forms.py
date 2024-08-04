from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'writer', 'giturl']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'writer']

class ReviewSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')